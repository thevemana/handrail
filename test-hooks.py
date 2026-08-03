#!/usr/bin/env python3
"""Test the hooks without installing them. Run: python test-hooks.py

Feeds each hook the same stdin payload Claude Code sends and checks the decision.
Passing here means the logic is right. It does not mean hooks.json is wired
correctly, which only a live session proves.

Both hooks are opt-in, so every behavioural case below runs against a temporary
config file that turns them on. The opt-in gate itself is tested separately, at
the end, because "the hook did nothing" is the correct answer there and the wrong
answer everywhere else.
"""
import json
import os
import subprocess
import sys
import tempfile

HOOKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hooks")

# (script, tool_input, should_deny, label)
CASES = [
    ("protect-paths.py", {"file_path": "/proj/.env"}, True, "protected .env"),
    ("protect-paths.py", {"file_path": "/proj/.env.local"}, True, "protected .env.local"),
    ("protect-paths.py", {"file_path": "/proj/certs/server.pem"}, True, "protected .pem"),
    ("protect-paths.py", {"file_path": "/proj/secrets/db.yaml"}, True, "protected secrets dir"),
    ("protect-paths.py", {"file_path": "/proj/.env.example"}, False, "allow-listed .env.example"),
    ("protect-paths.py", {"file_path": "/proj/src/app.py"}, False, "ordinary source file"),
    ("protect-paths.py", {}, False, "no file_path in payload"),
    ("protect-paths.py", {"notebook_path": "/proj/secrets/notes.ipynb"}, True,
     "NotebookEdit uses notebook_path, not file_path"),
    ("protect-paths.py", {"notebook_path": "/proj/analysis.ipynb"}, False,
     "ordinary notebook (true negative for the notebook path)"),

    # Regression guards for the fnmatch over-block. `*` crosses `/` in fnmatch, so
    # a single "**/credentials*" made every project directory whose name merely
    # starts with the word entirely unwritable. The third case is the one that
    # used to fail.
    ("protect-paths.py", {"file_path": "/proj/credentials.json"}, True, "credentials.json"),
    ("protect-paths.py", {"file_path": "/proj/credentials/db.yaml"}, True, "credentials/ dir"),
    ("protect-paths.py", {"file_path": "/dev/credentials-service/src/main.py"}, False,
     "credentials-service is an ordinary project, not a secret"),
]


def run(script, tool_input, extra=None, config=None):
    payload = {"tool_input": tool_input}
    if extra:
        payload.update(extra)
    env = dict(os.environ)
    env["HANDRAIL_HOOKS_CONFIG"] = config if config else os.devnull
    return subprocess.run([sys.executable, os.path.join(HOOKS, script)],
                          input=json.dumps(payload), capture_output=True, text=True,
                          env=env)


def raw(script, stdin, config=None):
    env = dict(os.environ)
    env["HANDRAIL_HOOKS_CONFIG"] = config if config else os.devnull
    return subprocess.run([sys.executable, os.path.join(HOOKS, script)],
                          input=stdin, capture_output=True, text=True, env=env)


def check(label, ok, failures):
    print(f"{'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        failures.append(label)


def write_config(directory, **flags):
    path = os.path.join(directory, "handrail-hooks.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(flags, f)
    return path


def main():
    failures = []

    with tempfile.TemporaryDirectory() as tmp:
        on = write_config(tmp, **{"protect-paths": True, "save-plan": True})

        for script, tool_input, should_deny, label in CASES:
            out = run(script, tool_input, config=on)
            check(f"{script:22} {label}", ('"deny"' in out.stdout) == should_deny, failures)

        # A crashing hook must fail open, or a bug in it locks you out of your tools.
        out = raw("protect-paths.py", "not json at all", config=on)
        check("protect-paths.py       fails open on malformed stdin",
              out.returncode == 0 and '"deny"' not in out.stdout, failures)

        # save-plan.py: writes the plan, and always returns the hard stop.
        plans = os.path.join(tmp, "proj")
        plan = "# Plan: test the save hook\n\n## Goal\nProve it writes."
        out = run("save-plan.py", {"plan": plan}, extra={"cwd": plans}, config=on)
        try:
            control = json.loads(out.stdout)
        except (json.JSONDecodeError, ValueError):
            control = {}
        written = os.listdir(os.path.join(plans, "plans")) if os.path.isdir(os.path.join(plans, "plans")) else []
        check("save-plan.py           writes a slugged file into plans/",
              any(f.endswith("-test-the-save-hook.md") for f in written), failures)
        check("save-plan.py           returns the hard stop (continue: false)",
              control.get("continue") is False, failures)

        # Re-approving the identical plan must not create a duplicate.
        run("save-plan.py", {"plan": plan}, extra={"cwd": plans}, config=on)
        again = os.listdir(os.path.join(plans, "plans"))
        check("save-plan.py           skips an identical re-approval",
              len(again) == len(written), failures)

        # A malformed payload must still return the hard stop, never swallow it.
        out = raw("save-plan.py", "not json", config=on)
        try:
            control = json.loads(out.stdout)
        except (json.JSONDecodeError, ValueError):
            control = {}
        check("save-plan.py           still stops the turn on malformed stdin",
              control.get("continue") is False, failures)

        behavioural = len(CASES) + 5

        # --- The opt-in gate. Doing nothing is the pass condition here. ---
        off = write_config(tmp, **{"protect-paths": False, "save-plan": False})
        missing = os.path.join(tmp, "no-such-file.json")

        gate = [
            ("protect-paths.py", missing, "no config file at all"),
            ("protect-paths.py", off, "config present, set to false"),
        ]
        for script, cfg, label in gate:
            out = run(script, {"file_path": "/proj/.env"}, config=cfg)
            check(f"{script:22} stays out of the way: {label}",
                  out.returncode == 0 and '"deny"' not in out.stdout, failures)

        quiet = os.path.join(tmp, "quiet")
        for cfg, label in ((missing, "no config file at all"), (off, "config present, set to false")):
            out = run("save-plan.py", {"plan": plan}, extra={"cwd": quiet}, config=cfg)
            silent = out.returncode == 0 and "continue" not in out.stdout
            unwritten = not os.path.isdir(os.path.join(quiet, "plans"))
            check(f"save-plan.py           stays out of the way: {label}",
                  silent and unwritten, failures)

        total = behavioural + len(gate) + 2

    print(f"\n{total - len(failures)}/{total} passed")
    for f in failures:
        print(f"  failed: {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
