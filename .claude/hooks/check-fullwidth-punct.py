#!/usr/bin/env python3
import json
import sys

# ／ is intentionally excluded: index.html's sunrise/sunset line
# ("日出 05:25 ／ 日落 18:33") uses it deliberately per prior design decision.
FULLWIDTH_PUNCT = "，。、；：？！…—（）【】「」『』《》〈〉～·＼＂＇［］｛｝＿｜"


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {}) or {}

    if tool_name == "Edit":
        text = tool_input.get("new_string", "") or ""
    elif tool_name == "Write":
        text = tool_input.get("content", "") or ""
    else:
        text = ""

    found = sorted({ch for ch in text if ch in FULLWIDTH_PUNCT})
    if found:
        result = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    "偵測到全形標點符號：" + " ".join(found)
                    + "。請改用半形標點（, . ! ? : ; ( ) ' / 等）後再試一次。"
                ),
            }
        }
        print(json.dumps(result, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
