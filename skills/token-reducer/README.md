# token-reducer

Production-ready Multica workspace skill that passively and actively minimizes LLM token consumption across terminal command execution, test runner outputs, git diffs, and whole-codebase context packing.

## Components

1. **RTK (Rust Token Killer):** Ultra-low-latency (sub-3ms) terminal CLI proxy that compacts test output, prunes lockfile diffs, formats git status, and tees raw logs.
2. **Transparent Hooks (`agy_hook_rewrite.py`):** Harness-level `PreToolUse` hook interceptor that mutates commands in-flight with zero agent prompt directives or cognitive overhead.
3. **Deterministic Auto-Installer (`ensure_rtk.sh`):** Fetches the official static musl RTK binary (v0.46.0, ~18MB) from GitHub releases when missing.
4. **Repomix Context Packager (`pack_context.sh`):** Tree-sitter AST compression engine that strips comments and collapses implementations to signatures to fit codebase context under strict token budgets.
5. **Zero-Dependency Fallback (`compact_fallback.py`):** Pure Python in-tree fallback for air-gapped environments.

## File Layout

```text
token-reducer/
├── SKILL.md                          # Skill definition & agent instruction manifest
├── README.md                         # Human-readable documentation
├── references/
│   ├── BENCHMARK_MATRIX.md           # Benchmark data (RTK vs TokenJuice vs Repomix)
│   └── OPERATIONAL_RECIPES.md        # Command syntax, hook setup, and recipes
├── scripts/
│   ├── agy_hook_rewrite.py           # Antigravity PreToolUse hook rewrite handler
│   ├── ensure_rtk.sh                 # RTK binary auto-installer
│   ├── compact_run.sh                # Streaming CLI command orchestrator
│   ├── pack_context.sh               # Repomix AST codebase context packager
│   └── compact_fallback.py           # Zero-dependency Python fallback
└── tests/
    └── test_orchestrator.py          # Automated verification test suite
```

## Running Tests

```bash
python3 -m unittest tests/test_orchestrator.py
```
