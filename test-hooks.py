#!/usr/bin/env python3
"""Test the hooks without installing them. Run: python test-hooks.py

Feeds each hook the same stdin payload Claude Code sends and checks the decision.
Passing here means the logic is right. It does not mean hooks.json is wired
correctly, which only a live session proves.

The co-author trailer is assembled at runtime rather than written literally, so
this file does not itself trip a trailer-blocking hook.
"""
import json
import os
import subprocess
import sys

HOOKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hooks")
TRAILER = "Co-Authored-By" + ": Claude <noreply@anthropic.com>"

# (script, tool_input, should_deny, label)
CASES = [
    ("protect-paths.py", {"file_path": "/proj/.env"}, True, "protected .env"),
    ("protect-paths.py", {"file_path": "/proj/.env.local"}, True, "protected .env.local"),
    ("protect-paths.py", {"file_path": "/proj/certs/server.pem"}, True, "protected .pem"),
    ("protect-paths.py", {"file_path": "/proj/secrets/db.yaml"}, True, "protected secrets dir"),
    ("protect-paths.py", {"file_path": "/proj/.env.example"}, False, "allow-listed .env.example"),
    ("protect-paths.py", {"file_path": "/proj/src/app.py"}, False, "ordinary source file"),
    ("protect-paths.py", {}, False, "no file_path in payload"),

    ("block-ai-trailer.py", {"command": f'git commit -m "x\n\n{TRAILER}"'}, True,
     "commit carrying the trailer"),
    ("block-ai-trailer.py", {"command": f'git commit -am "x\n\n{TRAILER}"'}, True,
     "commit -am carrying the trailer"),
    ("block-ai-trailer.py", {"command": f'git -c user.name=x commit -m "x\n\n{TRAILER.lower()}"'},
     True, "global flags before subcommand, lowercased trailer"),
    ("block-ai-trailer.py", {"command": 'git commit -m "clean message"'}, False, "clean commit"),
    ("block-ai-trailer.py", {"command": f'git log --format=%B | grep "{TRAILER}"'}, False,
     "reading history for the trailer stays allowed"),
    ("block-ai-trailer.py", {"command": "git log --grep=commit --format=%B"}, False,
     "the word commit inside a flag value"),
    ("block-ai-trailer.py", {"command": f'echo "{TRAILER}" > notes.txt'}, False,
     "non-git command that merely mentions it"),
]


def run(script, tool_input, extra=None):
    payload = {"tool_input": tool_input}
    if extra:
        payload.update(extra)
    return subprocess.run([sys.executable, os.path.join(HOOKS, script)],
                          input=json.dumps(payload), capture_output=True, text=True)


def check(label, ok, failures):
    print(f"{'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        failures.append(label)


def main():
    failures = []

    for script, tool_input, should_deny, label in CASES:
        out = run(script, tool_input)
        check(f"{script:22} {label}", ('"deny"' in out.stdout) == should_deny, failures)

    # A crashing hook must fail open, or a bug in it locks you out of your tools.
    for script in ("protect-paths.py", "block-ai-trailer.py"):
        out = subprocess.run([sys.executable, os.path.join(HOOKS, script)],
                             input="not json at all", capture_output=True, text=True)
        ok = out.returncode == 0 and '"deny"' not in out.stdout
        check(f"{script:22} fails open on malformed stdin", ok, failures)

    # save-plan.py: writes the plan, and always returns the hard stop.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        plan = "# Plan: test the save hook\n\n## Goal\nProve it writes."
        out = run("save-plan.py", {"plan": plan}, extra={"cwd": tmp})
        try:
            control = json.loads(out.stdout)
        except (json.JSONDecodeError, ValueError):
            control = {}
        written = os.listdir(os.path.join(tmp, "plans")) if os.path.isdir(os.path.join(tmp, "plans")) else []
        check("save-plan.py           writes a slugged file into plans/",
              any(f.endswith("-test-the-save-hook.md") for f in written), failures)
        check("save-plan.py           returns the hard stop (continue: false)",
              control.get("continue") is False, failures)

        # Re-approving the identical plan must not create a duplicate.
        run("save-plan.py", {"plan": plan}, extra={"cwd": tmp})
        again = os.listdir(os.path.join(tmp, "plans"))
        check("save-plan.py           skips an identical re-approval",
              len(again) == len(written), failures)

        # A malformed payload must still return the hard stop, never swallow it.
        out = subprocess.run([sys.executable, os.path.join(HOOKS, "save-plan.py")],
                             input="not json", capture_output=True, text=True)
        try:
            control = json.loads(out.stdout)
        except (json.JSONDecodeError, ValueError):
            control = {}
        check("save-plan.py           still stops the turn on malformed stdin",
              control.get("continue") is False, failures)

    total = len(CASES) + 2 + 4
    print(f"\n{total - len(failures)}/{total} passed")
    for f in failures:
        print(f"  failed: {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
