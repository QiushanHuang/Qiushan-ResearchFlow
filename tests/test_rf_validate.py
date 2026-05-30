import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "rf_validate.py"


def write_jsonl(path, entries):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def base_entry(**overrides):
    entry = {
        "schema_version": 1,
        "id": "idx:valid",
        "kind": "library-index",
        "title": "Valid index",
        "status": "active",
        "path": "library/",
        "created_at": "2026-05-30",
        "updated_at": "2026-05-30",
        "checksum": "",
        "read_policy": "index_only",
    }
    entry.update(overrides)
    return entry


class RFValidateTests(unittest.TestCase):
    def run_validator(self, root, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(root), *args],
            cwd=PROJECT_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def with_root(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        (root / "indexes").mkdir(parents=True)
        (root / "library").mkdir()
        self.addCleanup(tmp.cleanup)
        return root

    def test_valid_index_passes(self):
        root = self.with_root()
        write_jsonl(root / "indexes" / "library.index.jsonl", [base_entry()])

        result = self.run_validator(root)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_bad_jsonl_fails(self):
        root = self.with_root()
        bad = root / "indexes" / "bad.index.jsonl"
        bad.write_text('{"id": "broken"\n', encoding="utf-8")

        result = self.run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL", result.stdout)

    def test_missing_required_field_fails(self):
        root = self.with_root()
        entry = base_entry()
        del entry["read_policy"]
        write_jsonl(root / "indexes" / "missing.index.jsonl", [entry])

        result = self.run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("read_policy", result.stdout)

    def test_duplicate_id_fails(self):
        root = self.with_root()
        write_jsonl(root / "indexes" / "dupe.index.jsonl", [base_entry(), base_entry()])

        result = self.run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate id", result.stdout)

    def test_external_library_requires_boundary(self):
        root = self.with_root()
        entry = base_entry(kind="external-library-source", id="src:bad")
        write_jsonl(root / "indexes" / "library.index.jsonl", [entry])

        result = self.run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("truth_boundary", result.stdout)

    def test_missing_path_warns_and_strict_fails(self):
        root = self.with_root()
        write_jsonl(
            root / "indexes" / "path.index.jsonl",
            [base_entry(id="idx:missing-path", path="missing/path")],
        )

        normal = self.run_validator(root)
        strict = self.run_validator(root, "--strict")

        self.assertEqual(normal.returncode, 0, normal.stdout + normal.stderr)
        self.assertIn("WARN", normal.stdout)
        self.assertEqual(strict.returncode, 1)

    def test_unsafe_memory_proposal_fails(self):
        root = self.with_root()
        (root / "memory" / "proposals").mkdir(parents=True)
        (root / "memory" / "proposals" / "bad.md").write_text(
            """---
schema_version: 1
proposal_id: mem-bad
target_layer: global
status: proposed
requires_human_confirmation: false
created_at: 2026-05-30
---

# Memory Proposal

## Proposed Memory

## Source Evidence

## Scope

## Confidence

## Invalidates On
""",
            encoding="utf-8",
        )
        write_jsonl(root / "indexes" / "ok.index.jsonl", [base_entry()])

        result = self.run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("requires_human_confirmation", result.stdout)

    def test_candidate_cannot_apply(self):
        root = self.with_root()
        entry = base_entry(
            id="evo:candidate",
            kind="evolution-candidate",
            title="Unsafe candidate",
            path="evolution/candidates/bad.md",
            fact_status="candidate",
            truth_boundary="signal_not_fact",
            requires_review=True,
            apply_allowed=True,
        )
        (root / "evolution" / "candidates").mkdir(parents=True)
        (root / "evolution" / "candidates" / "bad.md").write_text("", encoding="utf-8")
        write_jsonl(root / "indexes" / "evolution.candidate.index.jsonl", [entry])

        result = self.run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("apply_allowed", result.stdout)

    def test_resource_cannot_auto_execute(self):
        root = self.with_root()
        entry = base_entry(
            id="resource:bad",
            kind="compute-resource",
            title="Unsafe resource",
            path="resources/compute/bad.md",
            access="ssh:bad",
            location="lab",
            cpu_cores=64,
            memory_gb=256,
            suitable_tasks=["simulation"],
            score_only=True,
            auto_execute_allowed=True,
        )
        (root / "resources" / "compute").mkdir(parents=True)
        (root / "resources" / "compute" / "bad.md").write_text("", encoding="utf-8")
        write_jsonl(root / "indexes" / "resource.index.jsonl", [entry])

        result = self.run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("auto_execute_allowed", result.stdout)

    def test_evolution_inbox_requires_normalized_intent(self):
        root = self.with_root()
        (root / "evolution" / "inbox").mkdir(parents=True)
        (root / "evolution" / "inbox" / "bad.md").write_text(
            """---
schema_version: 1
id: evo-inbox-bad
kind: evolution-inbox
status: captured
created_at: 2026-05-30
updated_at: 2026-05-30
source: user
read_policy: on_demand
---

# Evolution Inbox

## Raw Signal

Messy original user input.
""",
            encoding="utf-8",
        )
        write_jsonl(root / "indexes" / "ok.index.jsonl", [base_entry()])

        result = self.run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("Normalized Intent", result.stdout)

    def test_reusable_actions_define_five_pass_subagent_review(self):
        actions = PROJECT_ROOT / "commands" / "reusable-actions.md"
        command = PROJECT_ROOT / "commands" / "subagent-five-pass-review.md"

        text = actions.read_text(encoding="utf-8")

        self.assertIn("rf_subagent_five_pass_review", text)
        self.assertIn("commands/subagent-five-pass-review.md", text)
        self.assertTrue(command.exists())

    def test_codex_skill_entry_requires_trigger_metadata(self):
        root = self.with_root()
        entry = base_entry(
            id="skill:bad",
            kind="codex-skill",
            title="Bad skill",
            path="skills-registry/inventory/bad.md",
        )
        (root / "skills-registry" / "inventory").mkdir(parents=True)
        (root / "skills-registry" / "inventory" / "bad.md").write_text("", encoding="utf-8")
        write_jsonl(root / "indexes" / "skill.index.jsonl", [entry])

        result = self.run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("trigger_summary", result.stdout)

    def test_skill_usage_entry_requires_project_context(self):
        root = self.with_root()
        entry = base_entry(
            id="skill-usage:bad",
            kind="skill-usage",
            title="Bad skill usage",
            path="skills-registry/usage/bad.md",
            skill_ids=["skill:rf-intake-router"],
        )
        (root / "skills-registry" / "usage").mkdir(parents=True)
        (root / "skills-registry" / "usage" / "bad.md").write_text("", encoding="utf-8")
        write_jsonl(root / "indexes" / "skill-usage.index.jsonl", [entry])

        result = self.run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("project_id", result.stdout)

    def test_skill_management_module_exists(self):
        expected = [
            PROJECT_ROOT / "skills-registry" / "README.md",
            PROJECT_ROOT / "skills-registry" / "inventory" / "codex-available-2026-05-30.md",
            PROJECT_ROOT / "commands" / "skill-inventory.md",
            PROJECT_ROOT / "commands" / "skill-usage-log.md",
            PROJECT_ROOT / "indexes" / "skill.index.jsonl",
            PROJECT_ROOT / "indexes" / "skill-usage.index.jsonl",
            PROJECT_ROOT / "skills" / "rf-skill-governance" / "SKILL.md",
        ]

        missing = [str(path) for path in expected if not path.exists()]

        self.assertEqual(missing, [])

    def test_philosophy_policy_module_exists(self):
        expected = [
            PROJECT_ROOT / "framework" / "philosophy.md",
            PROJECT_ROOT / "framework" / "boundaries.md",
            PROJECT_ROOT / "framework" / "habit-learning.md",
        ]
        missing = [str(path) for path in expected if not path.exists()]

        self.assertEqual(missing, [])

    def test_safe_identity_and_habit_policies_are_required(self):
        rf_yaml = (PROJECT_ROOT / "rf.yaml").read_text(encoding="utf-8")

        self.assertIn("creative_policy:", rf_yaml)
        self.assertIn("human_creative_authority: true", rf_yaml)
        self.assertIn("agent_mechanical_execution: true", rf_yaml)
        self.assertIn("representation_policy:", rf_yaml)
        self.assertIn("impersonation_allowed: false", rf_yaml)
        self.assertIn("external_commitment_requires_explicit_confirmation: true", rf_yaml)
        self.assertIn("habit_learning_policy:", rf_yaml)
        self.assertIn("single_observation_to_universal_memory_allowed: false", rf_yaml)

    def test_state_machine_does_not_add_repeat_run_states(self):
        state_machine = (PROJECT_ROOT / "framework" / "state-machine.md").read_text(encoding="utf-8")

        forbidden = ["REPEAT_RUN", "DELEGATING", "AUTO_EXECUTING"]
        for marker in forbidden:
            self.assertNotIn(marker, state_machine)

    def test_project_adapter_declares_repeat_procedure_indexes(self):
        adapter = (PROJECT_ROOT / "templates" / "project-adapter.rf.yaml").read_text(encoding="utf-8")

        for key in ["creative_passes", "golden_runs", "procedures", "repeat_runs", "exceptions"]:
            self.assertIn(key + ":", adapter)

    def test_project_interface_skills_and_prompts_exist(self):
        expected = [
            PROJECT_ROOT / "skills" / "rf-project-interface-router" / "SKILL.md",
            PROJECT_ROOT / "skills" / "rf-project-native-onboarding" / "SKILL.md",
            PROJECT_ROOT / "skills" / "rf-project-legacy-onboarding" / "SKILL.md",
            PROJECT_ROOT / "commands" / "project-interface.md",
            PROJECT_ROOT / "prompts" / "project-interface" / "native-new-project.md",
            PROJECT_ROOT / "prompts" / "project-interface" / "legacy-shadow-project.md",
            PROJECT_ROOT / "prompts" / "project-interface" / "natural-language-connect.md",
            PROJECT_ROOT / "prompts" / "project-interface" / "first-run-golden-procedure.md",
            PROJECT_ROOT / "prompts" / "project-interface" / "skill-retrospective.md",
            PROJECT_ROOT / "templates" / "first-run-golden-procedure.md",
        ]

        missing = [str(path) for path in expected if not path.exists()]

        self.assertEqual(missing, [])
        self.assertFalse((PROJECT_ROOT / "skills" / "rf-project-first-run-capture").exists())

    def test_project_connect_command_documents_native_and_legacy_modes(self):
        command = (PROJECT_ROOT / "commands" / "project-connect.md").read_text(encoding="utf-8")
        interface = (PROJECT_ROOT / "commands" / "project-interface.md").read_text(encoding="utf-8")

        self.assertIn("--mode native", command)
        self.assertIn("--mode legacy", command)
        self.assertIn("project-interfaces/legacy", command)
        self.assertIn("rf_project_native_connect", interface)
        self.assertIn("rf_project_legacy_connect", interface)

    def test_project_interface_supports_natural_language_entry(self):
        interface = (PROJECT_ROOT / "commands" / "project-interface.md").read_text(encoding="utf-8")
        prompt = (PROJECT_ROOT / "prompts" / "project-interface" / "natural-language-connect.md").read_text(encoding="utf-8")
        router = (PROJECT_ROOT / "skills" / "rf-project-interface-router" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("Natural Language Entry", interface)
        self.assertIn("The user should not need to run shell commands", interface)
        self.assertIn("agent runs the connect and validate scripts", interface)
        self.assertIn("I want to connect this project to ResearchFlow", prompt)
        self.assertIn("Do not ask the user to run commands", router)

    def test_public_documentation_surface_exists(self):
        expected = [
            PROJECT_ROOT / "docs" / "README.md",
            PROJECT_ROOT / "docs" / "user-manual.md",
            PROJECT_ROOT / "docs" / "technical-manual.md",
            PROJECT_ROOT / "docs" / "local-public-sync.md",
            PROJECT_ROOT / "indexes" / "documentation.index.jsonl",
        ]

        missing = [str(path) for path in expected if not path.exists()]
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        rf_yaml = (PROJECT_ROOT / "rf.yaml").read_text(encoding="utf-8")
        sync_manual = (PROJECT_ROOT / "docs" / "local-public-sync.md").read_text(encoding="utf-8")

        self.assertEqual(missing, [])
        self.assertIn("docs/user-manual.md", readme)
        self.assertIn("docs/technical-manual.md", readme)
        self.assertIn("docs/local-public-sync.md", readme)
        self.assertIn("Connect the current project to ResearchFlow. This project may create .researchflow", readme)
        self.assertIn("把当前项目接入 ResearchFlow。这个项目可以创建 .researchflow", readme)
        self.assertIn("https://img.shields.io/static/v1?label=workflow", readme)
        self.assertIn("## Philosophy", readme)
        self.assertIn("## 理念", readme)
        self.assertNotIn("**Language:**", readme)
        self.assertNotIn("**语言切换：**", readme)
        self.assertNotIn("Agent Philosophy", readme)
        self.assertNotIn("Agent 理念", readme)
        self.assertNotIn("Agent Workflow", readme)
        self.assertNotIn("privacy-sanitized", readme)
        self.assertNotIn("context-index--first", readme)
        self.assertIn("documentation: indexes/documentation.index.jsonl", rf_yaml)
        self.assertIn("PUBLIC-SYNC", sync_manual)
        self.assertIn("LOCAL-PRIVATE", sync_manual)

    def test_release_markers_fail_in_docs(self):
        root = self.with_root()
        (root / "commands").mkdir()
        (root / "commands" / "bad.md").write_text("Ship blocker: TODO marker\n", encoding="utf-8")
        write_jsonl(root / "indexes" / "ok.index.jsonl", [base_entry()])

        result = self.run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("release-marker", result.stdout)

    def test_rf_yaml_default_read_cannot_include_prompts(self):
        root = self.with_root()
        (root / "rf.yaml").write_text(
            """schema_version: 1
default_read:
  - README.md
  - prompts/project-interface/native-new-project.md
""",
            encoding="utf-8",
        )
        write_jsonl(root / "indexes" / "ok.index.jsonl", [base_entry()])

        result = self.run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("prompt-default-read", result.stdout)


if __name__ == "__main__":
    unittest.main()
