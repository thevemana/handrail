#!/usr/bin/env python3
"""PreToolUse hook: block writes to paths you never want an agent editing.

Wired to matcher "Edit|Write|NotebookEdit". Edit PROTECTED below to suit.

Patterns are matched against the normalised absolute path with forward slashes,
so they work the same on Windows and macOS.
"""
import fnmatch
import json
import os
import sys

# Add your own. Each entry is a glob matched against the full path.
PROTECTED = [
    "**/.env",
    "**/.env.*",
    "**/*.pem",
    "**/*.key",
    "**/id_rsa*",
    "**/secrets/**",
    "**/credentials*",
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
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # never block on a hook bug

    raw = payload.get("tool_input", {}).get("file_path", "")
    if not raw:
        sys.exit(0)

    path = normalise(raw)
    if matches(path, ALLOWED):
        sys.exit(0)
    if matches(path, PROTECTED):
        deny(
            f"Writes to {raw} are blocked by the protect-paths hook. "
            "If this is intentional, edit PROTECTED in hooks/protect-paths.py "
            "or make the change by hand outside Claude Code."
        )
    sys.exit(0)


if __name__ == "__main__":
    main()
