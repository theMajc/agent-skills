#!/usr/bin/env python3
"""
Zero-dependency Python fallback compactor for Multica agents.
Used when external binaries (rtk, tokenjuice) are not present in the runtime environment.
"""

import sys
import os
import re
import subprocess

ANSI_REGEX = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def strip_ansi(text: str) -> str:
    return ANSI_REGEX.sub('', text)

def compact_test_output(lines: list[str]) -> list[str]:
    """Isolate failed tests, stack traces, and summary while collapsing passing tests."""
    result = []
    in_failure = False
    failure_block = []
    summary_lines = []

    for line in lines:
        stripped = line.strip()
        lower = stripped.lower()

        # Detect summary lines (usually at the end)
        if any(marker in lower for marker in ['tests:', 'suites:', 'test suites:', 'total:', 'passed,', 'failed,', 'short test summary info']):
            summary_lines.append(line)
            continue

        # Detect failure start
        if any(marker in stripped for marker in ['FAIL', '✕', 'FAILED', 'FAILURE:', 'AssertionError', 'Error:', 'not ok']):
            in_failure = True
            failure_block.append(line)
            continue

        if in_failure:
            # Continue collecting failure stack/details until next passing test or separator
            if stripped.startswith('✓') or stripped.startswith('PASS') or stripped.startswith('ok '):
                in_failure = False
                if len(failure_block) > 40:
                    result.extend(failure_block[:20])
                    result.append(f"  ... [{len(failure_block)-30} lines collapsed] ...")
                    result.extend(failure_block[-10:])
                else:
                    result.extend(failure_block)
                failure_block = []
            else:
                failure_block.append(line)

    if failure_block:
        if len(failure_block) > 40:
            result.extend(failure_block[:20])
            result.append(f"  ... [{len(failure_block)-30} lines collapsed] ...")
            result.extend(failure_block[-10:])
        else:
            result.extend(failure_block)

    if not result and not summary_lines:
        # If no explicit failures were isolated, return head and tail
        if len(lines) > 30:
            return lines[:10] + [f"... [{len(lines)-20} lines omitted] ..."] + lines[-10:]
        return lines

    return result + summary_lines

def compact_diff_output(lines: list[str]) -> list[str]:
    """Strip lockfile noise and collapse large hunk bodies."""
    result = []
    skipping_lockfile = False

    for line in lines:
        if line.startswith('diff --git'):
            if any(l in line for l in ['lock.json', 'lock.yaml', 'Cargo.lock', 'yarn.lock', 'pnpm-lock']):
                skipping_lockfile = True
                result.append(f"[diff pruned: lockfile change {line.split()[-1]}]")
                continue
            else:
                skipping_lockfile = False

        if not skipping_lockfile:
            result.append(line)

    if len(result) > 100:
        return result[:30] + [f"... [{len(result)-60} diff lines omitted] ..."] + result[-30:]
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: compact_fallback.py [--test|--diff|--general] [--] <command...>", file=sys.stderr)
        sys.exit(1)

    args = sys.argv[1:]
    mode = "general"

    if args[0].startswith("--") and args[0] in ["--test", "--diff", "--general"]:
        mode = args[0][2:]
        args = args[1:]

    if args and args[0] == "--":
        args = args[1:]

    if not args:
        print("Error: No command specified to run.", file=sys.stderr)
        sys.exit(1)

    cmd = args

    # Infer mode from command name if general
    if mode == "general":
        cmd_str = " ".join(cmd).lower()
        if any(t in cmd_str for t in ["test", "vitest", "jest", "pytest"]):
            mode = "test"
        elif "diff" in cmd_str:
            mode = "diff"

    # Set non-color env vars
    env = os.environ.copy()
    env["NO_COLOR"] = "1"
    env["FORCE_COLOR"] = "0"
    env["TERM"] = "dumb"

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
        errors="replace"
    )

    raw_output, _ = proc.communicate()
    clean_text = strip_ansi(raw_output)
    lines = clean_text.splitlines()

    if mode == "test":
        compacted = compact_test_output(lines)
    elif mode == "diff":
        compacted = compact_diff_output(lines)
    else:
        if len(lines) > 40:
            compacted = lines[:15] + [f"... [{len(lines)-30} lines omitted] ..."] + lines[-15:]
        else:
            compacted = lines

    for l in compacted:
        print(l)

    sys.exit(proc.returncode)

if __name__ == "__main__":
    main()
