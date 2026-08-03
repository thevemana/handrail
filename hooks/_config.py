#!/usr/bin/env python3
"""Shared opt-in check for handrail's hooks.

Both hooks ship wired but dormant. Nothing fires until you say so, per hook, in
`~/.claude/handrail-hooks.json`:

    {
      "protect-paths": true,
      "save-plan": true
    }

No file, or a missing key, or anything other than `true`, means off. `/handrail:onboard`
offers to write this file for you; you can also create it by hand.

**Why the toggle lives here and not in `hooks/hooks.json`.** A marketplace-installed
plugin lives in Claude Code's plugin cache, and Claude Code auto-updates installed
plugins in the background. Anything you edit inside the plugin gets overwritten on the
next update, silently, and the hook you thought you turned off comes back. This file is
in your own `~/.claude/`, so an update cannot touch it.

Set HANDRAIL_HOOKS_CONFIG to point the check at a different file. The test suite uses
this; there is no other reason to.
"""
import json
import os


def config_path():
    override = os.environ.get("HANDRAIL_HOOKS_CONFIG")
    if override:
        return override
    return os.path.join(os.path.expanduser("~"), ".claude", "handrail-hooks.json")


def enabled(name):
    """True only if the config file exists and sets this hook to exactly true.

    Every failure mode returns False. A missing file, unreadable file, malformed
    JSON or absent key all mean "not turned on", which is the safe reading: a
    guard nobody asked for should not start guarding because a file was corrupt.
    """
    try:
        with open(config_path(), encoding="utf-8") as f:
            cfg = json.load(f)
    except (OSError, ValueError):
        return False
    return isinstance(cfg, dict) and cfg.get(name) is True
