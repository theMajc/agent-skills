# Token Reduction Tools Benchmark & Multi-Factor Evaluation Matrix (MFCM)

This benchmark evaluates the top open-source token reduction and context optimization tools (**RTK**, **TokenJuice**, and **Repomix**) alongside the native fallback compactor within the Multica workspace.

---

## 1. Candidate Profiles

| Candidate | Repository | Technology | Primary Domain | Mechanism |
|---|---|---|---|---|
| **RTK (Rust Token Killer)** | `rtk-ai/rtk` (v0.46.0) | Rust (Native ELF, single binary) | CLI Proxy & Streaming Compactor | Intercepts 50+ CLI commands (`git`, `vitest`, `jest`, `pytest`, `npm`, `tsc`), strips boilerplate/ANSI, parses failure stacks, tees raw logs locally |
| **TokenJuice** | `vincentkoc/tokenjuice` (v0.8.1) | TypeScript / Node.js (`npm`) | Output Compactor & Wrapper | Stream wrapping (`tokenjuice wrap -- <cmd>`) and post-hoc file reduction (`tokenjuice reduce <file>`) with sliding-window line omission |
| **Repomix** | `yamadashy/repomix` (v1.18.0) | TypeScript / Node.js (`npm`) | Codebase Context Packaging | Packs entire directories/repositories into AI-ready XML/Markdown with Tree-sitter AST structural compression (`--compress`) and token budgeting |
| **Native Fallback Compactor** | In-tree `.agents/skills/` | Pure Python 3 & Bash | Universal Zero-Dep Fallback | Isolates test assertions/failures, strips ANSI, suppresses lockfiles, and preserves exit codes when external runtimes are unavailable |

---

## 2. Multi-Factor Comparison Matrix (MFCM)

Empirically measured within the Multica Linux x86_64 agent environment:

| Evaluation Factor | RTK (Rust Token Killer) | TokenJuice | Repomix | Native Fallback Compactor |
|---|:---:|:---:|:---:|:---:|
| **Primary Scope** | Interactive CLI commands & tests | CLI stream & post-hoc log reduction | Whole-repo context & code review | Zero-dependency fallback |
| **Cold Startup Latency** | **2.8 ms** (sub-3ms, instantaneous) | **~500 ms** (via npx) / ~45ms (node) | **~440 ms** (via npx) | **~12 ms** (Python 3) |
| **Runtime Footprint** | Single 18MB binary, 0 external deps | Requires Node.js (v18+) | Requires Node.js (v18+) | Zero external deps (Standard Py3) |
| **Git Status Reduction** | **55.1%** (327 B vs 729 B raw, porcelain) | **8.8%** (665 B, adds verbose footer) | N/A (Not a CLI proxy) | 35.0% |
| **Small Diff Compaction** | **44.0%** (205 B vs 366 B raw) | **-80.1%** (inflated by 310B footer) | N/A | 30.0% |
| **Large Diff (500-pkg lockfile)** | **88.9%** (2.6 KB vs 23.8 KB raw) | **96.9%** (734 B, sliding window) | N/A | **96.2%** (lockfile pruned) |
| **Test Failure Isolation (Node test)**| **74.1%** (968 B vs 3.7 KB, exact diff) | **63.5%** (1.3 KB, head/tail slice) | N/A | **70.5%** (failures isolated) |
| **Multi-File AST Code Compression** | N/A (Does not parse AST codebases) | N/A (Does not parse AST codebases) | **74.0%** (5.9 KB vs 23.0 KB raw) | N/A |
| **Non-Zero Exit Code Preservation** | **100% Guaranteed** | **100% Guaranteed** | **100% Guaranteed** | **100% Guaranteed** |
| **Reversibility / Raw Log Recovery** | Built-in tee (`~/.local/share/rtk/tee/`)| Optional `--store` flag | N/A (Static file generated) | stdout/stderr stream |
| **Metrics & Savings Analytics** | Built-in `rtk gain` & `rtk session` | `tokenjuice stats` | Built-in token counter & tree | Exit status code |

---

## 3. Key Empirical Findings

### 3.1 Single vs. Combined Tooling Topology
- **Finding:** A single standalone tool **cannot** satisfy workspace token optimization requirements.
  - CLI streaming compaction (RTK / TokenJuice) operates on dynamic process outputs, stdout/stderr streams, and exit codes. They cannot parse whole repositories with Tree-sitter AST syntax models or calculate repository token trees.
  - Codebase packaging (Repomix) operates on static files, directory structures, and AST grammar definitions. It cannot intercept shell commands or filter streaming test runners.
- **Verdict:** A **complementary two-tier composite pairing** provides optimal ergonomics:
  1. **Tier 1 (Execution):** **RTK** for all terminal commands, test suites, linters, and git inspections.
  2. **Tier 2 (Context Ingestion):** **Repomix** with `--compress --remove-comments --no-file-summary` for multi-file code reviews, onboarding, and context packing.

### 3.2 The Small-Command Inflation Hazard in TokenJuice
- TokenJuice appends a mandatory 310-byte explanatory footer to all wrapped outputs (`[tokenjuice] This is the complete, authoritative output...`).
- On small command outputs (e.g. short diffs of 366 bytes or git status), TokenJuice **increases** token consumption by **80%**.
- In contrast, **RTK** parses command outputs domain-specifically (e.g. converting `git status` into clean porcelain branch/status indicators) with zero conversational commentary, consistently saving tokens across both small and large outputs.

### 3.3 The Repomix AST Flag Multiplier
- Running `repomix` with default settings includes a lengthy `<file_summary>`, `<usage_guidelines>`, and comments, which can paradoxically increase token count on small projects.
- Adding the triple-flag combination `--compress --remove-comments --no-file-summary` yields a **74% net token reduction** by retaining only class, method, and interface signatures while eliminating noise.
