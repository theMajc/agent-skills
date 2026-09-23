<!-- BEGIN VERIFICATION MATRIX TEMPLATE -->
### Post-Generation Verification Report: `<target_function_name>`

#### 1. Function Overview
- **Function / Target:** `<module>.<function_name>` (lines `<start_line>-<end_line>`)
- **Language / Runtime:** `<language>` (e.g., TypeScript / Python / Go / Rust)
- **Primary Responsibility:** `<single sentence describing the function's contract>`

---

#### 2. Edge-Case Verification Checklist

| Edge Case Category | Specific Scenario Tested | Handled? | Evidence / Line Ref | Falsifiable Justification & Notes |
| :--- | :--- | :---: | :--- | :--- |
| **Empty / Null Input** | `None`, `null`, `""`, `[]`, `{}` | `[Handled / Not Handled]` | `L<XX>-L<YY>` | `<One line explaining code guard or why missing>` |
| **Duplicate Identifier** | Duplicate ID, repeated payload entry, replay request | `[Handled / Not Handled]` | `L<XX>-L<YY>` | `<One line explaining deduplication or vulnerability>` |
| **Malformed Record** | Missing required key, invalid data type, truncated payload | `[Handled / Not Handled]` | `L<XX>-L<YY>` | `<One line explaining schema validation or crash risk>` |
| **Rate Limit / 429 Backoff** | Downstream HTTP 429 / 503 / network throttling | `[Handled / Not Handled]` | `L<XX>-L<YY>` | `<One line explaining retry/backoff or unhandled error>` |
| **Boundary / Limits** | Numerical boundary (0, negative, MAX_INT), off-by-one, size limits | `[Handled / Not Handled]` | `L<XX>-L<YY>` | `<One line explaining bounds checking or overflow risk>` |
| **Concurrency & State** | Shared mutable state, async race conditions, non-atomic ops | `[Handled / Not Handled]` | `L<XX>-L<YY>` | `<One line explaining thread/async safety or data race>` |
| **Resource & Failure Modes** | Unhandled exception bubbling, unclosed file/socket descriptors | `[Handled / Not Handled]` | `L<XX>-L<YY>` | `<One line explaining cleanup block (try/finally, with) or leak>` |

---

#### 3. Verification Scorecard & Triage
- **Total Edge Cases Evaluated:** `<Total>`
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
