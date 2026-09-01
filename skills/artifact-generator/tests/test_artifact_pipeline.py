#!/usr/bin/env python3
"""
Test Suite for Dynamic Artifact Generator Skill
Verifies PDF, SVG, and HTML generation across all audience presets.
"""

import os
import sys
import subprocess
import unittest
import shutil

class TestArtifactPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.abspath("scratch/test_dist")
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)
        os.makedirs(cls.test_dir, exist_ok=True)

        cls.script_path = os.path.abspath("agent-skills/skills/artifact-generator/scripts/render_artifact.py")
        cls.data_path = os.path.abspath("agent-skills/skills/artifact-generator/examples/resume_data.json")

    def run_generator(self, preset, fmt="all"):
        cmd = [
            sys.executable,
            self.script_path,
            "--data", self.data_path,
            "--preset", preset,
            "--format", fmt,
            "--output-dir", self.test_dir
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Generator failed for preset {preset}:\n{res.stderr}")

    def test_01_executive_preset(self):
        self.run_generator("executive", "all")
        pdf_path = os.path.join(self.test_dir, "artifact_executive.pdf")
        html_path = os.path.join(self.test_dir, "artifact_executive_web.html")
        svg_path = os.path.join(self.test_dir, "artifact_executive_page_1.svg")

        self.assertTrue(os.path.exists(pdf_path), "Executive PDF not found")
        self.assertTrue(os.path.exists(html_path), "Executive HTML not found")
        self.assertTrue(os.path.exists(svg_path), "Executive SVG Page 1 not found")

        with open(pdf_path, "rb") as f:
            header = f.read(5)
            self.assertEqual(header, b"%PDF-", "Invalid PDF magic header")

    def test_02_technical_preset(self):
        self.run_generator("technical", "pdf")
        pdf_path = os.path.join(self.test_dir, "artifact_technical.pdf")
        self.assertTrue(os.path.exists(pdf_path), "Technical PDF not found")
        self.assertGreater(os.path.getsize(pdf_path), 20000, "Technical PDF unexpectedly small")

    def test_03_graphically_rich_preset(self):
        self.run_generator("graphically_rich", "pdf")
        pdf_path = os.path.join(self.test_dir, "artifact_graphically_rich.pdf")
        self.assertTrue(os.path.exists(pdf_path), "Graphically rich PDF not found")
        self.assertGreater(os.path.getsize(pdf_path), 20000, "Graphic PDF unexpectedly small")

    def test_04_ats_text_extraction(self):
        # Verify text readability
        try:
            from pypdf import PdfReader
            pdf_path = os.path.join(self.test_dir, "artifact_executive.pdf")
            reader = PdfReader(pdf_path)
            extracted = "".join(p.extract_text() for p in reader.pages)
            self.assertIn("Alex Mercer", extracted)
            self.assertIn("Nexus Autonomous Systems", extracted)
            self.assertIn("Distributed Systems", extracted)
        except ImportError:
            pass

    def test_05_reproducible_determinism(self):
        import hashlib
        dir1 = os.path.join(self.test_dir, "det1")
        dir2 = os.path.join(self.test_dir, "det2")

        cmd1 = [sys.executable, self.script_path, "--data", self.data_path, "--preset", "executive", "--format", "pdf", "--deterministic", "--output-dir", dir1]
        cmd2 = [sys.executable, self.script_path, "--data", self.data_path, "--preset", "executive", "--format", "pdf", "--deterministic", "--output-dir", dir2]

        subprocess.run(cmd1, check=True, capture_output=True)
        subprocess.run(cmd2, check=True, capture_output=True)

        pdf1 = os.path.join(dir1, "artifact_executive.pdf")
        pdf2 = os.path.join(dir2, "artifact_executive.pdf")

        with open(pdf1, "rb") as f1, open(pdf2, "rb") as f2:
            hash1 = hashlib.sha256(f1.read()).hexdigest()
            hash2 = hashlib.sha256(f2.read()).hexdigest()

        self.assertEqual(hash1, hash2, "Deterministic PDF generation failed: SHA256 hashes do not match")

if __name__ == "__main__":
    unittest.main()
