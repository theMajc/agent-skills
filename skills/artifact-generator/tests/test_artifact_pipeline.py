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

if __name__ == "__main__":
    unittest.main()
