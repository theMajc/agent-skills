#!/usr/bin/env python3
"""
Unit and validation test suite for verify-ai-output skill.
Validates SKILL.md frontmatter, domain-scoped (non-fixed) edge-case guidance,
template contract, anti-rubber-stamp invariants, and example consistency.
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

    def test_02_scope_is_domain_derived_not_fixed(self):
        """Skill must explicitly scope edge-case selection to the function under
        review rather than mandate a fixed universal category list — this is
        the specific defect the skill was overhauled to fix (MIRA-108 feedback:
        a hardcoded taxonomy narrows a frontier model's judgment instead of
        directing it)."""
        lowered = self.skill_content.lower()
        self.assertIn("non-exhaustive", lowered)
        self.assertIn("judgment", lowered)
        # Must not claim the lens table is mandatory/complete
        self.assertNotIn("universal edge-case taxonomy", lowered)
        self.assertNotIn("mandatory taxonomy", lowered)
        # Must explicitly warn against forcing inapplicable categories
        self.assertIn("irrelevant", lowered)

    def test_03_template_has_no_fixed_row_count(self):
        """Template must not hardcode a fixed 7-row / 7-category structure —
        row count and categories must be derived per-function."""
        self.assertNotIn("Total Edge Cases Evaluated:** `<Total>`", self.template_content)
        self.assertIn("however many rows", self.template_content.lower())

    def test_04_anti_rubber_stamp_invariant(self):
        """Must require both Handled and Not Handled states, rejecting single pass/fail."""
        self.assertIn("Handled", self.template_content)
        self.assertIn("Not Handled", self.template_content)
        self.assertIn("Justification", self.template_content)
        # Verify SKILL.md explicitly forbids single pass/fail
        self.assertIn("pass/fail", self.skill_content.lower())

    def test_05_example_conformance(self):
        """Example must demonstrate real evaluation with both handled and not-handled
        rows, and must explain why its categories were chosen rather than presenting
        them as a fixed universal set."""
        self.assertIn("Handled", self.example_content)
        self.assertIn("Not Handled", self.example_content)
        self.assertIn("Critical Gaps Requiring Remediation", self.example_content)
        self.assertIn("Remediation Code Patch", self.example_content)
        self.assertIn("not the fixed set", self.example_content.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
