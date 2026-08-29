#!/usr/bin/env python3
"""
Verification test suite for terminal-output-compactor orchestrator.
Tests fallback scripts, RTK execution, TokenJuice integration, Repomix packaging,
and strict exit code propagation.
"""

import os
import subprocess
import tempfile
import unittest

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")

class TestCompactorOrchestrator(unittest.TestCase):

    def test_01_fallback_ansi_stripping(self):
        cmd = [
            "python3",
            os.path.join(SCRIPTS_DIR, "compact_fallback.py"),
            "--",
            "python3",
            "-c",
            "print('\\033[31mError:\\033[0m failed assertion')"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertNotIn("\x1B", res.stdout)
        self.assertIn("Error: failed assertion", res.stdout)

    def test_02_fallback_exit_code_propagation(self):
        cmd = [
            "python3",
            os.path.join(SCRIPTS_DIR, "compact_fallback.py"),
            "--",
            "python3",
            "-c",
            "import sys; sys.exit(42)"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 42)

    def test_03_fallback_test_failure_isolation(self):
        test_script = """
print('ok 1 - unit 1')
print('ok 2 - unit 2')
print('FAIL: test_auth_failure')
print('AssertionError: 401 != 200')
print('  at auth.spec.ts:42')
print('ok 3 - unit 3')
print('Tests: 2 passed, 1 failed')
"""
        cmd = [
            "python3",
            os.path.join(SCRIPTS_DIR, "compact_fallback.py"),
            "--test",
            "--",
            "python3",
            "-c",
            test_script
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("FAIL: test_auth_failure", res.stdout)
        self.assertIn("AssertionError: 401 != 200", res.stdout)
        self.assertIn("Tests: 2 passed, 1 failed", res.stdout)
        # passing test lines should be omitted
        self.assertNotIn("ok 1 - unit 1", res.stdout)

    def test_04_fallback_diff_lockfile_pruning(self):
        diff_text = """diff --git a/src/app.ts b/src/app.ts
--- a/src/app.ts
+++ b/src/app.ts
@@ -1 +1 @@
-console.log(1);
+console.log(2);
diff --git a/package-lock.json b/package-lock.json
--- a/package-lock.json
+++ b/package-lock.json
@@ -10,3 +10,4 @@
+  \"version\": \"2.0.0\"
"""
        cmd = [
            "python3",
            os.path.join(SCRIPTS_DIR, "compact_fallback.py"),
            "--diff",
            "--",
            "python3",
            "-c",
            f"print({repr(diff_text)})"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("src/app.ts", res.stdout)
        self.assertIn("[diff pruned: lockfile change b/package-lock.json]", res.stdout)

    def test_05_compact_run_rtk_execution(self):
        cmd = [
            os.path.join(SCRIPTS_DIR, "compact_run.sh"),
            "python3",
            "-c",
            "print('hello orchestrator')"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertTrue("hello orchestrator" in res.stdout or "Command completed successfully" in res.stdout)

    def test_06_compact_run_exit_code_forwarding(self):
        cmd = [
            os.path.join(SCRIPTS_DIR, "compact_run.sh"),
            "python3",
            "-c",
            "import sys; sys.exit(7)"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 7)

    def test_07_pack_context_repomix_execution(self):
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "index.ts"), "w") as f:
                f.write("export function isReady(): boolean { return true; }\n")
            output_xml = os.path.join(td, "context.xml")
            cmd = [
                os.path.join(SCRIPTS_DIR, "pack_context.sh"),
                "--dir", td,
                "--output", output_xml
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)
            self.assertTrue(os.path.exists(output_xml))
            with open(output_xml) as f:
                content = f.read()
            self.assertIn("export function isReady(): boolean", content)

    def test_08_transparent_hook_rewrite(self):
        import json
        payload = {"toolCall": {"name": "run_command", "args": {"CommandLine": "git status"}}}
        cmd = [
            "python3",
            os.path.join(SCRIPTS_DIR, "agy_hook_rewrite.py")
        ]
        res = subprocess.run(cmd, input=json.dumps(payload), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data.get("decision"), "allow")
        self.assertEqual(data.get("overwrite", {}).get("CommandLine"), "rtk git status")

    def test_09_ensure_rtk_idempotent(self):
        cmd = [os.path.join(SCRIPTS_DIR, "ensure_rtk.sh")]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
