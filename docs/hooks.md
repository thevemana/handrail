# Hooks

Not beginner material, this is the detail for anyone who wants to know exactly what runs, when, and
how to change or remove it. See the main [README](../README.md) for the beginner-friendly version.

A hook runs outside the model, at the tool-call layer. Claude proposes a tool call, the harness runs
the hook first, the hook returns a decision, and the harness obeys it. Claude does not get a vote.

## Both hooks are off until you turn them on

Installing handrail wires the hooks up. It does not start them. Nothing fires until you say so, per
hook, in `~/.claude/handrail-hooks.json`:

```json
{
  "save-plan": true,
  "protect-paths": true
}
```

Only a hook set to exactly `true` runs. No file means none of them do. `/handrail:onboard` offers to
write this for you, and you can edit it by hand any time; the change takes effect on the next tool
call, with no reload needed.

**The switch lives in your `~/.claude/`, deliberately, and not inside the plugin.** A
marketplace-installed plugin lives in Claude Code's plugin cache, and Claude Code auto-updates
installed plugins in the background. Anything you change inside the plugin gets overwritten on the
next update, silently, and a hook you thought you had turned off comes back. Your own `~/.claude/`
is the one place an update cannot reach.

## They need Python 3 on your PATH

Skills don't. Check with `python --version`. If it errors but `python3 --version` works, edit
`hooks/hooks.json` and change `python` to `python3` in both `command` lines, then `/reload-plugins`.
On Windows, `python` is usually right; on macOS and most Linux distributions, `python3` is.

**This is the single most common install problem and it is close to invisible.** A hook whose
interpreter does not exist fails to start, and Claude Code treats a hook that fails to start as a
*non-blocking* error: it shows a small `hook error` notice in the transcript and lets the tool call
through. Only exit code 2 blocks anything. So the failure looks like a hook that ran and found
nothing to object to, which is exactly what it does not look like from the inside.

If you turned a hook on and are not sure it is running, do not infer it from the absence of
complaints. Run the demo in [Try them yourself](#try-them-yourself) below.

**No Python? Four of the five skills still work exactly as described in the main README.** You just
won't get the hooks. The one exception is `consolidate-folder`'s file-inventory helper script, which
also needs Python; the skill still runs without it, just without that one step.

**Verify the hooks before trusting them.** From a clone of the repo (the file is not part of what
gets installed):

```
git clone https://github.com/thevemana/handrail
cd handrail
python test-hooks.py
```

Expect `21/21 passed`. This runs the hook logic directly, so it proves the code works. It does not
prove the wiring works, for that, see [Try them yourself](#try-them-yourself) below.

Each of the two is described the same way in the same order, so you can scan them side by side.
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
| **What it does** | Refuses any write to `.env` and its variants (`.env.local`, `.env.production`, and similar), `*.pem`, `*.key`, `id_rsa*`, `secrets/`, `credentials`, `node_modules/` or `.git/`. `.env.example` and `.env.template` are explicitly allowed |
| **When it fires** | Before any file edit or write, once you have turned it on. Event `PreToolUse`, matcher `Edit\|Write\|NotebookEdit` |
| **What you see** | *"Writes to `<path>` are blocked by the protect-paths hook. If this is intentional, make the change by hand outside Claude Code, or set "protect-paths": false in ~/.claude/handrail-hooks.json to turn the hook off entirely."* |
| **Why you want it** | The damage from one bad write to `.env` is not the edit, it is the commit that follows it. Paths are normalised to absolute with forward slashes first, so the patterns behave the same on Windows and macOS |
| **Turning it off** | Set `"protect-paths": false` in `~/.claude/handrail-hooks.json`, or delete the file |
| **Narrowing it instead** | Edit the `PROTECTED` and `ALLOWED` lists at the top of `hooks/protect-paths.py`. Both are plain glob lists meant to be edited. See the warning below about where that file lives |

**One trap worth knowing before you edit those lists.** They are matched with `fnmatch`, where `*`
crosses `/` rather than stopping at it. A single `**/credentials*` therefore matches every file
under any directory whose name merely begins with the word, so `credentials-service/src/main.py`
becomes unwritable. That bug shipped here once. The fix is three narrow patterns rather than one
broad one, which is why the list reads `**/credentials`, `**/credentials.*` and `**/credentials/**`.

## A note on disabling

**Use `~/.claude/handrail-hooks.json`.** Setting a hook to `false`, or deleting the file, turns it
off cleanly and takes effect on the next tool call.

Three things people get wrong:

- **Editing the plugin's own files does not stick.** A marketplace install lives in Claude Code's
  plugin cache, which auto-updates in the background. An edit to `hooks/hooks.json` there survives
  until the next update and then silently reverts, bringing the hook back. Earlier versions of this
  page recommended exactly that. It was wrong.
- **Deleting the `.py` file is not how you turn a hook off either.** The entry in `hooks/hooks.json`
  is what wires it up. Without the script it just fails, and a failing hook is noise rather than
  absence.
- **You do not need a reload to change the config file.** The hooks read it on every call. Reloads
  are only needed if you change `hooks/hooks.json` itself.

**Turning off both, keeping the skills.** Delete `~/.claude/handrail-hooks.json`. That is the
default state anyway. The skills are unaffected, since nothing references the hooks.

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
something, the two hooks describe what must not happen.

An earlier build shipped a third hook that refused commits carrying an AI co-author trailer. It was
cut, on this same test: a trailer in your commit metadata costs a correction, not real damage, so by
the plugin's own rule it was a `CLAUDE.md` line wearing a hook's clothes. If you want that behaviour,
the native setting is `attribution.commit: ""` in `settings.json`, which needs no plugin at all.

## Try them yourself

Two things to type, each with what you should see, because a silently broken hook looks exactly
like nothing happening. **Turn the hooks on first**, or the correct result is nothing happening and
you learn nothing.

**1. Watch a hook refuse you.** With `"protect-paths": true` set, ask Claude to write something to a
file called `.env`:

```
Create a .env file in this folder with API_KEY=test
```

*You should see:* a refusal, not a file. The message begins *"Writes to ... are blocked by the
protect-paths hook."* If a `.env` file appears instead, the hook is not wired up. See
[Troubleshooting](#troubleshooting) below.

**2. Watch a plan stop.** With `"save-plan": true` set, Ask Claude to plan something non-trivial, and approve the plan.

*You should see:* the turn end immediately, with *"Plan saved to plans/.... Say the word when ready
to execute."* No implementation starts. There should be a new dated file in `plans/`. Saying "go
ahead" is what starts the work.

## Troubleshooting

**Telling a working hook from a silently broken one.** This is the important one. A hook with a wrong
path does nothing at all, which is indistinguishable from a hook that is working and simply has not
found anything to object to. The only reliable check is to make one fire on purpose, using the `.env`
test above. A refusal means the wiring is good. A created file means it is not. `python
test-hooks.py` passing `21/21` tells you the logic is sound but says nothing about whether Claude
Code is calling it. The two failures look identical from the outside, which is why both checks are
worth running.

**Check the config file before blaming the wiring.** Since both hooks are off by default, the first
question when one does not fire is whether `~/.claude/handrail-hooks.json` exists and sets it to
exactly `true`. A missing file, a typo in the hook name, or `"true"` as a string rather than a
boolean all read as off. That is a far more likely explanation than broken wiring.
