#!/usr/bin/env python3
"""PreToolUse hook: block writes to paths you never want an agent editing.

Wired to matcher "Edit|Write|NotebookEdit". Edit PROTECTED below to suit.

**Off until you turn it on.** Set "protect-paths": true in
`~/.claude/handrail-hooks.json`. See _config.py for why the switch lives there and
not in this plugin's own files.

Patterns are matched against the normalised absolute path with forward slashes,
so they work the same on Windows and macOS.
"""
import fnmatch
import json
import os
import sys

import _config

# Add your own. Each entry is a glob matched against the full path.
PROTECTED = [
    "**/.env",
    "**/.env.*",
    "**/*.pem",
    "**/*.key",
    "**/id_rsa*",
    "**/secrets/**",
    # Three patterns, not one glob. fnmatch lets `*` cross `/`, so the obvious
    # "**/credentials*" also matches every file under any directory whose name
    # merely starts with the word, making C:/dev/credentials-service/src/main.py
    # unwritable. Same shape as the secrets entry above, which never had the bug.
    "**/credentials",
    "**/credentials.*",
    "**/credentials/**",
    "**/node_modules/**",
    "**/.git/**",
]

# Explicit escape hatches, checked first.
ALLOWED = [
    "**/.env.example",
    "**/.env.template",
]


def normalise(path):
    return os.path.abspath(os.path.expanduser(path)).replace("\\", "/")


def matches(path, patterns):
    return any(fnmatch.fnmatch(path, p) for p in patterns)


def deny(reason):
    json.dump({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }, sys.stdout)
    sys.exit(0)


def main():
    if not _config.enabled("protect-paths"):
        sys.exit(0)

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # never block on a hook bug

    # Edit and Write pass "file_path"; NotebookEdit passes "notebook_path".
    # Reading only the first silently allows every notebook edit, which looks
    # exactly like a hook that ran and found nothing to object to.
    tool_input = payload.get("tool_input", {}) or {}
    raw = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not raw:
        sys.exit(0)

    path = normalise(raw)
    if matches(path, ALLOWED):
        sys.exit(0)
    if matches(path, PROTECTED):
        deny(
            f"Writes to {raw} are blocked by the protect-paths hook. "
            "If this is intentional, make the change by hand outside Claude Code, "
            "or set \"protect-paths\": false in ~/.claude/handrail-hooks.json to "
            "turn the hook off entirely."
        )
    sys.exit(0)


if __name__ == "__main__":
    main()
