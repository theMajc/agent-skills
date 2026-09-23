---
name: verify-ai-output
description: "Post-generation verification protocol for AI-generated code and functions. Produces a structured, falsifiable edge-case checklist distinguishing explicitly handled vs. unhandled cases — drawn from the target function's actual domain and contract, not a fixed generic list — with mandatory line-level justifications and remediation actions. Invocable via /verify."
user-invocable: true
triggers:
  - "/verify"
  - "verify-ai-output"
  - "verify"
  - "verify function"
  - "verify code"
---

# Verify AI Output (`verify-ai-output`)

Post-generation verification protocol for AI-generated code and functions. Converts subjective or invisible "mental checks" into an explicit, structured, and gradable verification artifact.

---

## 1. Core Philosophy & Invariants

When AI generates code, subtle edge cases are frequently overlooked or falsely assumed to be handled — and which edge cases matter depends entirely on what the function actually does. A string-formatting helper has nothing to do with HTTP 429s; a query builder cares about injection, not resource cleanup. The `/verify` skill enforces visible, falsifiable verification immediately following function generation, scoped to the function's real domain rather than a generic list applied by rote.

### Non-Negotiable Invariants

1. **Dual Handled vs. Not-Handled Columns (No Monolithic Pass/Fail)**
   - The output **must always separate** what is handled from what is unhandled into distinct columns (`Handled [✓]` vs `Not Handled [✗]`).
   - A single aggregate pass/fail line or subjective summary (e.g., "Looks good! Tests pass.") is strictly prohibited.

2. **Anti-Rubber-Stamp Invariant (Falsifiable Evidence)**
   - Every row in the checklist requires an explicit **one-line justification** referencing specific line numbers, code constructs, or conditions in the generated function.
   - If a condition is not explicitly guarded in code, it **must be marked as Not Handled**. Rubber-stamping ("all cases handled") without line-level proof is a protocol failure.

3. **Domain-Derived Scope, Not a Fixed List**
   - The set of edge cases checked is derived from *this* function — its language, its stated or inferred contract, its actual failure surface — not from a generic checklist applied uniformly regardless of what the code does. §2 gives illustrative lenses to jog thinking; it is a reminder, not a taxonomy to complete.
   - Applying an irrelevant category (e.g. probing rate-limit backoff on a pure in-memory sort) is itself a protocol failure — padding the report with inapplicable rows is as bad as missing an applicable one.

4. **Actionable Remediation**
   - For every edge case marked as **Not Handled**, the report must state whether it represents an acceptable design decision (e.g., delegated to upstream gateway) or a critical gap requiring an immediate code patch.

---

## 2. Illustrative Lenses (non-exhaustive — use judgment, not a checklist)

These are starting points to prime thinking about what could go wrong, grouped by the kind of function under review. Use whichever apply, ignore the ones that don't, and add categories that aren't listed here at all when the function's actual domain calls for them (SQL injection for a query builder, timezone/locale handling for a date function, Unicode normalization for a text parser, numerical stability for a scientific computation, and so on — the list of real domains is far longer than any table can hold).

| Function shape | Failure lenses worth checking |
|---|---|
| **Parses or validates external input** | Empty/null/malformed payloads, missing required fields, type coercion surprises, encoding issues. |
| **Deduplicates, upserts, or keys by identity** | Duplicate/repeated identifiers, key collisions, identity changing mid-stream. |
| **Calls a network service or external API** | Timeouts, rate limits (429)/5xx with retry-backoff, partial responses, connection drops. |
| **Does numeric or bounds-sensitive work** | Zero, negative, `MAX_INT`/overflow, off-by-one, floating-point precision. |
| **Runs concurrently or holds shared/mutable state** | Race conditions, non-atomic read-modify-write, mutable default arguments, deadlock/starvation. |
| **Acquires a resource (socket, file, connection, subprocess)** | Leak on the exception path, double-close, not guaranteed to release under cancellation. |
| **Anything else** | Whatever is actually specific to this function's contract — don't force it into the rows above if it doesn't belong there. |

---

## 3. Verification Workflow

When `/verify` is invoked on an AI-generated function or code snippet, follow this 5-step sequence:

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Function Identification & AST/Signature Inspection        │
│    - Extract signature, arguments, return type, side effects │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 2. Domain-Scoped Edge-Case Probing                           │
│    - Determine which failure lenses actually apply (§2)     │
│    - Add function-specific categories §2 doesn't cover       │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 3. Construct Dual-Column Verification Matrix                │
│    - Explicit Handled vs. Not Handled status                │
│    - Cite exact code lines and falsifiable justifications   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 4. Remediation Assessment                                   │
│    - Categorize unhandled gaps: [Critical] vs [Acceptable]  │
│    - Provide targeted code patch if critical gaps exist     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 5. Output Verification Report                               │
│    - Emit standardized Markdown table & summary metrics     │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Function Identification
Extract the target function's name, parameters, expected invariants, and external dependencies.

### Step 2: Domain-Scoped Edge-Case Probing
Read the function and decide, from what it actually does, which failure lenses in §2 apply — and what else applies that isn't in §2 at all. Then trace code paths against each one actually selected: guard clauses, deduplication/idempotency mechanisms, schema validation, retry/backoff logic, bounds checks, concurrency safety, resource cleanup, or whatever else is relevant to this function specifically.

### Step 3: Populate Verification Matrix
One row per edge case actually selected in Step 2 — however many that is. Assign either `Handled [✓]` or `Not Handled [✗]` for each, with a precise, single-sentence justification and code reference.

### Step 4: Remediation Plan
If any unhandled item poses runtime or data integrity risks, provide a minimal, non-breaking code diff fixing the gap.

### Step 5: Deliver Verification Report
Render the final output using the template format.

---

## 4. Output Template Specification

The verification output follows the shape in `templates/verification_matrix.md`: one row per edge case actually identified as relevant to the function under review (not a fixed row count), each with Category / Specific Edge Case / Status / Line-Ref / Justification, followed by summary metrics computed from however many rows actually exist:

```markdown
### Verification Matrix: `<function_name>`

| Category | Specific Edge Case | Status | Line / Ref | Justification & Evidence |
| :--- | :--- | :---: | :--- | :--- |
| **Empty Input** | `None` / `""` / `[]` | `Handled` | L4-L6 | Guard clause `if not records:` returns early with empty result. |
| **Duplicate ID** | Duplicate primary keys in payload | `Not Handled` | — | Overwrites existing dictionary key without deduplication or warning. |
| *(one row per edge case actually relevant to this function — add or omit rows freely)* | | | | |

#### Summary Metrics
- **Total Edge Cases Evaluated:** `<N — however many rows were actually relevant>`
- **Handled:** `<count> / <N>`
- **Not Handled:** `<count> / <N>`
- **Critical Unhandled Gaps:** `<count>` (`<list>`)

#### Remediation & Patch
[Include code patch or explicit rationale for deferred items]
```

---

## 5. Examples & References

- Complete Template: [`templates/verification_matrix.md`](templates/verification_matrix.md)
- Real-World Verification Example: [`examples/example_verification.md`](examples/example_verification.md)
