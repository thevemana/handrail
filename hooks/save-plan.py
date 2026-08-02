#!/usr/bin/env python3
"""PostToolUse hook for ExitPlanMode: save the approved plan, then stop.

Two jobs:

1. **Snapshot.** Writes the plan to `<project>/plans/YYYY-MM-DD-<slug>.md` the
   moment it is approved, with the slug taken from the plan's own `# Plan:`
   heading. Same-title-same-day collisions get -b, -c, and so on. Identical
   re-approvals are skipped rather than duplicated. The text is read straight
   from the tool input, so this does not depend on where Claude Code stages its
   own auto-save.

2. **Hard stop.** Returns `continue: false`, which ends the turn the instant a
   plan is approved. Approving a plan never silently starts the implementation.
   You decide when to trigger execution, in that session or a later one.

The second job is the one worth having. Without it, "yes, that plan looks right"
and "go build it" are the same keystroke, which is only what you wanted some of
the time. Delete the three `control` keys below if you would rather it just save.
"""
import datetime
import json
import os
import re
import sys


def derive_slug(plan):
    title = None
    for line in plan.splitlines():
        m = re.match(r"^#\s*Plan:\s*(.+)$", line.strip(), re.IGNORECASE)
        if m:
            title = m.group(1)
            break
    if not title:
        for line in plan.splitlines():
            s = line.strip()
            if s.startswith("#"):
                title = s.lstrip("#").strip()
                break
    if not title:
        title = "plan"
    # Drop trailing metadata after a dash, pipe, or middot.
    title = re.split(r"[—|·]", title)[0].strip()
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    words = [w for w in slug.split("-") if w][:8]
    return "-".join(words) or "plan"


def target_path(plans_dir, base, plan):
    """Path to write, or None if an identical snapshot already exists."""
    primary = os.path.join(plans_dir, base + ".md")
    existing = [primary] if os.path.exists(primary) else []
    for c in "bcdefghijklmnopqrstuvwxyz":
        p = os.path.join(plans_dir, "{}-{}.md".format(base, c))
        if os.path.exists(p):
            existing.append(p)
        else:
            break
    for p in existing:
        try:
            with open(p, encoding="utf-8") as f:
                if f.read() == plan:
                    return None
        except OSError:
            pass
    if not os.path.exists(primary):
        return primary
    for c in "bcdefghijklmnopqrstuvwxyz":
        p = os.path.join(plans_dir, "{}-{}.md".format(base, c))
        if not os.path.exists(p):
            return p
    stamp = datetime.datetime.now().strftime("%H%M%S")
    return os.path.join(plans_dir, "{}-{}.md".format(base, stamp))


def main():
    control = {
        "continue": False,
        "stopReason": "Plan approved and saved to plans/. Execution is paused. "
                      "Say when you want me to proceed.",
        "systemMessage": "Plan saved to plans/. Say the word when ready to execute.",
    }
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        data = {}

    try:
        plan = (data.get("tool_input", {}) or {}).get("plan", "") or ""
        if plan.strip():
            project_dir = (data.get("cwd")
                           or os.environ.get("CLAUDE_PROJECT_DIR")
                           or os.getcwd())
            plans_dir = os.path.join(project_dir, "plans")
            os.makedirs(plans_dir, exist_ok=True)
            base = "{}-{}".format(datetime.date.today().strftime("%Y-%m-%d"),
                                  derive_slug(plan))
            path = target_path(plans_dir, base, plan)
            if path is None:
                control["systemMessage"] = "Plan already saved (identical). Execution paused."
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(plan)
                control["systemMessage"] = (
                    "Plan saved to plans/{}. Say the word when ready to execute."
                    .format(os.path.basename(path)))
    except Exception as e:  # a snapshot failure must not swallow the hard stop
        control["systemMessage"] = "Plan approved (save failed: {}). Execution paused.".format(e)

    sys.stdout.write(json.dumps(control))


if __name__ == "__main__":
    main()
