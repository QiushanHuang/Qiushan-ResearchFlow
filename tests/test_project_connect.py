import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONNECT = PROJECT_ROOT / "scripts" / "rf_project_connect.py"
VALIDATE = PROJECT_ROOT / "scripts" / "rf_project_validate.py"


def run_script(script, *args):
    return subprocess.run(
        [sys.executable, str(script), *map(str, args)],
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def snapshot_tree(root):
    return sorted(
        (
            str(path.relative_to(root)),
            path.is_dir(),
            path.stat().st_size if path.is_file() else 0,
        )
        for path in root.rglob("*")
    )


class ProjectConnectTests(unittest.TestCase):
    def make_framework(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name) / "researchflow"
        (root / "indexes").mkdir(parents=True)
        (root / "indexes" / "project.index.jsonl").write_text("", encoding="utf-8")
        self.addCleanup(tmp.cleanup)
        return root.resolve()

    def make_project(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name) / "project"
        root.mkdir()
        self.addCleanup(tmp.cleanup)
        return root.resolve()

    def test_connect_creates_adapter_tree_and_pointer(self):
        framework = self.make_framework()
        project = self.make_project()

        result = run_script(
            CONNECT,
            "--framework-root",
            framework,
            "--project-root",
            project,
            "--project-id",
            "project:demo",
            "--title",
            "Demo Project",
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((project / ".researchflow" / "project.rf.yaml").exists())
        self.assertTrue((project / ".researchflow" / "memory" / "project.md").exists())
        self.assertTrue((project / ".researchflow" / "local.private.yaml.example").exists())
        for name in [
            "task.index.jsonl",
            "knowledge.index.jsonl",
            "artifact.index.jsonl",
            "experiment.index.jsonl",
            "creative-pass.index.jsonl",
            "golden-run.index.jsonl",
            "procedure.index.jsonl",
            "repeat-run.index.jsonl",
            "exception.index.jsonl",
        ]:
            self.assertTrue((project / ".researchflow" / "indexes" / name).exists(), name)
        pointer = read_jsonl(framework / "indexes" / "project.index.jsonl")[0]
        self.assertEqual(pointer["id"], "project:demo")
        self.assertEqual(pointer["kind"], "project")
        self.assertTrue(pointer["path"].endswith(".researchflow/project.rf.yaml"))
        self.assertEqual(pointer["fact_status"], "pointer")
        self.assertTrue(pointer["truth_boundary"]["not_project_fact"])

    def test_legacy_connect_creates_shadow_adapter_without_touching_project(self):
        framework = self.make_framework()
        project = self.make_project()
        (project / "existing.txt").write_text("keep", encoding="utf-8")
        before = snapshot_tree(project)

        result = run_script(
            CONNECT,
            "--mode",
            "legacy",
            "--framework-root",
            framework,
            "--project-root",
            project,
            "--project-id",
            "project:legacy-demo",
            "--title",
            "Legacy Demo",
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((project / ".researchflow").exists())
        self.assertEqual((project / "existing.txt").read_text(encoding="utf-8"), "keep")
        self.assertEqual(snapshot_tree(project), before)

        shadow = framework / "project-interfaces" / "legacy" / "project-legacy-demo"
        adapter = shadow / "project.rf.yaml"
        self.assertTrue(adapter.exists())
        self.assertTrue((shadow / "memory" / "project.md").exists())
        self.assertTrue((shadow / "skills" / "usage.index.jsonl").exists())
        adapter_text = adapter.read_text(encoding="utf-8")
        self.assertIn("adapter_mode: legacy_shadow", adapter_text)
        self.assertIn(f"  project_root: {project}", adapter_text)
        self.assertIn(f"  adapter_root: {shadow}", adapter_text)

        pointer = read_jsonl(framework / "indexes" / "project.index.jsonl")[0]
        self.assertEqual(pointer["id"], "project:legacy-demo")
        self.assertEqual(pointer["adapter_mode"], "legacy_shadow")
        self.assertEqual(Path(pointer["adapter_path"]), adapter)
        self.assertEqual(Path(pointer["project_root"]), project)

    def test_legacy_connected_project_validates(self):
        framework = self.make_framework()
        project = self.make_project()
        connect = run_script(
            CONNECT,
            "--mode",
            "legacy",
            "--framework-root",
            framework,
            "--project-root",
            project,
            "--project-id",
            "project:legacy-demo",
            "--title",
            "Legacy Demo",
        )
        adapter = framework / "project-interfaces" / "legacy" / "project-legacy-demo" / "project.rf.yaml"
        validate = run_script(VALIDATE, "--framework-root", framework, "--adapter", adapter, "--strict")

        self.assertEqual(connect.returncode, 0, connect.stdout + connect.stderr)
        self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)
        self.assertIn("PASS", validate.stdout)

    def test_legacy_existing_shadow_adapter_fails(self):
        framework = self.make_framework()
        project = self.make_project()
        first = run_script(
            CONNECT,
            "--mode",
            "legacy",
            "--framework-root",
            framework,
            "--project-root",
            project,
            "--project-id",
            "project:legacy-demo",
            "--title",
            "Legacy Demo",
        )
        second = run_script(
            CONNECT,
            "--mode",
            "legacy",
            "--framework-root",
            framework,
            "--project-root",
            project,
            "--project-id",
            "project:legacy-demo-2",
            "--title",
            "Legacy Demo 2",
        )

        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertNotEqual(second.returncode, 0)
        self.assertIn("project root already registered", second.stdout + second.stderr)

    def test_duplicate_project_id_fails(self):
        framework = self.make_framework()
        project_a = self.make_project()
        project_b = self.make_project()
        first = run_script(CONNECT, "--framework-root", framework, "--project-root", project_a, "--project-id", "project:demo", "--title", "Demo")
        second = run_script(CONNECT, "--framework-root", framework, "--project-root", project_b, "--project-id", "project:demo", "--title", "Demo 2")

        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertNotEqual(second.returncode, 0)
        self.assertIn("duplicate project_id", second.stdout + second.stderr)

    def test_existing_adapter_fails(self):
        framework = self.make_framework()
        project = self.make_project()
        (project / ".researchflow").mkdir()
        (project / ".researchflow" / "project.rf.yaml").write_text("schema_version: 1\n", encoding="utf-8")

        result = run_script(CONNECT, "--framework-root", framework, "--project-root", project, "--project-id", "project:demo", "--title", "Demo")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already exists", result.stdout + result.stderr)

    def test_validate_connected_project_passes(self):
        framework = self.make_framework()
        project = self.make_project()
        connect = run_script(CONNECT, "--framework-root", framework, "--project-root", project, "--project-id", "project:demo", "--title", "Demo")
        validate = run_script(VALIDATE, "--framework-root", framework, "--adapter", project / ".researchflow" / "project.rf.yaml", "--strict")

        self.assertEqual(connect.returncode, 0, connect.stdout + connect.stderr)
        self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)
        self.assertIn("PASS", validate.stdout)

    def test_global_pointer_forbidden_fields_fail(self):
        framework = self.make_framework()
        project = self.make_project()
        run_script(CONNECT, "--framework-root", framework, "--project-root", project, "--project-id", "project:demo", "--title", "Demo")
        pointer_path = framework / "indexes" / "project.index.jsonl"
        entry = read_jsonl(pointer_path)[0]
        entry["memory"] = "leak"
        pointer_path.write_text(json.dumps(entry) + "\n", encoding="utf-8")

        result = run_script(VALIDATE, "--framework-root", framework, "--adapter", project / ".researchflow" / "project.rf.yaml")

        self.assertEqual(result.returncode, 1)
        self.assertIn("forbidden global project field", result.stdout)

    def test_adapter_auto_apply_true_fails(self):
        framework = self.make_framework()
        project = self.make_project()
        run_script(CONNECT, "--framework-root", framework, "--project-root", project, "--project-id", "project:demo", "--title", "Demo")
        adapter = project / ".researchflow" / "project.rf.yaml"
        text = adapter.read_text(encoding="utf-8").replace("  auto_apply: false", "  auto_apply: true")
        adapter.write_text(text, encoding="utf-8")

        result = run_script(VALIDATE, "--framework-root", framework, "--adapter", adapter)

        self.assertEqual(result.returncode, 1)
        self.assertIn("upgrade_policy.auto_apply", result.stdout)

    def test_legacy_adapter_root_inside_project_fails(self):
        framework = self.make_framework()
        project = self.make_project()
        run_script(
            CONNECT,
            "--mode",
            "legacy",
            "--framework-root",
            framework,
            "--project-root",
            project,
            "--project-id",
            "project:legacy-demo",
            "--title",
            "Legacy Demo",
        )
        adapter = framework / "project-interfaces" / "legacy" / "project-legacy-demo" / "project.rf.yaml"
        shadow = framework / "project-interfaces" / "legacy" / "project-legacy-demo"
        text = adapter.read_text(encoding="utf-8").replace(f"  adapter_root: {shadow}", f"  adapter_root: {project}")
        adapter.write_text(text, encoding="utf-8")

        result = run_script(VALIDATE, "--framework-root", framework, "--adapter", adapter)

        self.assertEqual(result.returncode, 1)
        self.assertIn("legacy adapter_root must be under", result.stdout)

    def test_legacy_project_memory_inside_project_fails(self):
        framework = self.make_framework()
        project = self.make_project()
        run_script(
            CONNECT,
            "--mode",
            "legacy",
            "--framework-root",
            framework,
            "--project-root",
            project,
            "--project-id",
            "project:legacy-demo",
            "--title",
            "Legacy Demo",
        )
        adapter = framework / "project-interfaces" / "legacy" / "project-legacy-demo" / "project.rf.yaml"
        text = adapter.read_text(encoding="utf-8").replace(
            "  project_memory: memory/project.md",
            f"  project_memory: {project / 'memory.md'}",
        )
        adapter.write_text(text, encoding="utf-8")

        result = run_script(VALIDATE, "--framework-root", framework, "--adapter", adapter)

        self.assertEqual(result.returncode, 1)
        self.assertIn("project_memory resolves inside legacy project_root", result.stdout)

    def test_legacy_secrets_file_inside_project_fails(self):
        framework = self.make_framework()
        project = self.make_project()
        run_script(
            CONNECT,
            "--mode",
            "legacy",
            "--framework-root",
            framework,
            "--project-root",
            project,
            "--project-id",
            "project:legacy-demo",
            "--title",
            "Legacy Demo",
        )
        adapter = framework / "project-interfaces" / "legacy" / "project-legacy-demo" / "project.rf.yaml"
        text = adapter.read_text(encoding="utf-8").replace(
            "  secrets_file: local.private.yaml",
            f"  secrets_file: {project / 'local.private.yaml'}",
        )
        adapter.write_text(text, encoding="utf-8")

        result = run_script(VALIDATE, "--framework-root", framework, "--adapter", adapter)

        self.assertEqual(result.returncode, 1)
        self.assertIn("secrets_file resolves inside legacy project_root", result.stdout)

    def test_active_procedure_without_golden_run_fails(self):
        framework = self.make_framework()
        project = self.make_project()
        run_script(CONNECT, "--framework-root", framework, "--project-root", project, "--project-id", "project:demo", "--title", "Demo")
        procedure = {
            "schema_version": 1,
            "id": "procedure:bad",
            "kind": "procedure",
            "title": "Bad procedure",
            "status": "approved",
            "path": ".researchflow/procedures/bad.md",
            "created_at": "2026-05-30",
            "updated_at": "2026-05-30",
            "checksum": "",
            "read_policy": "index_only",
            "project_id": "project:demo",
            "procedure_id": "procedure:bad",
            "procedure_version": "1",
            "requires_human_creative_pass": True,
            "agent_execution_policy": "mechanical_only",
            "exception_route": "needs_user",
        }
        (project / ".researchflow" / "indexes" / "procedure.index.jsonl").write_text(json.dumps(procedure) + "\n", encoding="utf-8")

        result = run_script(VALIDATE, "--framework-root", framework, "--adapter", project / ".researchflow" / "project.rf.yaml")

        self.assertEqual(result.returncode, 1)
        self.assertIn("source_golden_run_id", result.stdout)

    def test_repeat_run_unknown_procedure_fails(self):
        framework = self.make_framework()
        project = self.make_project()
        run_script(CONNECT, "--framework-root", framework, "--project-root", project, "--project-id", "project:demo", "--title", "Demo")
        repeat = {
            "schema_version": 1,
            "id": "repeat:bad",
            "kind": "repeat-run",
            "title": "Bad repeat",
            "status": "executed",
            "path": ".researchflow/repeat/bad.md",
            "created_at": "2026-05-30",
            "updated_at": "2026-05-30",
            "checksum": "",
            "read_policy": "index_only",
            "project_id": "project:demo",
            "repeat_run_id": "repeat:bad",
            "procedure_id": "procedure:missing",
            "procedure_version": "1",
            "dedupe_key": "same",
        }
        (project / ".researchflow" / "indexes" / "repeat-run.index.jsonl").write_text(json.dumps(repeat) + "\n", encoding="utf-8")

        result = run_script(VALIDATE, "--framework-root", framework, "--adapter", project / ".researchflow" / "project.rf.yaml")

        self.assertEqual(result.returncode, 1)
        self.assertIn("procedure not found", result.stdout)

    def test_done_repeat_run_requires_digest_claim_review(self):
        framework = self.make_framework()
        project = self.make_project()
        run_script(CONNECT, "--framework-root", framework, "--project-root", project, "--project-id", "project:demo", "--title", "Demo")
        golden = {
            "schema_version": 1,
            "id": "golden:ok",
            "kind": "golden-run",
            "title": "Golden",
            "status": "passed",
            "path": ".researchflow/golden/ok.md",
            "created_at": "2026-05-30",
            "updated_at": "2026-05-30",
            "checksum": "",
            "read_policy": "index_only",
            "project_id": "project:demo",
            "golden_run_id": "golden:ok",
            "creative_pass_id": "creative:ok",
        }
        procedure = {
            "schema_version": 1,
            "id": "procedure:ok",
            "kind": "procedure",
            "title": "Procedure",
            "status": "approved",
            "path": ".researchflow/procedures/ok.md",
            "created_at": "2026-05-30",
            "updated_at": "2026-05-30",
            "checksum": "",
            "read_policy": "index_only",
            "project_id": "project:demo",
            "procedure_id": "procedure:ok",
            "procedure_version": "1",
            "source_golden_run_id": "golden:ok",
            "requires_human_creative_pass": True,
            "agent_execution_policy": "mechanical_only",
            "exception_route": "needs_user",
        }
        repeat = {
            "schema_version": 1,
            "id": "repeat:bad",
            "kind": "repeat-run",
            "title": "Repeat",
            "status": "done",
            "path": ".researchflow/repeat/bad.md",
            "created_at": "2026-05-30",
            "updated_at": "2026-05-30",
            "checksum": "",
            "read_policy": "index_only",
            "project_id": "project:demo",
            "repeat_run_id": "repeat:bad",
            "procedure_id": "procedure:ok",
            "procedure_version": "1",
            "dedupe_key": "same",
        }
        (project / ".researchflow" / "indexes" / "golden-run.index.jsonl").write_text(json.dumps(golden) + "\n", encoding="utf-8")
        (project / ".researchflow" / "indexes" / "procedure.index.jsonl").write_text(json.dumps(procedure) + "\n", encoding="utf-8")
        (project / ".researchflow" / "indexes" / "repeat-run.index.jsonl").write_text(json.dumps(repeat) + "\n", encoding="utf-8")

        result = run_script(VALIDATE, "--framework-root", framework, "--adapter", project / ".researchflow" / "project.rf.yaml")

        self.assertEqual(result.returncode, 1)
        self.assertIn("done repeat-run requires", result.stdout)


if __name__ == "__main__":
    unittest.main()
