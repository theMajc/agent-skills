<!-- BEGIN VERIFICATION MATRIX TEMPLATE -->
### Post-Generation Verification Report: `<target_function_name>`

#### 1. Function Overview
- **Function / Target:** `<module>.<function_name>` (lines `<start_line>-<end_line>`)
- **Language / Runtime:** `<language>` (e.g., TypeScript / Python / Go / Rust)
- **Primary Responsibility:** `<single sentence describing the function's contract>`

---

#### 2. Edge-Case Verification Checklist

One row per edge case actually relevant to *this* function's language, contract, and domain (see `SKILL.md` §2 for illustrative, non-exhaustive lenses) — add or omit rows freely; there is no fixed row count.

| Edge Case Category | Specific Scenario Tested | Handled? | Evidence / Line Ref | Falsifiable Justification & Notes |
| :--- | :--- | :---: | :--- | :--- |
| `<category derived from this function's actual failure surface>` | `<concrete scenario>` | `[Handled / Not Handled]` | `L<XX>-L<YY>` | `<One line explaining code guard or why missing>` |
| `<...>` | `<...>` | `[Handled / Not Handled]` | `L<XX>-L<YY>` | `<...>` |

---

#### 3. Verification Scorecard & Triage
- **Total Edge Cases Evaluated:** `<N — however many rows were actually relevant to this function>`
- **Handled (`Handled`):** `<Count>` (`<Percentage>%`)
- **Not Handled (`Not Handled`):** `<Count>` (`<Percentage>%`)
- **Critical Gaps Requiring Remediation:** `<Count>` (`<List of categories>`)
- **Acceptable Exclusions / Delegated Upstream:** `<Count>` (`<List of categories with justification>`)

---

#### 4. Remediation Code Patch (Required if Critical Gaps Exist)

*(If any critical gap is marked `Not Handled`, provide the exact replacement code or diff below. If all critical cases are handled or deferred, state "No immediate code patch required".)*

```<language>
// Example patch addressing unhandled edge cases:
// - Added guard clause for empty input
// - Added exponential backoff retry on HTTP 429
```

---

#### 5. Verification Verdict
- [ ] **VERIFIED (Ready for Production / Merge):** All critical edge cases handled with line-level evidence.
- [ ] **REMEDIATION REQUIRED:** Unhandled critical edge cases identified; apply recommended patch before merge.
- [ ] **ACCEPTED WITH EXCLUSIONS:** Unhandled items are non-critical and explicitly delegated to upstream layer / framework.

<!-- END VERIFICATION MATRIX TEMPLATE -->
