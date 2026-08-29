---
name: token-reducer
description: "Use when executing terminal commands, test runners, git diffs, or packing repository context under token budgets using RTK, Repomix, or fallback compactors."
user-invocable: false
allowed-tools: Bash(*)
---

# Token Reducer: Multi-Tier Output Compactor & Context Optimizer

A unified Multica workspace skill and tool orchestrator providing sub-3ms streaming output compaction, test failure isolation, lockfile diff pruning, and Tree-sitter AST codebase packaging.

---

## 1. Architecture & Execution Topology

LLM coding agents spend up to 85% of their context windows on redundant terminal noise, passing test logs, bloated diffs, and whole-file dumps. `token-reducer` combines specialized open-source token reduction engines with an in-tree, zero-dependency local fallback:

```
                      AGENT EXECUTION / CONTEXT INGESTION
                                       │
        ┌──────────────────────────────┴──────────────────────────────┐
        ▼                                                             ▼
[Streaming Terminal Commands]                               [Codebase Context Packing]
(Tests, Diffs, Builds, Linters)                             (Multi-file AST Ingestion)
        │                                                             │
        ▼                                                             ▼
`scripts/compact_run.sh`                                   `scripts/pack_context.sh`
        │                                                             │
  ┌─────┴─────────────────────┐                                       ▼
  │ 1. RTK (sub-3ms Rust)     │                               Repomix AST Engine
  │ 2. TokenJuice (npm wrap)  │                               (--compress, --remove-comments,
  │ 3. Python3 Fallback       │                                --no-file-summary, --budget N)
  └───────────────────────────┘
```

---

## 2. Multi-Factor Comparison Summary

| Metric | RTK (Rust Token Killer) | TokenJuice | Repomix | Python Fallback |
|---|:---:|:---:|:---:|:---:|
| **Domain** | Terminal CLI Proxy | Stream Wrapper / Reducer | Codebase Packaging | In-Tree Fallback |
| **Startup Overhead** | **2.8 ms** (sub-3ms) | ~500 ms (npx) / 45ms (node) | ~440 ms (npx) | ~12 ms |
| **Runtime Footprint** | Native ELF (18MB) | Node.js / npm | Node.js / npm | Zero external deps |
| **Git Status Reduction** | **55.1%** (327 B) | 8.8% (adds footer) | N/A | 35.0% |
| **Diff Compaction** | **44.0%** (small), **88.9%** (lockfile) | **96.9%** (lockfile) | N/A | **96.2%** (lockfile pruned) |
| **Test Failure Isolation** | **74.1%** (isolates stack trace) | 63.5% (head/tail slice) | N/A | 70.5% (failure isolate) |
| **AST Code Compression** | N/A | N/A | **74.0%** (signatures only) | N/A |
| **Exit Code Forwarding** | **100% Guaranteed** | **100% Guaranteed** | **100% Guaranteed** | **100% Guaranteed** |

*For benchmark details and test reproduction, see [BENCHMARK_MATRIX.md](references/BENCHMARK_MATRIX.md).*

---

## 3. Transparent Harness Integration

Rather than burdening agents with manual CLI prefixing or prompt-driven wrappers, this skill supports **transparent harness-level lifecycle interception**:

1. **Antigravity (`agy`) PreToolUse Hook:**
   - Configured in `.agents/hooks.json` under `PreToolUse` for `run_command`.
   - Calls `scripts/agy_hook_rewrite.py`, which validates commands via `rtk hook check`.
   - Mutates `CommandLine` in-flight via the harness's native `overwrite` field (e.g. `git status` -> `rtk git status`, `npx vitest run` -> `rtk vitest`).
   - The agent writes normal bash commands with zero prompt overhead or cognitive load.

2. **Claude Code Hook:**
   - Configured via `rtk init -g --agent claude` to patch Claude Code's `~/.claude/settings.json` with `PreToolUse` hooks (`rtk hook claude`).

3. **Auto-Installation & Offline Fallback (`ensure_rtk.sh`):**
   - Automatically downloads and unpacks the official static musl binary (v0.46.0, ~18MB) from GitHub releases to `~/.gemini/antigravity-cli/bin/rtk` or `~/.local/bin/rtk` when absent.
   - In air-gapped or offline environments, `compact_run.sh` seamlessly falls back to `compact_fallback.py`.

---

## 4. Usage Workflow

1. **Passive Execution (Zero-Touch):**
   - Standard commands executed by the agent (`git status`, `git diff`, `vitest run`, `npm test`, `pytest`) are intercepted and compacted transparently.
2. **Explicit Codebase Packing:**
   - When multi-file repository context is needed, invoke `scripts/pack_context.sh` or `repomix --compress --remove-comments --token-budget <N>`.
3. **Telemetry & Audit:**
   - Uncompacted raw outputs are preserved under `~/.local/share/rtk/tee/`.
   - View cumulative token savings via `rtk gain`.

*For detailed recipes and usage examples, see [OPERATIONAL_RECIPES.md](references/OPERATIONAL_RECIPES.md).*
