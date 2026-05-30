#!/usr/bin/env python3
"""Connect a project to ResearchFlow with native or legacy-shadow adapters."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


LOCAL_INDEXES = {
    "tasks": "task.index.jsonl",
    "knowledge": "knowledge.index.jsonl",
    "artifacts": "artifact.index.jsonl",
    "experiments": "experiment.index.jsonl",
    "creative_passes": "creative-pass.index.jsonl",
    "golden_runs": "golden-run.index.jsonl",
    "procedures": "procedure.index.jsonl",
    "repeat_runs": "repeat-run.index.jsonl",
    "exceptions": "exception.index.jsonl",
}

MODE_TO_ADAPTER_MODE = {
    "native": "native",
    "legacy": "legacy_shadow",
}


def fail(message: str) -> int:
    print(f"FAIL {message}", file=sys.stderr)
    return 1


def load_project_entries(project_index: Path) -> list[dict]:
    if not project_index.exists():
        return []
    entries = []
    for line in project_index.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entries.append(json.loads(line))
    return entries


def safe_project_slug(project_id: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", project_id).strip(".-")
    if not slug or slug in {".", ".."} or ".." in slug:
        raise ValueError("project-id cannot produce a safe adapter slug")
    return slug


def is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def yaml_path(path: Path) -> str:
    return str(path)


def yaml_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def local_index_value(adapter_mode: str, filename: str) -> str:
    if adapter_mode == "native":
        return f".researchflow/indexes/{filename}"
    return f"indexes/{filename}"


def project_memory_value(adapter_mode: str) -> str:
    if adapter_mode == "native":
        return ".researchflow/memory/project.md"
    return "memory/project.md"


def secrets_value(adapter_mode: str) -> str:
    if adapter_mode == "native":
        return ".researchflow/local.private.yaml"
    return "local.private.yaml"


def skill_usage_value(adapter_mode: str) -> str:
    if adapter_mode == "native":
        return ".researchflow/skills/usage.index.jsonl"
    return "skills/usage.index.jsonl"


def write_adapter(
    path: Path,
    framework_root: Path,
    project_root: Path,
    adapter_root: Path,
    project_id: str,
    title: str,
    adapter_mode: str,
) -> None:
    writes_to_project = "true" if adapter_mode == "native" else "false"
    sync_authority = "local_project" if adapter_mode == "native" else "researchflow_managed"
    context_default = "adapter_first" if adapter_mode == "native" else "index_first"
    allowed_root = ".researchflow/**" if adapter_mode == "native" else f"{adapter_root}/**"
    lines = [
        "schema_version: 1",
        "kind: project-adapter",
        f"adapter_mode: {adapter_mode}",
        f"project_id: {yaml_scalar(project_id)}",
        f"title: {yaml_scalar(title)}",
        "status: active",
        "",
        "framework:",
        f"  root: {yaml_path(framework_root)}",
        f"  project_index_id: {project_id}",
        "",
        "paths:",
        f"  project_root: {yaml_path(project_root)}",
        f"  adapter_root: {yaml_path(adapter_root)}",
        f"  project_memory: {project_memory_value(adapter_mode)}",
        "  local_indexes:",
    ]
    for key, filename in LOCAL_INDEXES.items():
        lines.append(f"    {key}: {local_index_value(adapter_mode, filename)}")
    lines.extend(
        [
            f"    skill_usage: {skill_usage_value(adapter_mode)}",
            "",
            "execution_policy:",
            "  human_role: creative_judgment",
            "  agent_role: mechanical_execution",
            "  identity_boundary: agent_executes_not_represents_identity",
            "  procedure_state_model: use_existing_researchflow_state_machine",
            "  exception_route: needs_user",
            "",
            "write_policy:",
            f"  writes_to_project: {writes_to_project}",
            "  allowed_roots:",
            f"    - {allowed_root}",
            "",
            "context_policy:",
            f"  default: {context_default}",
            "  body_loading: explicit_reference_only",
            "  forbid_deep_scan: true",
            "",
            "memory_policy:",
            "  habit_learning_requires_evidence_chain: true",
            "  project_to_universal_requires_bridge: true",
            "  apply_requires_review: true",
            "",
            "upgrade_policy:",
            "  proposal_required: true",
            "  auto_apply: false",
            "",
            "golden_run:",
            "  default_id:",
            "  selection_policy: approved_only",
            "",
            "sync:",
            f"  authority: {sync_authority}",
            "  adapter_revision: 1",
            "  last_synced_at:",
            "  global_revision_seen:",
            "",
            "privacy:",
            "  export_allowed: false",
            "  contains_private_data: true",
            "  writes_to_project_allowed: false" if adapter_mode == "legacy_shadow" else "  writes_to_project_allowed: true",
            f"  secrets_file: {secrets_value(adapter_mode)}",
            "",
            "read_policy:",
            f"  default: {context_default}",
            "  skip_by_default:",
            "    - logs/**",
            "    - raw/**",
            "    - artifacts/**",
            "    - .git/**",
            "    - node_modules/**",
            "    - .venv/**",
            '    - "*.ckpt"',
            '    - "*.npy"',
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def append_project_pointer(
    project_index: Path,
    adapter_path: Path,
    project_root: Path,
    project_id: str,
    title: str,
    adapter_mode: str,
) -> None:
    today = date.today().isoformat()
    entry = {
        "schema_version": 1,
        "id": project_id,
        "kind": "project",
        "title": title,
        "status": "active",
        "path": str(adapter_path),
        "created_at": today,
        "updated_at": today,
        "checksum": "",
        "read_policy": "adapter_first",
        "adapter_mode": adapter_mode,
        "adapter_path": str(adapter_path),
        "project_root": str(project_root),
        "fact_status": "pointer",
        "truth_boundary": {"not_project_fact": True, "source": "project-adapter"},
    }
    with project_index.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def create_adapter_tree(root: Path) -> None:
    (root / "indexes").mkdir(parents=True)
    (root / "memory").mkdir(parents=True)
    (root / "skills").mkdir(parents=True)
    (root / "procedures").mkdir(parents=True)
    (root / "golden-runs").mkdir(parents=True)
    (root / "repeat-runs").mkdir(parents=True)
    (root / "exceptions").mkdir(parents=True)
    for filename in LOCAL_INDEXES.values():
        (root / "indexes" / filename).write_text("", encoding="utf-8")
    (root / "skills" / "usage.index.jsonl").write_text("", encoding="utf-8")


def write_project_memory(root: Path, project_id: str) -> None:
    (root / "memory" / "project.md").write_text(
        f"---\nschema_version: 1\nproject_id: {project_id}\nkind: project-memory\nstatus: active\nread_policy: on_demand\n---\n\n# Project Memory\n\n",
        encoding="utf-8",
    )


def write_private_example(root: Path) -> None:
    (root / "local.private.yaml.example").write_text(
        "schema_version: 1\nkind: local-private\n# Copy to local.private.yaml and do not commit real secrets.\n",
        encoding="utf-8",
    )


def verify_unique_registration(entries: list[dict], project_id: str, project_root: Path) -> int | None:
    for entry in entries:
        if entry.get("id") == project_id:
            return fail(f"duplicate project_id: {project_id}")
        if Path(str(entry.get("project_root", ""))).resolve() == project_root:
            return fail(f"project root already registered: {project_root}")
    return None


def connect_native(framework_root: Path, project_root: Path, project_id: str, title: str, project_index: Path) -> int:
    adapter_root = project_root / ".researchflow"
    adapter = adapter_root / "project.rf.yaml"
    if adapter.exists():
        return fail(f"adapter already exists: {adapter}")
    create_adapter_tree(adapter_root)
    write_project_memory(adapter_root, project_id)
    write_private_example(adapter_root)
    write_adapter(adapter, framework_root, project_root, adapter_root, project_id, title, "native")
    append_project_pointer(project_index, adapter, project_root, project_id, title, "native")
    print("PASS mode native")
    print(f"PASS connected {project_id} at {project_root}")
    print(f"PASS adapter {adapter}")
    return 0


def connect_legacy(framework_root: Path, project_root: Path, project_id: str, title: str, project_index: Path) -> int:
    if (project_root / ".researchflow").exists():
        return fail(f"legacy mode requires no existing project .researchflow: {project_root / '.researchflow'}")
    try:
        slug = safe_project_slug(project_id)
    except ValueError as exc:
        return fail(str(exc))
    adapter_root = framework_root / "project-interfaces" / "legacy" / slug
    adapter = adapter_root / "project.rf.yaml"
    if adapter.exists():
        return fail(f"adapter already exists: {adapter}")
    if is_relative_to(adapter_root, project_root):
        return fail("legacy adapter root must not be inside project root")

    create_adapter_tree(adapter_root)
    write_project_memory(adapter_root, project_id)
    write_private_example(adapter_root)
    write_adapter(adapter, framework_root, project_root, adapter_root, project_id, title, "legacy_shadow")
    append_project_pointer(project_index, adapter, project_root, project_id, title, "legacy_shadow")
    print("PASS mode legacy")
    print(f"PASS connected {project_id} at {project_root}")
    print(f"PASS adapter {adapter}")
    print(f"PASS no-touch project root {project_root}")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Connect a project to ResearchFlow.")
    parser.add_argument("--mode", choices=sorted(MODE_TO_ADAPTER_MODE), default="native")
    parser.add_argument("--framework-root", required=True)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args(argv)

    framework_root = Path(args.framework_root).resolve()
    project_root = Path(args.project_root).resolve()
    if not framework_root.exists():
        return fail(f"framework root does not exist: {framework_root}")
    project_index = framework_root / "indexes" / "project.index.jsonl"
    if not project_index.exists():
        return fail(f"missing project index: {project_index}")
    if not project_root.exists():
        return fail(f"project root does not exist: {project_root}")
    if not args.project_id.startswith("project:"):
        return fail("project-id must start with project:")

    entries = load_project_entries(project_index)
    duplicate = verify_unique_registration(entries, args.project_id, project_root)
    if duplicate is not None:
        return duplicate

    if args.mode == "native":
        return connect_native(framework_root, project_root, args.project_id, args.title, project_index)
    return connect_legacy(framework_root, project_root, args.project_id, args.title, project_index)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
