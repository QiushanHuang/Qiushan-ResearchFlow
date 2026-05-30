#!/usr/bin/env python3
"""Validate a connected ResearchFlow project adapter and local indexes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_LOCAL_INDEXES = {
    "tasks",
    "knowledge",
    "artifacts",
    "experiments",
    "creative_passes",
    "golden_runs",
    "procedures",
    "repeat_runs",
    "exceptions",
    "skill_usage",
}

FORBIDDEN_GLOBAL_FIELDS = {
    "facts",
    "memory",
    "claims",
    "digests",
    "procedure_body",
    "secrets",
    "token",
    "private_path",
}

FORBIDDEN_GLOBAL_PATH_PARTS = ("local.private", "/raw/", "/logs/", "/artifacts/")
ADAPTER_MODES = {"native", "legacy_shadow"}


def emit(level: str, path: str, rule: str, message: str, findings: list[tuple[str, str, str, str]]) -> None:
    findings.append((level, path, rule, message))


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() in {"null", "none"}:
        return None
    try:
        return int(value)
    except ValueError:
        return value.strip('"').strip("'")


def parse_simple_yaml(path: Path) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or raw.strip().startswith("- "):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if value.strip() == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = parse_scalar(value)
    return root


def read_jsonl(path: Path, findings: list[tuple[str, str, str, str]]) -> list[dict[str, Any]]:
    entries = []
    if not path.exists():
        emit("FAIL", str(path), "missing", "index does not exist", findings)
        return entries
    seen = set()
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            emit("FAIL", str(path), "jsonl", f"line {lineno}: {exc.msg}", findings)
            continue
        entry_id = entry.get("id")
        if entry_id in seen:
            emit("FAIL", str(path), "duplicate-id", f"duplicate id {entry_id}", findings)
        seen.add(entry_id)
        entries.append(entry)
    return entries


def is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def resolve_declared_path(adapter_mode: str, project_root: Path, adapter_root: Path, value: str) -> Path:
    raw = Path(value)
    if raw.is_absolute():
        return raw.resolve()
    if adapter_mode == "native" and value.startswith(".researchflow/"):
        return (project_root / value).resolve()
    return (adapter_root / value).resolve()


def validate_global_pointer(
    framework_root: Path,
    adapter: Path,
    project_id: str,
    project_root: Path,
    adapter_mode: str,
    findings: list[tuple[str, str, str, str]],
) -> dict[str, Any] | None:
    entries = read_jsonl(framework_root / "indexes" / "project.index.jsonl", findings)
    matches = [entry for entry in entries if entry.get("id") == project_id]
    if not matches:
        emit("FAIL", str(framework_root / "indexes" / "project.index.jsonl"), "project-pointer", "missing global project pointer", findings)
        return None
    entry = matches[0]
    for field in FORBIDDEN_GLOBAL_FIELDS:
        if field in entry:
            emit("FAIL", "indexes/project.index.jsonl", "pointer-only", f"forbidden global project field {field}", findings)
    for key in ("path", "adapter_path"):
        value = str(entry.get(key, ""))
        if value and Path(value).name != "project.rf.yaml":
            emit("FAIL", "indexes/project.index.jsonl", "adapter-pointer", f"{key} must point to project.rf.yaml", findings)
        if any(part in value for part in FORBIDDEN_GLOBAL_PATH_PARTS):
            emit("FAIL", "indexes/project.index.jsonl", "private-path", f"{key} contains forbidden path {value}", findings)
        if adapter_mode == "legacy_shadow" and value and is_relative_to(Path(value), project_root):
            emit("FAIL", "indexes/project.index.jsonl", "legacy-pointer", f"{key} must not point inside legacy project root", findings)
    if Path(str(entry.get("path", ""))).resolve() != adapter.resolve():
        emit("FAIL", "indexes/project.index.jsonl", "adapter-pointer", "global path does not match adapter", findings)
    if Path(str(entry.get("adapter_path", ""))).resolve() != adapter.resolve():
        emit("FAIL", "indexes/project.index.jsonl", "adapter-pointer", "global adapter_path does not match adapter", findings)
    if Path(str(entry.get("project_root", ""))).resolve() != project_root.resolve():
        emit("FAIL", "indexes/project.index.jsonl", "project-root", "global project_root does not match adapter", findings)
    if entry.get("adapter_mode") not in {adapter_mode, None, ""}:
        emit("FAIL", "indexes/project.index.jsonl", "adapter-mode", "global adapter_mode does not match adapter", findings)
    if adapter_mode == "legacy_shadow" and entry.get("adapter_mode") != "legacy_shadow":
        emit("FAIL", "indexes/project.index.jsonl", "adapter-mode", "legacy pointer must set adapter_mode legacy_shadow", findings)
    if entry.get("fact_status") != "pointer":
        emit("FAIL", "indexes/project.index.jsonl", "pointer-only", "fact_status must be pointer", findings)
    boundary = entry.get("truth_boundary", {})
    if not isinstance(boundary, dict) or boundary.get("not_project_fact") is not True:
        emit("FAIL", "indexes/project.index.jsonl", "pointer-only", "truth_boundary.not_project_fact must be true", findings)
    return entry


def validate_adapter_mode(
    adapter: Path,
    framework_root: Path,
    project_root: Path,
    adapter_root: Path,
    adapter_mode: str,
    data: dict[str, Any],
    findings: list[tuple[str, str, str, str]],
) -> None:
    if adapter_mode not in ADAPTER_MODES:
        emit("FAIL", str(adapter), "adapter-mode", "adapter_mode must be native or legacy_shadow", findings)
        return

    expected_native_root = (project_root / ".researchflow").resolve()
    expected_legacy_parent = (framework_root / "project-interfaces" / "legacy").resolve()
    if adapter_mode == "native":
        if adapter_root.resolve() != expected_native_root:
            emit("FAIL", str(adapter), "adapter-root", "native adapter_root must be project_root/.researchflow", findings)
        if adapter.resolve() != (adapter_root / "project.rf.yaml").resolve():
            emit("FAIL", str(adapter), "adapter-root", "native adapter must be adapter_root/project.rf.yaml", findings)
        if data.get("sync", {}).get("authority") != "local_project":
            emit("FAIL", str(adapter), "sync", "native sync.authority must be local_project", findings)
        if data.get("write_policy", {}).get("writes_to_project") is not True:
            emit("FAIL", str(adapter), "write-policy", "native write_policy.writes_to_project must be true", findings)
    else:
        if not is_relative_to(adapter_root, expected_legacy_parent):
            emit("FAIL", str(adapter), "adapter-root", "legacy adapter_root must be under framework project-interfaces/legacy", findings)
        if is_relative_to(adapter_root, project_root):
            emit("FAIL", str(adapter), "adapter-root", "legacy adapter_root must not be inside project_root", findings)
        if adapter.resolve() != (adapter_root / "project.rf.yaml").resolve():
            emit("FAIL", str(adapter), "adapter-root", "legacy adapter must be adapter_root/project.rf.yaml", findings)
        if data.get("sync", {}).get("authority") != "researchflow_managed":
            emit("FAIL", str(adapter), "sync", "legacy sync.authority must be researchflow_managed", findings)
        if data.get("write_policy", {}).get("writes_to_project") is not False:
            emit("FAIL", str(adapter), "write-policy", "legacy write_policy.writes_to_project must be false", findings)
        if data.get("privacy", {}).get("writes_to_project_allowed") is not False:
            emit("FAIL", str(adapter), "privacy", "legacy privacy.writes_to_project_allowed must be false", findings)
        if not project_root.exists():
            emit("WARN", str(adapter), "project-root", "legacy project_root is currently unavailable", findings)

    if data.get("context_policy", {}).get("body_loading") != "explicit_reference_only":
        emit("FAIL", str(adapter), "context-policy", "context_policy.body_loading must be explicit_reference_only", findings)
    if data.get("context_policy", {}).get("forbid_deep_scan") is not True:
        emit("FAIL", str(adapter), "context-policy", "context_policy.forbid_deep_scan must be true", findings)
    if data.get("upgrade_policy", {}).get("proposal_required") is not True:
        emit("FAIL", str(adapter), "upgrade-policy", "upgrade_policy.proposal_required must be true", findings)
    if data.get("upgrade_policy", {}).get("auto_apply") is not False:
        emit("FAIL", str(adapter), "upgrade-policy", "upgrade_policy.auto_apply must be false", findings)
    if data.get("memory_policy", {}).get("apply_requires_review") is not True:
        emit("FAIL", str(adapter), "memory-policy", "memory_policy.apply_requires_review must be true", findings)


def validate_local_indexes(
    adapter_mode: str,
    project_root: Path,
    adapter_root: Path,
    adapter_data: dict[str, Any],
    findings: list[tuple[str, str, str, str]],
) -> dict[str, list[dict[str, Any]]]:
    local_indexes = adapter_data.get("paths", {}).get("local_indexes", {})
    loaded: dict[str, list[dict[str, Any]]] = {}
    for key in REQUIRED_LOCAL_INDEXES:
        if key not in local_indexes:
            emit("FAIL", "project.rf.yaml", "local-indexes", f"missing local index {key}", findings)
            continue
        path = resolve_declared_path(adapter_mode, project_root, adapter_root, str(local_indexes[key]))
        if adapter_mode == "legacy_shadow":
            if not is_relative_to(path, adapter_root):
                emit("FAIL", "project.rf.yaml", "local-indexes", f"{key} resolves outside adapter_root", findings)
            if is_relative_to(path, project_root):
                emit("FAIL", "project.rf.yaml", "local-indexes", f"{key} resolves inside legacy project_root", findings)
        loaded[key] = read_jsonl(path, findings)
    return loaded


def validate_metadata_paths(
    adapter_mode: str,
    project_root: Path,
    adapter_root: Path,
    adapter_data: dict[str, Any],
    findings: list[tuple[str, str, str, str]],
) -> None:
    if adapter_mode != "legacy_shadow":
        return
    checks = {
        "project_memory": str(adapter_data.get("paths", {}).get("project_memory", "")),
        "secrets_file": str(adapter_data.get("privacy", {}).get("secrets_file", "")),
    }
    for label, value in checks.items():
        if not value:
            emit("FAIL", "project.rf.yaml", "metadata-paths", f"{label} is required", findings)
            continue
        path = resolve_declared_path(adapter_mode, project_root, adapter_root, value)
        if not is_relative_to(path, adapter_root):
            emit("FAIL", "project.rf.yaml", "metadata-paths", f"{label} resolves outside adapter_root", findings)
        if is_relative_to(path, project_root):
            emit("FAIL", "project.rf.yaml", "metadata-paths", f"{label} resolves inside legacy project_root", findings)


def validate_procedure_chain(loaded: dict[str, list[dict[str, Any]]], findings: list[tuple[str, str, str, str]]) -> None:
    creative_ids = {entry.get("creative_pass_id") or entry.get("id") for entry in loaded.get("creative_passes", [])}
    golden = {}
    for entry in loaded.get("golden_runs", []):
        golden_id = entry.get("golden_run_id") or entry.get("id")
        golden[golden_id] = entry
        if entry.get("creative_pass_id") and entry.get("creative_pass_id") not in creative_ids:
            emit("FAIL", "golden-run.index.jsonl", "creative-pass-ref", "creative_pass_id not found", findings)

    procedures = {}
    for entry in loaded.get("procedures", []):
        proc_id = entry.get("procedure_id") or entry.get("id")
        procedures[proc_id] = entry
        status = entry.get("status")
        if status in {"approved", "active"}:
            source = entry.get("source_golden_run_id") or entry.get("derived_from_golden_run_id")
            if not source:
                emit("FAIL", "procedure.index.jsonl", "golden-run-ref", "approved procedure requires source_golden_run_id", findings)
            elif source not in golden:
                emit("FAIL", "procedure.index.jsonl", "golden-run-ref", "source_golden_run_id not found", findings)
        if entry.get("requires_human_creative_pass") is False:
            emit("FAIL", "procedure.index.jsonl", "human-pass", "requires_human_creative_pass must not be false", findings)
        if entry.get("agent_execution_policy") not in {"mechanical_only", None, ""}:
            emit("FAIL", "procedure.index.jsonl", "execution-policy", "agent_execution_policy must be mechanical_only", findings)

    done_keys = set()
    exceptions = {entry.get("exception_id") or entry.get("id"): entry for entry in loaded.get("exceptions", [])}
    for entry in loaded.get("repeat_runs", []):
        proc_id = entry.get("procedure_id")
        procedure = procedures.get(proc_id)
        if not procedure:
            emit("FAIL", "repeat-run.index.jsonl", "procedure-ref", "procedure not found", findings)
            continue
        if procedure.get("status") not in {"approved", "active"}:
            emit("FAIL", "repeat-run.index.jsonl", "procedure-status", "repeat-run requires approved procedure", findings)
        version = str(entry.get("procedure_version", ""))
        expected_version = str(procedure.get("procedure_version") or procedure.get("version") or "")
        if version != expected_version:
            emit("FAIL", "repeat-run.index.jsonl", "procedure-version", "procedure_version does not match procedure", findings)
        state = entry.get("state") or entry.get("status")
        if state == "done":
            missing = [field for field in ("digest_id", "claim_id", "review_decision") if not entry.get(field)]
            if missing:
                emit("FAIL", "repeat-run.index.jsonl", "done-evidence", "done repeat-run requires " + ", ".join(missing), findings)
            key = (proc_id, version, entry.get("dedupe_key"))
            if key in done_keys:
                emit("FAIL", "repeat-run.index.jsonl", "dedupe", "duplicate done repeat-run for procedure/version/dedupe_key", findings)
            done_keys.add(key)
        if state == "exception":
            exception_id = entry.get("exception_id")
            exception = exceptions.get(exception_id)
            if not exception:
                emit("FAIL", "repeat-run.index.jsonl", "exception-ref", "exception_id not found", findings)
            else:
                if not exception.get("route"):
                    emit("FAIL", "exception.index.jsonl", "exception-route", "exception requires route", findings)
                if not exception.get("human_question"):
                    emit("FAIL", "exception.index.jsonl", "exception-route", "exception requires human_question", findings)
                if exception.get("resolved") is not False:
                    emit("FAIL", "exception.index.jsonl", "exception-route", "new exception must start resolved false", findings)


def validate(adapter: Path, framework_root: Path, strict: bool) -> int:
    findings: list[tuple[str, str, str, str]] = []
    if not adapter.exists():
        emit("FAIL", str(adapter), "adapter", "adapter does not exist", findings)
    if not framework_root.exists():
        emit("FAIL", str(framework_root), "framework-root", "framework root does not exist", findings)
    if findings:
        return finish(findings, strict)

    data = parse_simple_yaml(adapter)
    project_id = str(data.get("project_id", ""))
    paths = data.get("paths", {})
    project_root = Path(str(paths.get("project_root", adapter.parents[1]))).resolve()
    adapter_mode = str(data.get("adapter_mode", ""))
    if not adapter_mode and adapter.resolve() == (project_root / ".researchflow" / "project.rf.yaml").resolve():
        adapter_mode = "native"
        emit("WARN", str(adapter), "adapter-mode", "adapter_mode missing; inferred native from legacy format", findings)
    adapter_root = Path(str(paths.get("adapter_root", adapter.parent))).resolve()

    if data.get("kind") != "project-adapter":
        emit("FAIL", str(adapter), "adapter", "kind must be project-adapter", findings)
    if not project_id.startswith("project:"):
        emit("FAIL", str(adapter), "project-id", "project_id must start with project:", findings)
    if str(data.get("framework", {}).get("root", "")) and Path(str(data["framework"]["root"])).resolve() != framework_root.resolve():
        emit("FAIL", str(adapter), "framework-root", "adapter framework.root mismatch", findings)
    if not paths.get("adapter_root"):
        emit("FAIL", str(adapter), "adapter-root", "paths.adapter_root is required", findings)
    validate_adapter_mode(adapter, framework_root, project_root, adapter_root, adapter_mode, data, findings)
    if data.get("privacy", {}).get("export_allowed") is not False:
        emit("WARN", str(adapter), "privacy", "privacy.export_allowed should be false", findings)

    validate_metadata_paths(adapter_mode, project_root, adapter_root, data, findings)
    loaded = validate_local_indexes(adapter_mode, project_root, adapter_root, data, findings)
    validate_global_pointer(framework_root, adapter, project_id, project_root, adapter_mode, findings)
    validate_procedure_chain(loaded, findings)
    return finish(findings, strict)


def finish(findings: list[tuple[str, str, str, str]], strict: bool) -> int:
    has_fail = any(level == "FAIL" for level, *_ in findings)
    has_warn = any(level == "WARN" for level, *_ in findings)
    if not findings:
        findings.append(("PASS", "project", "validation", "no issues found"))
    elif not has_fail:
        findings.append(("PASS", "project", "validation", "completed with warnings"))
    for level, path, rule, message in findings:
        print(f"{level} {path} {rule} {message}")
    return 1 if has_fail or (strict and has_warn) else 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate a connected ResearchFlow project.")
    parser.add_argument("project", nargs="?", help="Project root. If set, reads <project>/.researchflow/project.rf.yaml")
    parser.add_argument("--framework-root", required=True)
    parser.add_argument("--adapter")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)

    adapter = Path(args.adapter).resolve() if args.adapter else Path(args.project).resolve() / ".researchflow" / "project.rf.yaml"
    return validate(adapter, Path(args.framework_root).resolve(), args.strict)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
