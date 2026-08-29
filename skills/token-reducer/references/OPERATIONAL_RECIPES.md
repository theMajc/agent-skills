# Operational Recipes: Transparent & Explicit Context Compaction

This document defines the operational models for token compaction across transparent harness hooks and explicit context ingestion.

---

## 1. Transparent Terminal Execution (Primary Workflow)

Thanks to the `PreToolUse` hook in `.agents/hooks.json`, **agents do NOT need to manually prefix commands or use custom wrapper syntax**.

The agent simply issues natural developer commands:

```bash
# Natural execution - automatically intercepted and rewritten to RTK:
git status            # Rewritten to: rtk git status
git diff              # Rewritten to: rtk diff
npx vitest run        # Rewritten to: rtk vitest
jest --silent         # Rewritten to: rtk jest --silent
pytest -q             # Rewritten to: rtk pytest -q
npx tsc --noEmit      # Rewritten to: rtk tsc
npm run test          # Rewritten to: rtk npm run test
```

### What Happens Behind the Scenes:
1. `run_command` is called by the agent.
2. The `PreToolUse` hook triggers `scripts/agy_hook_rewrite.py`.
3. `rtk hook check` evaluates if a specialized compactor exists.
4. The hook returns `{"decision": "allow", "overwrite": {"CommandLine": "rtk <cmd>"}}`.
5. The compacted output enters the context window with **sub-3ms latency**, full exit code preservation, and raw logs teed to `~/.local/share/rtk/tee/`.

---

## 2. Auto-Installation Strategy (`ensure_rtk.sh`)

If an agent or container starts in an environment where `rtk` is not installed:
1. `agy_hook_rewrite.py` detects missing binary and invokes `scripts/ensure_rtk.sh`.
2. `ensure_rtk.sh` downloads the static musl binary (~18MB, zero external dependencies) directly from GitHub releases and places it in `~/.gemini/antigravity-cli/bin/rtk`.
3. If internet access is restricted or download fails, the hook automatically rewrites commands to the zero-dependency Python fallback `scripts/compact_fallback.py`.

---

## 3. Explicit Codebase Context Ingestion (Repomix)

Whole-repository context packaging cannot be inferred from a shell command. When an agent needs to inspect an entire codebase, module, or subproject:

```bash
# 1. High-efficiency AST compression (74% token reduction)
repomix path/to/project --compress --remove-comments --no-file-summary --output .agent_context/repo_context.xml

# 2. Guard with token budget (fails with exit code 1 if budget exceeded)
repomix . --compress --remove-comments --no-file-summary --token-budget 20000 --output .agent_context/context.xml

# 3. Via the helper script
.agents/skills/terminal-output-compactor/scripts/pack_context.sh --dir ./src --output context.xml --budget 15000
```

---

## 4. Telemetry & Auditability

Agents and users can inspect token savings at any time:

```bash
# Inspect cumulative token reduction and command history
rtk gain
rtk gain --history

# Recover raw untruncated logs for any run
cat ~/.local/share/rtk/tee/<timestamp>_<command>.log
```
