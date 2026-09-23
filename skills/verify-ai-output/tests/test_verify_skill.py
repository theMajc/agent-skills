#!/usr/bin/env python3
"""
Unit and validation test suite for verify-ai-output skill.
Validates SKILL.md frontmatter, taxonomy coverage, template contract,
anti-rubber-stamp invariants, and example consistency.
"""

import os
import re
import unittest

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_MD_PATH = os.path.join(SKILL_DIR, "SKILL.md")
TEMPLATE_PATH = os.path.join(SKILL_DIR, "templates", "verification_matrix.md")
EXAMPLE_PATH = os.path.join(SKILL_DIR, "examples", "example_verification.md")


class TestVerifyAiOutputSkill(unittest.TestCase):

    def setUp(self):
        self.assertTrue(os.path.exists(SKILL_MD_PATH), "SKILL.md must exist")
        with open(SKILL_MD_PATH, "r", encoding="utf-8") as f:
            self.skill_content = f.read()

        self.assertTrue(os.path.exists(TEMPLATE_PATH), "Template must exist")
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            self.template_content = f.read()

        self.assertTrue(os.path.exists(EXAMPLE_PATH), "Example must exist")
        with open(EXAMPLE_PATH, "r", encoding="utf-8") as f:
            self.example_content = f.read()

    def test_01_yaml_frontmatter(self):
        """SKILL.md must contain valid frontmatter with name and triggers."""
        self.assertTrue(self.skill_content.startswith("---"))
        frontmatter_match = re.search(r"^---\n(.*?)\n---", self.skill_content, re.DOTALL)
        self.assertIsNotNone(frontmatter_match, "Valid YAML frontmatter required")
        frontmatter = frontmatter_match.group(1)
        self.assertIn("name: verify-ai-output", frontmatter)
        self.assertIn("/verify", frontmatter)
        self.assertIn("user-invocable: true", frontmatter)

    def test_02_mandatory_taxonomy_coverage(self):
        """Skill and template must cover all core edge-case taxonomy categories."""
        required_categories = [
            "Empty",
            "Duplicate",
            "Malformed",
            "429",
            "Boundary",
            "Concurrency",
        ]
        for category in required_categories:
            self.assertIn(
                category.lower(),
                self.skill_content.lower(),
                f"SKILL.md must cover taxonomy category: {category}"
            )
            self.assertIn(
                category.lower(),
                self.template_content.lower(),
                f"Template must cover taxonomy category: {category}"
            )

    def test_03_anti_rubber_stamp_invariant(self):
        """Must require both Handled and Not Handled states, rejecting single pass/fail."""
        self.assertIn("Handled", self.template_content)
        self.assertIn("Not Handled", self.template_content)
        self.assertIn("Justification", self.template_content)
        # Verify SKILL.md explicitly forbids single pass/fail
        self.assertIn("pass/fail", self.skill_content.lower())

    def test_04_example_conformance(self):
        """Example must demonstrate real evaluation with both handled and not-handled rows."""
        self.assertIn("Handled", self.example_content)
        self.assertIn("Not Handled", self.example_content)
        self.assertIn("Critical Gaps Requiring Remediation", self.example_content)
        self.assertIn("Remediation Code Patch", self.example_content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
