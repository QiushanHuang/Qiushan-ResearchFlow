#!/usr/bin/env python3
"""Lightweight ResearchFlow validator."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_RULES = {
    "common_index_required": [
        "schema_version",
        "id",
        "kind",
        "title",
        "status",
        "path",
        "created_at",
        "updated_at",
        "checksum",
        "read_policy",
    ],
    "read_policies": ["index_only", "on_demand", "adapter_first", "registry_only", "skip"],
    "fact_statuses": ["pointer", "candidate", "observed", "verified", "stale", "conflict"],
    "memory_target_layers": ["project", "bridge", "universal"],
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RELEASE_MARKER_RE = re.compile(r"\b(TODO|TBD|FIXME)\b")
HYGIENE_DIRS = {
    "commands",
    "framework",
    "skills",
    "prompts",
    "templates",
    "evolution",
    "skills-registry",
}


@dataclass
class Finding:
    level: str
    path: str
    rule: str
    message: str

    def line(self) -> str:
        return f"{self.level} {self.path} {self.rule} {self.message}"


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
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value.replace("'", '"'))
        except json.JSONDecodeError:
            return value
    try:
        return int(value)
    except ValueError:
        return value.strip('"').strip("'")


def load_simple_rules(root: Path) -> dict[str, Any]:
    rules = {key: list(value) if isinstance(value, list) else value for key, value in DEFAULT_RULES.items()}
    path = root / "framework" / "validation-rules.yaml"
    if not path.exists():
        return rules

    current_key: str | None = None
    current_map_key: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if indent == 0 and line.endswith(":"):
            current_key = line[:-1]
            current_map_key = None
            rules[current_key] = []
            continue
        if indent == 0 and ":" in line:
            key, value = line.split(":", 1)
            rules[key.strip()] = parse_scalar(value)
            current_key = key.strip()
            current_map_key = None
            continue
        if current_key and line.startswith("- "):
            if not isinstance(rules.get(current_key), list):
                rules[current_key] = []
            rules[current_key].append(parse_scalar(line[2:]))
            continue
        if current_key and ":" in line:
            if not isinstance(rules.get(current_key), dict):
                rules[current_key] = {}
            key, value = line.split(":", 1)
            rules[current_key][key.strip()] = parse_scalar(value)
            current_map_key = key.strip()
            continue
        if current_key and current_map_key and line.startswith("- "):
            bucket = rules[current_key].setdefault(current_map_key, [])
            if isinstance(bucket, list):
                bucket.append(parse_scalar(line[2:]))
    return rules


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def add(findings: list[Finding], level: str, path: str, rule: str, message: str) -> None:
    findings.append(Finding(level, path, rule, message))


def is_boundary_kind(kind: str) -> bool:
    return (
        "external-library" in kind
        or kind.startswith("rss")
        or kind.startswith("evolution-")
        or kind in {"project-link", "project-link-index"}
    )


def path_exists(root: Path, entry_path: str) -> bool:
    if "://" in entry_path:
        return True
    return (root / entry_path).exists()


def validate_index_entry(
    root: Path,
    file_path: Path,
    entry: dict[str, Any],
    rules: dict[str, Any],
    project_ids: set[str],
    findings: list[Finding],
) -> None:
    path_label = rel(root, file_path)
    required = rules.get("common_index_required", DEFAULT_RULES["common_index_required"])
    missing = [field for field in required if field not in entry]
    if missing:
        add(findings, "FAIL", path_label, "required-fields", "missing " + ", ".join(missing))
        return

    kind = str(entry.get("kind", ""))
    read_policy = entry.get("read_policy")
    if read_policy not in rules.get("read_policies", DEFAULT_RULES["read_policies"]):
        add(findings, "FAIL", path_label, "read-policy", f"invalid read_policy {read_policy!r}")

    for field in ("created_at", "updated_at"):
        value = str(entry.get(field, ""))
        if value and not DATE_RE.match(value):
            add(findings, "FAIL", path_label, "date-format", f"{field} must be YYYY-MM-DD")

    entry_path = str(entry.get("path", ""))
    if not entry_path:
        add(findings, "FAIL", path_label, "path", "path must not be empty")
    elif not path_exists(root, entry_path):
        add(findings, "WARN", path_label, "path", f"path does not exist: {entry_path}")

    if is_boundary_kind(kind):
        for field in ("fact_status", "truth_boundary"):
            if field not in entry:
                add(findings, "FAIL", path_label, "boundary", f"missing {field}")
        if entry.get("fact_status") and entry.get("fact_status") not in rules.get(
            "fact_statuses", DEFAULT_RULES["fact_statuses"]
        ):
            add(findings, "FAIL", path_label, "boundary", "invalid fact_status")
        if entry.get("project_fact") is True:
            add(findings, "FAIL", path_label, "boundary", "boundary entry cannot set project_fact true")
        if kind.startswith(("external-library", "rss", "evolution-", "project-link")):
            if entry.get("not_project_fact") is not True:
                add(findings, "FAIL", path_label, "boundary", "not_project_fact must be true")

    if kind == "evolution-candidate":
        if entry.get("requires_review") is not True:
            add(findings, "FAIL", path_label, "candidate", "requires_review must be true")
        if entry.get("requires_human_confirmation") is not True:
            add(findings, "FAIL", path_label, "candidate", "requires_human_confirmation must be true")
        if entry.get("apply_allowed") is True:
            add(findings, "FAIL", path_label, "candidate", "apply_allowed must not be true")

    if kind.startswith("evolution-") and entry.get("status") == "resolved":
        if not entry.get("resolution_evidence"):
            add(findings, "FAIL", path_label, "evolution-resolution", "resolved status requires resolution_evidence")

    if kind == "project-link":
        for field in ("from_project_id", "to_project_id", "link_type", "fact_policy", "evidence_refs"):
            if field not in entry:
                add(findings, "FAIL", path_label, "project-link", f"missing {field}")
        if entry.get("fact_policy") != "not_project_fact":
            add(findings, "FAIL", path_label, "project-link", "fact_policy must be not_project_fact")
        if entry.get("fact_transfer_allowed") is not False:
            add(findings, "FAIL", path_label, "project-link", "fact_transfer_allowed must be false")
        for field in ("from_project_id", "to_project_id"):
            if entry.get(field) not in project_ids:
                add(findings, "WARN", path_label, "project-link", f"{field} not found in project.index.jsonl")

    if kind == "compute-resource":
        for field in ("access", "location", "cpu_cores", "memory_gb", "suitable_tasks"):
            if field not in entry:
                add(findings, "FAIL", path_label, "compute-resource", f"missing {field}")
        if entry.get("auto_execute_allowed") is True:
            add(findings, "FAIL", path_label, "compute-resource", "auto_execute_allowed must not be true")
        if entry.get("score_only") is not True:
            add(findings, "FAIL", path_label, "compute-resource", "score_only must be true")

    if kind == "storage-location":
        for field in ("path", "storage_type", "capacity_gb", "location", "mounted_on"):
            if field not in entry:
                add(findings, "FAIL", path_label, "storage-location", f"missing {field}")

    if kind == "task-route":
        if entry.get("assignment_policy") != "manual_confirm":
            add(findings, "FAIL", path_label, "task-route", "assignment_policy must be manual_confirm")
        requires = entry.get("requires", {})
        if isinstance(requires, dict):
            for field, value in requires.items():
                if field.endswith("_min") and not isinstance(value, (int, float)):
                    add(findings, "FAIL", path_label, "task-route", f"{field} must be numeric")

    if kind == "codex-skill":
        for field in ("skill_name", "trigger_summary", "source_root", "skill_path", "recommended_for"):
            if field not in entry:
                add(findings, "FAIL", path_label, "codex-skill", f"missing {field}")

    if kind == "skill-usage":
        for field in (
            "skill_ids",
            "project_id",
            "project_path",
            "researchflow_project_entry",
            "usage_scope",
            "task_type",
            "used_at",
            "outcome",
        ):
            if field not in entry:
                add(findings, "FAIL", path_label, "skill-usage", f"missing {field}")


def collect_project_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    path = root / "indexes" / "project.index.jsonl"
    if not path.exists():
        return ids
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "id" in entry:
            ids.add(entry["id"])
    return ids


def validate_indexes(root: Path, rules: dict[str, Any], findings: list[Finding]) -> None:
    indexes = root / "indexes"
    if not indexes.exists():
        add(findings, "FAIL", "indexes", "missing", "indexes directory does not exist")
        return

    project_ids = collect_project_ids(root)
    for file_path in sorted(indexes.glob("*.jsonl")):
        seen: set[str] = set()
        for lineno, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as exc:
                add(findings, "FAIL", rel(root, file_path), "jsonl", f"line {lineno}: {exc.msg}")
                continue
            entry_id = entry.get("id")
            if entry_id in seen:
                add(findings, "FAIL", rel(root, file_path), "duplicate-id", f"duplicate id {entry_id}")
            if entry_id:
                seen.add(entry_id)
            validate_index_entry(root, file_path, entry, rules, project_ids, findings)


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].splitlines()
    body = text[end + 4 :]
    data: dict[str, Any] = {}
    current_key: str | None = None
    for line in raw:
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            data[current_key].append(parse_scalar(line[4:]))
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            current_key = key.strip()
            data[current_key] = parse_scalar(value)
    return data, body


def has_section(body: str, title: str) -> bool:
    pattern = re.compile(rf"^##\s+{re.escape(title)}\s*$", re.MULTILINE)
    return bool(pattern.search(body))


def section_text(body: str, title: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(title)}\s*$", re.MULTILINE)
    match = pattern.search(body)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^##\s+", body[start:], re.MULTILINE)
    end = start + next_match.start() if next_match else len(body)
    return body[start:end].strip()


def validate_sections(path_label: str, body: str, required: list[str], findings: list[Finding], rule: str) -> None:
    for section in required:
        if not has_section(body, section):
            add(findings, "FAIL", path_label, rule, f"missing section {section}")


def validate_markdown(root: Path, rules: dict[str, Any], findings: list[Finding]) -> None:
    for path in sorted(root.rglob("*.md")):
        rel_path = rel(root, path)
        if rel_path.startswith("templates/"):
            continue
        text = path.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(text)
        if not frontmatter:
            continue

        kind = str(frontmatter.get("kind", ""))
        if frontmatter.get("claim_id"):
            for field in ("schema_version", "claim_id", "claim_status", "created_at"):
                if field not in frontmatter:
                    add(findings, "FAIL", rel_path, "claim-frontmatter", f"missing {field}")
            validate_sections(
                rel_path,
                body,
                ["Claim", "Evidence", "Scope", "Verification", "Residual Risk", "Not Done"],
                findings,
                "claim-sections",
            )
            if frontmatter.get("claim_status") not in {"draft", "", None} and not section_text(body, "Evidence"):
                add(findings, "FAIL", rel_path, "claim-evidence", "non-draft claim needs Evidence content")

        if frontmatter.get("digest_id"):
            for field in ("digest_id", "status", "created_at", "updated_at"):
                if field not in frontmatter:
                    add(findings, "FAIL", rel_path, "digest-frontmatter", f"missing {field}")
            validate_sections(
                rel_path,
                body,
                ["Question", "Setup Summary", "Observed Result", "Limitations", "Artifact Links", "Reproducibility", "Candidate Claims"],
                findings,
                "digest-sections",
            )

        if frontmatter.get("proposal_id"):
            if frontmatter.get("status") != "proposed":
                add(findings, "FAIL", rel_path, "memory-proposal", "status must be proposed")
            if frontmatter.get("requires_human_confirmation") is not True:
                add(findings, "FAIL", rel_path, "memory-proposal", "requires_human_confirmation must be true")
            if frontmatter.get("target_layer") not in rules.get(
                "memory_target_layers", DEFAULT_RULES["memory_target_layers"]
            ):
                add(findings, "FAIL", rel_path, "memory-proposal", "target_layer must be project, bridge, or universal")
            validate_sections(
                rel_path,
                body,
                ["Source Evidence", "Scope", "Confidence", "Invalidates On"],
                findings,
                "memory-proposal-sections",
            )

        if kind == "evolution-candidate" and frontmatter.get("apply_allowed") is True:
            add(findings, "FAIL", rel_path, "candidate", "apply_allowed must not be true")

        if kind == "evolution-inbox":
            validate_sections(
                rel_path,
                body,
                ["Raw Signal", "Normalized Intent"],
                findings,
                "evolution-inbox-sections",
            )

        if kind == "evolution-resolution" and frontmatter.get("resolution_status") == "resolved":
            if not section_text(body, "Resolution Evidence"):
                add(findings, "FAIL", rel_path, "evolution-resolution", "resolved status requires Resolution Evidence")

        if frontmatter.get("source_type") == "external_library":
            if frontmatter.get("not_project_fact") is not True:
                add(findings, "FAIL", rel_path, "library-source", "not_project_fact must be true")
            if "truth_boundary" not in frontmatter:
                add(findings, "FAIL", rel_path, "library-source", "missing truth_boundary")


def validate_release_hygiene(root: Path, findings: list[Finding]) -> None:
    for directory in HYGIENE_DIRS:
        base = root / directory
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml", ".json", ".jsonl"}:
                continue
            text = path.read_text(encoding="utf-8")
            match = RELEASE_MARKER_RE.search(text)
            if match:
                add(findings, "FAIL", rel(root, path), "release-marker", f"contains {match.group(1)}")


def validate_rf_yaml_policy(root: Path, findings: list[Finding]) -> None:
    path = root / "rf.yaml"
    if not path.exists():
        return
    in_default_read = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent == 0:
            in_default_read = stripped == "default_read:"
            continue
        if in_default_read and stripped.startswith("- ") and "prompts/" in stripped[2:]:
            add(findings, "FAIL", "rf.yaml", "prompt-default-read", "prompts must not be in default_read")


def run(root: Path, strict: bool) -> int:
    findings: list[Finding] = []
    rules = load_simple_rules(root)
    validate_indexes(root, rules, findings)
    validate_markdown(root, rules, findings)
    validate_release_hygiene(root, findings)
    validate_rf_yaml_policy(root, findings)

    has_fail = any(item.level == "FAIL" for item in findings)
    has_warn = any(item.level == "WARN" for item in findings)
    if not findings:
        add(findings, "PASS", str(root), "validation", "no issues found")
    elif not has_fail:
        add(findings, "PASS", str(root), "validation", "completed with warnings")

    for item in findings:
        print(item.line())

    if has_fail or (strict and has_warn):
        return 1
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate a ResearchFlow framework tree.")
    parser.add_argument("root", help="Path to agent-framework/researchflow")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        print(f"FAIL {root} args root directory does not exist", file=sys.stderr)
        return 2
    return run(root, args.strict)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
