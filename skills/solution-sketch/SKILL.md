---
name: solution-sketch
description: "Use before writing code on any non-trivial task — live pairing, an interview, solo implementation, or an autonomous run — right after the problem is understood and before code starts. Walks entities → data flow → edge cases → interface contract in a fixed order to produce a fast structured sketch, and emits a Mermaid diagram from it. This frames a single problem for implementation — it is not for splitting a large initiative into sub-issues/stage barriers (that's autonomous-evolution-engine's job). Use when asked to 'sketch this problem', 'frame this before we code', 'structure this before implementation', 'walk me through this problem', or at the start of any nontrivial implementation. Do not use for isolated diagram requests, post-hoc documentation of existing code, breaking an oversized task into sub-issues, or as a rigid intake form."
user-invocable: true
---

# Solution Sketch

A fast ritual for turning a problem statement — spoken, written, or self-derived — into a structured sketch before any code gets written. It externalizes reasoning; it does not replace it.

This is about *framing one problem for implementation* — entities, flow, failure modes, and a boundary — not about *splitting a large initiative into sub-issues*. For the latter (oversized tasks, stage barriers, INVEST gates), use `autonomous-evolution-engine` instead.

---

## 1. Design Constraint (read first)

This is a reasoning aid, not a form. Never interrogate field-by-field or block on an answer to every sub-question. Each step below draws primarily from what's already known about the problem — a human narrating out loud, a written spec, an issue description, or your own initial read of the problem if you're working solo. Ask at most one short clarifying question per step, and only when a human is present and the step genuinely cannot proceed without it; when working autonomously, state the assumption you're making instead and move on.

Keep each step tight — a handful of lines, not an essay. There is no fixed time budget here: an LLM doesn't have a wall clock, and pinning steps to minute marks (as an earlier version of this skill did) is a category error — it borrows a human-interview pacing device that means nothing to the process actually doing the work, and it pressures verbosity or brevity for no reason tied to the problem itself. If a step is running long relative to the problem's actual complexity, summarize what's known and advance — the goal is momentum, not exhaustiveness.

---

## 2. The Sequence

Walk these four steps in order. If narrating for a human, say each transition out loud (e.g. "okay, entities look like X, Y, Z — let's trace the flow"). If working autonomously, the same structure still applies — just as internal reasoning made visible in the output.

### Step 1 — Entities
Name the nouns in the problem: the things that get created, stored, moved, or referenced. For each, give a name and 1–2 defining attributes — not a full schema, just enough to anchor the diagram.

- Ask: "what are the things?" not "what are all their fields?"
- 3–6 entities is typical; more suggests the problem should be scoped down first.

### Step 2 — Data Flow
Trace one representative request or event from source to sink: where does it enter, what transforms happen, where does it land. Describe it as a chain — `source → transform → sink` — using the entities from Step 1.

- If there are multiple flows (e.g. read path and write path), pick the primary one and note the others exist without expanding them yet.

### Step 3 — Edge Cases
Name what breaks the happy path, drawing on your actual domain knowledge of what tends to fail in problems shaped like this one — do not limit yourself to a fixed checklist, and do not force in categories that don't apply to this problem. Aim for 3–5 concrete cases tied to the flow just traced, not a generic list recited regardless of context.

Some illustrative starting lenses, by problem shape — use these to prime thinking, not to constrain it:
- **Ingestion / sync / webhook-driven:** duplicate or replayed deliveries, partial-failure resumability, upstream rate limits or outages, schema drift from the source.
- **Concurrent / stateful:** races between readers and writers, stale reads, lost updates, deadlock or starvation under contention.
- **User-facing / interactive:** empty and loading states, partial input, cancellation mid-flow, conflicting concurrent edits.
- **Algorithmic / data-heavy:** boundary and empty-input values, pathological inputs that blow up complexity, precision/overflow at scale.

These are prompts, not a taxonomy to complete — a problem may need none of them and something else entirely (a parser needs malformed-input handling regardless of the above; a scheduler needs clock-skew handling that fits none of these buckets). Name whatever actually threatens correctness for *this* problem.

### Step 4 — Interface Contract
Define the smallest boundary the code will actually implement: a function signature, an endpoint shape, or an event schema. It should be just large enough to satisfy the flow and edge cases already named — resist expanding scope here.

---

## 3. Diagram Output

After the walk (not during it — don't interrupt reasoning to draw), emit **one** Mermaid diagram generated from what was established in Steps 1–2:

- **Entity-relationship** (`erDiagram`) when the problem is dominated by entities and their relationships (data modeling, storage design).
- **Sequence** (`sequenceDiagram`) when the problem is dominated by interaction over time (API calls, event flow, multi-service coordination).

Pick whichever the breakdown actually produced more of — don't force both. See `references/mermaid-templates.md` for syntax templates and a validity checklist (balanced brackets, correct arrow tokens, one diagram type declared) to run over the output before presenting it.

---

## 4. Output Shape

At the end of the ritual, the artifact left behind is:
- The Mermaid diagram (§3), valid and rendered inline.
- The edge cases actually identified as material to this problem (§2, Step 3) — whatever came out of applying judgment to this specific problem, not a fixed list.

Nothing else is required. The reasoning itself, not a written summary of it, is the primary output of the ritual.
