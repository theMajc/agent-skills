---
name: verify-ai-output
description: "Post-generation verification protocol for AI-generated code and functions. Produces a structured, falsifiable edge-case checklist distinguishing explicitly handled vs. unhandled cases (empty inputs, duplicates, malformed payloads, rate limits/backoff, boundaries, concurrency) with mandatory line-level justifications and remediation actions. Invocable via /verify."
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

When AI generates code, subtle edge cases (e.g., malformed payloads, duplicate keys, transient rate limits, boundary inputs) are frequently overlooked or falsely assumed to be handled. The `/verify` skill enforces visible, falsifiable verification immediately following function generation.

### Non-Negotiable Invariants

1. **Dual Handled vs. Not-Handled Columns (No Monolithic Pass/Fail)**
   - The output **must always separate** what is handled from what is unhandled into distinct columns (`Handled [✓]` vs `Not Handled [✗]`).
   - A single aggregate pass/fail line or subjective summary (e.g., "Looks good! Tests pass.") is strictly prohibited.

2. **Anti-Rubber-Stamp Invariant (Falsifiable Evidence)**
   - Every row in the checklist requires an explicit **one-line justification** referencing specific line numbers, code constructs, or conditions in the generated function.
   - If a condition is not explicitly guarded in code, it **must be marked as Not Handled**. Rubber-stamping ("all cases handled") without line-level proof is a protocol failure.

3. **Universal Arbitrary Function Applicability**
   - The skill operates on any arbitrary function (API endpoints, data transformers, parsers, async workers, mathematical algorithms, utilities) across any programming language without requiring exercise-specific or custom test configuration.

4. **Actionable Remediation**
   - For every edge case marked as **Not Handled**, the report must state whether it represents an acceptable design decision (e.g., delegated to upstream gateway) or a critical gap requiring an immediate code patch.

---

## 2. Universal Edge-Case Taxonomy

Every invocation of `/verify` evaluates the target function against the universal edge-case baseline:

| # | Edge Case Category | Description & Probing Question | Typical Failure Mode |
|---|---|---|---|
| **1** | **Empty / Null / Undefined Input** | What happens if the input is `None`, `null`, `undefined`, empty string `""`, empty list `[]`, or empty dict `{}`? | `TypeError`, `NullPointerException`, indexing into empty sequence. |
| **2** | **Duplicate Identifier / Collision** | How does the function behave if duplicate IDs, repeated records, or duplicate dictionary keys are supplied? | Silent overwrites, duplicate database inserts, non-idempotent mutations. |
| **3** | **Malformed / Schema Violation** | What happens when unexpected data types, missing required fields, or truncated JSON payloads arrive? | Unhandled `KeyError`, schema parsing crash, corrupted downstream state. |
| **4** | **Rate Limiting & HTTP 429 / Backoff** | If the function calls external APIs or downstream services, does it handle rate limits (HTTP 429) or transient 5xx errors with retry/exponential backoff? | Unhandled HTTP exceptions, cascading service degradation, infinite retry loops. |
| **5** | **Boundary & Extreme Values** | What happens at numerical boundaries (`0`, `-1`, `MAX_INT`, negative offsets, floating point precision limits) or maximum payload sizes? | Off-by-one errors, division by zero, memory exhaustion, integer overflow. |
| **6** | **Concurrency & State Mutability** | If invoked concurrently or with shared/mutable default arguments, does race conditions or state pollution occur? | Shared mutable default arguments (e.g., `def fn(acc=[])`), non-atomic read-modify-writes. |
| **7** | **Resource Cleanup & Failure Modes** | Are open sockets, file handles, database connections, or subprocesses guaranteed to close on exception? | Leaked connections, unclosed file descriptors, orphaned worker threads. |

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
│ 2. Systematic Edge-Case Probing                             │
│    - Test against all 7 taxonomy categories                 │
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

### Step 2: Systematic Edge-Case Probing
Trace code paths against each taxonomy item:
- Check guard clauses (`if not input: ...`).
- Check deduplication mechanisms (`set()`, unique constraints, idempotency keys).
- Check schema validation (`try/except`, Pydantic/Zod validators, type guards).
- Check HTTP/client retries (backoff decorator, retry loop, status code inspection).
- Check bounds checks (`len()`, range constraints, clamp functions).
- Check concurrency safety (`asyncio.Lock`, atomic primitives, immutable defaults).

### Step 3: Populate Verification Matrix
Assign either `Handled [✓]` or `Not Handled [✗]` for each row. Provide a precise, single-sentence justification with code references.

### Step 4: Remediation Plan
If any unhandled item poses runtime or data integrity risks, provide a minimal, non-breaking code diff fixing the gap.

### Step 5: Deliver Verification Report
Render the final output using the mandatory Markdown template format.

---

## 4. Output Template Specification

The verification output must strictly adhere to the structure defined in `templates/verification_matrix.md`:

```markdown
### Verification Matrix: `<function_name>`

| Category | Specific Edge Case | Status | Line / Ref | Justification & Evidence |
| :--- | :--- | :---: | :--- | :--- |
| **Empty Input** | `None` / `""` / `[]` | `Handled` | L4-L6 | Guard clause `if not records:` returns early with empty result. |
| **Duplicate ID** | Duplicate primary keys in payload | `Not Handled` | — | Overwrites existing dictionary key without deduplication or warning. |
| **Malformed Record** | Missing expected `'id'` or invalid type | `Handled` | L12-L15 | Validated via `validate_record()` with schema error catch. |
| **429 / Backoff** | Downstream rate limit (HTTP 429) | `Not Handled` | L22 | Raw `requests.get()` call without retry decorator or backoff loop. |
| **Boundary Values** | `batch_size = 0` or negative values | `Handled` | L8 | Clamped with `max(1, batch_size)`. |
| **Concurrency** | Concurrent invocation on shared cache | `Not Handled` | L30 | In-memory cache dictionary is modified without lock. |
| **Resource Leaks** | Network session / file descriptor | `Handled` | L18 | Managed within `with requests.Session() as session:` context. |

#### Summary Metrics
- **Total Edge Cases Evaluated:** 7
- **Handled:** 4 / 7 (57%)
- **Not Handled:** 3 / 7 (43%)
- **Critical Unhandled Gaps:** 2 (Duplicate ID, 429 / Backoff)

#### Remediation & Patch
[Include code patch or explicit rationale for deferred items]
```

---

## 5. Examples & References

- Complete Template: [`templates/verification_matrix.md`](templates/verification_matrix.md)
- Real-World Verification Example: [`examples/example_verification.md`](examples/example_verification.md)
