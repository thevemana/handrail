# Hooks

Not beginner material, this is the detail for anyone who wants to know exactly what runs, when, and
how to change or remove it. See the main [README](../README.md) for the beginner-friendly version.

A hook runs outside the model, at the tool-call layer. Claude proposes a tool call, the harness runs
the hook first, the hook returns a decision, and the harness obeys it. Claude does not get a vote.

**They need Python 3 on your PATH.** Skills don't. Check with `python --version`. If it errors but
`python3 --version` works, edit `hooks/hooks.json` and change `python` to `python3` in all three
`command` lines, then `/reload-plugins`. On Windows, `python` is usually right; on macOS and most
Linux distributions, `python3` is. This is the single most common install problem, and it's
invisible: a hook whose interpreter doesn't exist fails to start, and a hook that fails to start
blocks nothing.

**No Python? Four of the five skills still work exactly as described in the main README.** You just
won't get these three hooks. The one exception is `consolidate-folder`'s file-inventory helper
script, which also needs Python; the skill still runs without it, just without that one step.

**Verify the hooks before trusting them:**

```
python test-hooks.py
```

Expect `20/20 passed`. This runs the hook logic directly, so it proves the code works. It does not
prove the wiring works, for that, see [Try them yourself](#try-them-yourself) below.

Each of the three is described the same way in the same order, so you can scan them side by side.
The **Event** and matcher named in each row are Claude Code's own trigger point and tool filter,
useful mainly for finding the right block in `hooks/hooks.json` if you want to change one. The
**When it fires** description in plain English is the part that matters day to day.

## `save-plan.py`, the one to keep if you keep only one

| | |
|---|---|
| **What it does** | Saves an approved plan to `plans/YYYY-MM-DD-<slug>.md`, then ends the turn |
| **When it fires** | The moment you approve a plan. Event `PostToolUse`, matcher `ExitPlanMode` |
| **What you see** | *"Plan saved to plans/2026-08-02-your-plan.md. Say the word when ready to execute."* and the turn stops. A re-approved identical plan says *"Plan already saved (identical)"* rather than writing a second copy |
| **Why you want it** | Without it, "yes, that plan is right" and "go build it" are the same keystroke, which is only what you meant some of the time. It also means every approved plan exists as a file you can come back to next week |
| **Turning it off** | Delete the `PostToolUse` block from `hooks/hooks.json`. **Or turn off half of it:** delete the three `control` keys at the top of `main()` in `hooks/save-plan.py` to keep the plan-saving and drop only the stop |

The slug comes from the plan's own `# Plan:` heading. Two plans with the same title on the same day
get `-b`, `-c`, and so on.

## `protect-paths.py`, which refuses writes to files you never want touched

| | |
|---|---|
| **What it does** | Refuses any write to `.env` and its variants (`.env.local`, `.env.production`, and similar), `*.pem`, `*.key`, `id_rsa*`, `secrets/`, `credentials*`, `node_modules/` or `.git/`. `.env.example` and `.env.template` are explicitly allowed |
| **When it fires** | Before any file edit or write. Event `PreToolUse`, matcher `Edit\|Write\|NotebookEdit` |
| **What you see** | *"Writes to `<path>` are blocked by the protect-paths hook. If this is intentional, edit PROTECTED in hooks/protect-paths.py or make the change by hand outside Claude Code."* |
| **Why you want it** | The damage from one bad write to `.env` is not the edit, it is the commit that follows it. Paths are normalised to absolute with forward slashes first, so the patterns behave the same on Windows and macOS |
| **Turning it off** | Delete its block from `hooks/hooks.json`. More useful: edit the `PROTECTED` and `ALLOWED` lists at the top of `hooks/protect-paths.py`, both plain glob lists meant to be edited |

## `block-ai-trailer.py`, which keeps AI attribution out of commit metadata

| | |
|---|---|
| **What it does** | Refuses a `git commit` whose message carries a `Co-Authored-By: Claude` trailer, including one hidden in a `-F` or `--file` message file |
| **When it fires** | Before any shell command that creates a commit. Event `PreToolUse`, matcher `Bash\|PowerShell` |
| **What you see** | *"This commit message carries an AI co-author trailer, which this project does not use. Credit AI in the README or a tech-stack section... Remove the trailer and re-run the commit."* |
| **Why you want it** | If you would rather credit AI once in your README than in every commit's metadata forever. Reading history for the trailer stays allowed on purpose, since `git log \| grep Co-Authored-By` is how you find out whether you already have hundreds of them |
| **Turning it off** | Delete its `Bash\|PowerShell` block from `hooks/hooks.json` |

If you want this behaviour without a hook, the native setting is `attribution.commit: ""` in
`settings.json`. This hook is the backstop for a hand-written trailer or a settings file that gets
reverted.

## A note on disabling

Two things people get wrong:

- **Deleting the `.py` file is not how you turn a hook off.** The entry in `hooks/hooks.json` is what
  wires it up. Without the script it just fails, and a failing hook is noise rather than absence.
  Delete the block from `hooks/hooks.json`.
- **Re-enabling needs a reload.** Restore the block, then run `/reload-plugins` or restart. Skipping
  that step is the usual reason someone concludes the hook is broken.

**Turning off all three, keeping the skills.** Replace the contents of `hooks/hooks.json` with `{}`,
then `/reload-plugins`. The skills are unaffected, since nothing references the hooks.

## Why hooks and not just instructions

You can write rules in `CLAUDE.md` and Claude will mostly follow them. Mostly is the problem.

Anthropic's own documentation puts it plainly: *"Unlike CLAUDE.md instructions which are advisory,
hooks are deterministic and guarantee the action happens."* Adherence also gets worse as the file
grows, because the chance a session honours **every** rule falls as you add rules. A long instruction
file is not a safety mechanism.

So the split is:

- **A rule where being ignored costs a correction** belongs in `CLAUDE.md`. Cheap to write, fine at
  advisory reliability.
- **A rule where being ignored once causes real damage** belongs in a hook. Committing a secret,
  pushing to main, deleting data, overwriting a file you needed.

That is the same test used to decide what went in this plugin. The five skills describe how to do
something, the three hooks describe what must not happen.

## Try them yourself

Three things to type, each with what you should see, because a silently broken hook looks exactly
like nothing happening.

**1. Watch a hook refuse you.** Ask Claude to write something to a file called `.env`:

```
Create a .env file in this folder with API_KEY=test
```

*You should see:* a refusal, not a file. The message begins *"Writes to ... are blocked by the
protect-paths hook."* If a `.env` file appears instead, the hook is not wired up. See
[Troubleshooting](#troubleshooting) below.

**2. Watch the commit hook.** In a git repo with something staged, ask for a commit message carrying
`Co-Authored-By: Claude <noreply@anthropic.com>`.

*You should see:* the commit denied, with a message explaining the project does not use AI co-author
trailers. Note what is *not* blocked: `git log | grep Co-Authored-By` still runs fine, because
auditing for the trailer is how you find out whether you have the problem.

**3. Watch a plan stop.** Ask Claude to plan something non-trivial, and approve the plan.

*You should see:* the turn end immediately, with *"Plan saved to plans/.... Say the word when ready
to execute."* No implementation starts. There should be a new dated file in `plans/`. Saying "go
ahead" is what starts the work.

## Troubleshooting

**Telling a working hook from a silently broken one.** This is the important one. A hook with a wrong
path does nothing at all, which is indistinguishable from a hook that is working and simply has not
found anything to object to. The only reliable check is to make one fire on purpose, using the `.env`
test above. A refusal means the wiring is good. A created file means it is not. `python
test-hooks.py` passing `20/20` tells you the logic is sound but says nothing about whether Claude
Code is calling it. The two failures look identical from the outside, which is why both checks are
worth running.

**If you already run your own AI-trailer hook globally,** this plugin's will run alongside it and
both will deny the same commit. That is harmless, since two denials are one denial, but the doubled
message reads like a bug if nobody tells you. Drop whichever copy you prefer.
