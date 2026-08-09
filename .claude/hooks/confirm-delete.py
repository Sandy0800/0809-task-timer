#!/usr/bin/env python3
import json
import re
import sys

DELETE_PATTERNS = [
    r"\brm\b",
    r"\brmdir\b",
    r"\bunlink\b",
    r"\bshred\b",
    r"\btrash\b",
    r"\bgit\s+rm\b",
    r"\bfind\b.*-delete\b",
]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    command = (data.get("tool_input", {}) or {}).get("command", "") or ""

    if any(re.search(p, command) for p in DELETE_PATTERNS):
        result = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": (
                    "這個指令看起來會刪除檔案或資料夾：" + command
                    + " —— 請先跟使用者確認過再執行。"
                ),
            }
        }
        print(json.dumps(result, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
