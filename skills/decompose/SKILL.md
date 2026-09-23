---
name: decompose
description: "Use at the start of a live coding or pairing session, before any code is written, when a problem has just been stated out loud and needs to be broken down. Walks entities → data flow → edge cases → interface contract in a fixed sequence under 3 minutes, emits a Mermaid diagram generated from what was said, and — only for data-ingestion/sync-shaped problems — surfaces a short integration-pattern checklist. Use when asked to 'decompose this', 'break this down before we code', 'let's structure this out loud', 'walk me through this problem', or at the top of an interview/design session. Do not use for isolated diagram requests, post-hoc documentation of existing code, or as a rigid intake form."
user-invocable: true
---

# Decompose & Diagram

A fast, narratable ritual for turning a verbal problem statement into a structured breakdown before any code gets written. It externalizes what's being said — it does not replace saying it.

---

## 1. Design Constraint (read first)

This is a narration aid, not a form. Never interrogate the other person field-by-field or block on an answer to every sub-question. Each step below produces its output primarily from what has *already* been said in the conversation so far; ask at most one short clarifying question per step, and only when the step genuinely cannot proceed without it. If the verbal statement is thin on a step, say what's missing in one line and move on — the ritual's job is to keep momentum, not to stall it.

Target: **under 3 minutes** end-to-end for a typical problem statement. If a step is running long, summarize what's known and advance rather than exhausting the topic.

---

## 2. The Sequence

Walk these four steps in order. Narrate each transition out loud (e.g. "okay, entities look like X, Y, Z — let's trace the flow").

### Step 1 — Entities (~0:00–0:45)
Name the nouns in the problem: the things that get created, stored, moved, or referenced. For each, give a name and 1–2 defining attributes — not a full schema, just enough to anchor the diagram.

- Ask: "what are the things?" not "what are all their fields?"
- 3–6 entities is typical; more suggests the problem should be scoped down first.

### Step 2 — Data Flow (~0:45–1:30)
Trace one representative request or event from source to sink: where does it enter, what transforms happen, where does it land. Describe it as a chain — `source → transform → sink` — using the entities from Step 1.

- If there are multiple flows (e.g. read path and write path), pick the primary one and note the others exist without expanding them yet.

### Step 3 — Edge Cases (~1:30–2:15)
Name what breaks the happy path: empty/missing input, duplicates, concurrent writes, malformed data, partial failure, rate limits, out-of-order arrival. Aim for 3–5 concrete cases tied to the actual flow just traced, not a generic checklist.

- This is where the data-integration checklist (§4) gets folded in, when it applies — as talking points inside this step, not a separate pass.

### Step 4 — Interface Contract (~2:15–3:00)
Define the smallest boundary the code will actually implement: a function signature, an endpoint shape, or an event schema. It should be just large enough to satisfy the flow and edge cases already named — resist expanding scope here.

---

## 3. Diagram Output

After the walk (not during it — don't interrupt narration to draw), emit **one** Mermaid diagram generated from what was said in Steps 1–2:

- **Entity-relationship** (`erDiagram`) when the problem is dominated by entities and their relationships (data modeling, storage design).
- **Sequence** (`sequenceDiagram`) when the problem is dominated by interaction over time (API calls, event flow, multi-service coordination).

Pick whichever the conversation actually produced more of — don't force both. See `references/mermaid-templates.md` for syntax templates and a validity checklist (balanced brackets, correct arrow tokens, one diagram type declared) to run over the output before presenting it.

---

## 4. Data-Integration Checklist (conditional — not universal)

Only surface this when the problem itself is ingestion/sync-shaped: pulling from an external API, replicating a data source, polling, webhooks, batch import/export, or CDC-style change propagation. Recognize it from the entities and flow already named — do not ask "is this a data sync problem?" as a gate question.

If it applies, weave these three patterns into Step 3 (Edge Cases) as talking points, not a bolt-on task list:

1. **Upsert-by-natural-key** — how do repeated deliveries of the same record get deduplicated?
2. **Cursor/offset checkpointing** — how does the sync resume after a partial run without reprocessing everything or dropping records?
3. **Exponential backoff on 429** — how does the flow behave when the upstream source rate-limits it?

Full detail and phrasing for each: `references/integration-checklist.md`.

If the problem is not data-integration-shaped, skip this section entirely — do not mention it.

---

## 5. Output Shape

At the end of the ritual, the artifact left behind is:
- The Mermaid diagram (§3), valid and rendered inline.
- If applicable, the 1–3 integration patterns actually discussed (§4) — only the ones that came up, not the full checklist by default.

Nothing else is required. The narration itself, not a written summary of it, is the primary deliverable of the session.
