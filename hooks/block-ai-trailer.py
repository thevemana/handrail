#!/usr/bin/env python3
"""PreToolUse hook for Bash and PowerShell: block AI co-author trailers on commits.

Claude Code's default behaviour is to append a `Co-Authored-By: Claude` trailer
to commit messages. If you would rather credit AI in your README than in every
commit's metadata, the native fix is `attribution.commit: ""` in settings.json.
This hook is the backstop for a hand-written trailer, an older client, or a
settings file that gets reverted.

Why a hook and not a line in CLAUDE.md: an instruction competing against a live
harness default is a coin flip. This runs outside the model and cannot be skipped.

Scope: fires only when the command actually creates a commit. Reading history for
the trailer (`git log | grep Co-Authored-By`) stays allowed, since auditing for it
is how you find out whether you have the problem.
"""
import json
import os
import re
import sys

# Any tokens may sit between `git` and `commit`, so global flags like
# `git -c user.name=x commit` are still caught. Requiring whitespace directly
# before `commit` keeps `git log --grep=commit` from matching. Erring toward
# over-matching is deliberate: a false deny costs one retry, a false allow lets
# the trailer through, which is the thing this exists to prevent.
IS_COMMIT = re.compile(r"\bgit\b(?:\s+\S+)*?\s+commit\b")

TRAILER = re.compile(
    r"Co-?Authored-?By\s*:\s*[^\n]*"
    r"(?:Claude|Anthropic|noreply@anthropic\.com)",
    re.IGNORECASE,
)

# -F <path> / --file=<path> put the message in a file that the command text
# alone does not reveal, so resolve and scan those too.
MSG_FILE = re.compile(r"(?:-F|--file)(?:[=\s]+)(\"[^\"]+\"|'[^']+'|[^\s]+)")

REASON = (
    "This commit message carries an AI co-author trailer, which this project does "
    "not use. Credit AI in the README or a tech-stack section, where a reader "
    "looks for it, rather than in per-commit metadata. Remove the trailer and "
    "re-run the commit. To change this policy, edit or remove "
    "hooks/block-ai-trailer.py in the handrail plugin."
)


def unquote(token):
    if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'":
        return token[1:-1]
    return token


def message_file_text(command):
    """Read any -F/--file message files so a trailer hidden in one still trips."""
    chunks = []
    for match in MSG_FILE.finditer(command):
        path = unquote(match.group(1))
        if not path or path == "-":
            continue
        try:
            with open(os.path.expanduser(path), "r", encoding="utf-8",
                      errors="replace") as f:
                chunks.append(f.read())
        except OSError:
            continue
    return "\n".join(chunks)


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8", errors="replace"))
    except (json.JSONDecodeError, ValueError):
        print(json.dumps({}))  # never block on a hook bug
        return

    command = (data.get("tool_input", {}) or {}).get("command") or ""
    if not command or not IS_COMMIT.search(command):
        print(json.dumps({}))
        return

    if TRAILER.search(command + "\n" + message_file_text(command)):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": REASON,
            }
        }))
        return

    print(json.dumps({}))


if __name__ == "__main__":
    main()
