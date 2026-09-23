# Data-Integration Pattern Checklist

Talking points for Step 3 (Edge Cases) when the problem is ingestion/sync-shaped (§4 of `SKILL.md`). These are conversation prompts, not code to write — the point is to surface the question out loud, not to produce an implementation.

## 1. Upsert-by-Natural-Key

**The question:** if the same source record arrives twice — retry, re-poll, duplicate webhook delivery — does it create a duplicate, or does it land on the same row?

**Talking points:**
- What's the natural key from the *source* system (not an auto-incrementing local id)?
- Is the upsert idempotent if the same payload arrives twice in a row?
- What happens if the natural key itself changes upstream (e.g. a rename)?

## 2. Cursor/Offset Checkpointing

**The question:** if the sync dies halfway through, does it resume from where it left off, or does it reprocess everything (or worse, silently skip the rest)?

**Talking points:**
- Is the checkpoint a timestamp, an opaque cursor token, or a numeric offset — and which of those does the source API actually support reliably?
- Is the checkpoint written *after* a batch is durably committed, not before (otherwise a crash mid-batch loses records)?
- What happens on a cursor that's gone stale/expired upstream?

## 3. Exponential Backoff on 429

**The question:** when the upstream source starts rate-limiting, does the sync back off and recover, or does it hammer the source and get the integration blocked entirely?

**Talking points:**
- Does the backoff respect a `Retry-After` header if the source sends one, or is it a fixed exponential schedule?
- Is there a ceiling (max retries / max delay) so a persistent outage doesn't spin forever?
- Does backoff on one partition/shard of the sync block progress on the others, or is it isolated?
