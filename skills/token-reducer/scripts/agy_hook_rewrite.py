#!/usr/bin/env python3
"""
PreToolUse transparent command rewriter hook for Antigravity (agy).
Intercepts run_command calls, delegates to rtk hook check / rewrite,
and mutates CommandLine transparently without requiring agent manual prefixing.
"""

import sys
import json
import os
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENSURE_SCRIPT = os.path.join(SCRIPT_DIR, "ensure_rtk.sh")
FALLBACK_SCRIPT = os.path.join(SCRIPT_DIR, "compact_fallback.py")
SKILL_BIN_RTK = os.path.join(SCRIPT_DIR, "..", "bin", "rtk")

def resolve_rtk() -> str:
    # 1. Check system PATH
    rtk = shutil.which("rtk")
    if rtk:
        return rtk
    # 2. Check skill bin or antigravity bin
    for candidate in [SKILL_BIN_RTK, "/home/max/.gemini/antigravity-cli/bin/rtk"]:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    # 3. Try auto-installing via ensure_rtk.sh
    if os.path.isfile(ENSURE_SCRIPT) and os.access(ENSURE_SCRIPT, os.X_OK):
        try:
            res = subprocess.run([ENSURE_SCRIPT], capture_output=True, timeout=10)
            if res.returncode == 0:
                rtk = shutil.which("rtk")
                if rtk:
                    return rtk
                if os.path.isfile(SKILL_BIN_RTK) and os.access(SKILL_BIN_RTK, os.X_OK):
                    return SKILL_BIN_RTK
        except Exception:
            pass
    return ""

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"decision": "allow"}))
            return
        payload = json.loads(raw_input)
    except Exception:
        print(json.dumps({"decision": "allow"}))
        return

    tool_call = payload.get("toolCall", {})
    tool_name = tool_call.get("name", "")
    args = tool_call.get("args", {})
    command_line = args.get("CommandLine", "").strip()

    if tool_name != "run_command" or not command_line:
        print(json.dumps({"decision": "allow"}))
        return

    # Check if already prefixed with rtk or compact_run
    if command_line.startswith("rtk ") or "compact_run.sh" in command_line:
        print(json.dumps({"decision": "allow"}))
        return

    rtk_bin = resolve_rtk()
    if rtk_bin:
        try:
            # Use rtk hook check
            res = subprocess.run(
                [rtk_bin, "hook", "check", command_line],
                capture_output=True,
                text=True,
                timeout=2
            )
            if res.returncode == 0 and res.stdout.strip():
                rewritten = res.stdout.strip()
                out = {
                    "decision": "allow",
                    "overwrite": {
                        "CommandLine": rewritten
                    }
                }
                print(json.dumps(out))
                return
        except Exception:
            pass

    # If RTK is unavailable, fallback to internal Python compactor for tests / git diff
    lower_cmd = command_line.lower()
    if any(k in lower_cmd for k in ["vitest", "jest", "pytest", "node --test", "git diff", "git status"]):
        if os.path.isfile(FALLBACK_SCRIPT):
            rewritten = f"python3 {FALLBACK_SCRIPT} -- {command_line}"
            out = {
                "decision": "allow",
                "overwrite": {
                    "CommandLine": rewritten
                }
            }
            print(json.dumps(out))
            return

    # Passthrough untouched
    print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
