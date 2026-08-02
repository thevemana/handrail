# handrail

Something to hold onto while you learn Claude Code. Six **skills** (commands you type as
`/handrail:name`, which Claude reads and follows) write and refine your global **CLAUDE.md** (the
file Claude reads at the start of every session for how you want it to work), capture new rules the
moment they come up, and give a project a memory that survives between sessions. Three **hooks**
(small scripts that run automatically, outside the model, at points Claude Code exposes) enforce a
few rules that a file of instructions can only politely request.

Everything here is optional and everything here is editable. Once installed, these files are yours.

---

## Why is this useful?

Seven situations, each one the reason a specific piece of this exists.

**Mid-conversation, you say "always do it this way from now on," and it evaporates the moment the
session ends.** `codify` catches that sentence, asks a few short questions to make it a well-formed
rule instead of a raw quote, and routes it to the right home on its own: your global CLAUDE.md, a
project's, a scoped rule file, or a flag that it actually needs a hook instead.

**You install Claude Code and don't know what to put in `CLAUDE.md`.** A blank file gives you
nothing, a full template asks you to already know what you want. `onboard` interviews you a few
questions at a time and writes a real, personal first file instead.

**Weeks later, you've actually installed hooks and skills, and your CLAUDE.md still says none of
it exists.** `onboard` deliberately leaves the enforcement map and extension sections thin, because
nothing was real yet. `harden` comes back once something is, and records what's actually enforced
versus what's still just written down.

**You finish a session, and next time Claude has forgotten everything.** Not just the code, the
decisions. Why you rejected the obvious approach, what you already tried that did not work, what you
were about to do next. You re-explain it, or you re-derive it. `wrap` writes it down before the
session ends.

**You open a folder you have not touched in three months and Claude starts from zero.** It reads the
code fine, but the code does not say what the conventions are or which file is the one that matters.
`scaffold` gives the folder four small files that carry that between sessions.

**Eleven documents about the same thing, and no way to tell which one is current.** Somewhere in
there two of them contradict each other, and finding that out later is expensive.
`consolidate-folder` merges them and says exactly where they disagree.

**You approve a plan and it immediately starts building**, when you only meant *yes, that is right*.
There was no keystroke that meant one without the other. The `save-plan` hook makes approving a plan
save it and stop, so starting the work is a separate decision you make out loud.

---

## Install

**Before you start:** you need Python 3 on your PATH (check with `python --version`; the hooks need
it, the skills don't) and nothing else. `thevemana/handrail` is a public GitHub repo, so no account
or login is required beyond having Claude Code itself running.

Type both of these **inside a running Claude Code session** (they're Claude Code's own `/` commands,
not something you run in your regular terminal):

```
/plugin marketplace add thevemana/handrail
/plugin install handrail@thevemana
```

Then **restart Claude Code**, or run `/reload-plugins`. The skills will not appear until you do, and
this is the single most common reason someone concludes the install failed.

What to expect at each step:

| Step | What you should see |
|---|---|
| `marketplace add` | A confirmation naming the marketplace `thevemana` and the plugins it found (one: `handrail`) |
| `install` | A confirmation that `handrail` is installed, and a prompt to restart or reload |
| after the restart | Typing `/handrail` offers `onboard`, `harden`, `codify`, `wrap`, `scaffold` and `consolidate-folder` |

The install form is `<plugin>@<marketplace>`, not a bare plugin name. Here that is
`handrail@thevemana`: the plugin, then where it came from.

If `python --version` errors but `python3 --version` works, see
[Requirements and troubleshooting](#requirements-and-troubleshooting) before going further. A hook
that cannot start is silent about it.

Verify the hooks before trusting them:

```
python test-hooks.py
```

Expect `20/20 passed`. This runs the hook logic directly, so it proves the code works. It does not
prove the wiring works. For that, see the live checks in the next section.

---

## How do I play with it?

Five minutes, nine things to type. Each one says what you should see, because a silently broken
hook looks exactly like nothing happening.

**1. Write your global CLAUDE.md.** If you don't have one yet, or only have a thin first attempt:

```
/handrail:onboard
```

*You should see:* it checks what's already at `~/.claude/CLAUDE.md` first, then asks a handful of
questions in short rounds rather than handing you a blank template. It shows you the full draft
before writing anything. A blank file or a rough handful of lines both still get the normal
interview; it only refuses once the file looks genuinely lived-in, and then it offers to help with
one section instead of a rewrite. That refusal is a feature, so try it on purpose.

**2. Fill in what's already enforced.** Right after installing, the plugin's own three hooks are
real enforcement with nothing recorded about them yet. This is exactly what `harden` fills in first:

```
/handrail:harden
```

*You should see:* it reads `~/.claude/settings.json`, finds this plugin's own three hooks
(save-plan, protect-paths, block-ai-trailer), and proposes enforcement-map rows describing them
without asking you anything about hooks you didn't have to describe yourself. It shows the diff to
your CLAUDE.md's §2 and §8 before writing, not the whole file.

**3. Catch a rule on the fly.** Anywhere, mid-conversation, say something like:

```
From now on, always show a diff before editing a file in this repo.
```

*You should see:* it asks a few short questions (does this apply everywhere or just here, what
would a miss actually cost) rather than pasting your sentence straight into a file, then tells you
where it's landing before writing anything.

**4. Scaffold a project.** Pick any project folder, open Claude Code there, and type:

```
/handrail:scaffold
```

*You should see:* it lists the folder first and asks about anything it cannot infer, then writes
`CLAUDE.md`, `MEMORY.md`, `tasks.md` and an empty `plans/`. Open `CLAUDE.md`. It should describe
conventions your folder actually uses, not a generic template. If it reads generic, tell it what it
missed. The file is yours to correct.

**5. End a session properly.** Do a bit of real work first, then:

```
/handrail:wrap
```

*You should see:* a new file under `_wraps/`, named `YYYYMMDD-wrap-<title>.md`, plus a short summary
in chat naming where it landed. Open the file and read the **What Went Wrong** table. That is the
section that pays for itself, because a recorded dead end stops you walking into it twice.

**6. Consolidate a folder of notes.** Point it at a folder you already have:

```
/handrail:consolidate-folder ~/notes/some-project
```

*You should see:* a file manifest first, before any reading happens, listing what is in scope. Then
one long document. **Read the contradictions section first.** That is the part you could not have
got by reading the files yourself.

**7. Watch a hook refuse you.** Ask Claude to write something to a file called `.env`:

```
Create a .env file in this folder with API_KEY=test
```

*You should see:* a refusal, not a file. The message begins *"Writes to … are blocked by the
protect-paths hook."* If a `.env` file appears instead, the hook is not wired up. Go to
[troubleshooting](#requirements-and-troubleshooting).

**8. Watch the commit hook.** In a git repo with something staged, ask for a commit message carrying
`Co-Authored-By: Claude <noreply@anthropic.com>`.

*You should see:* the commit denied, with a message explaining the project does not use AI co-author
trailers. Note what is *not* blocked: `git log | grep Co-Authored-By` still runs fine, because
auditing for the trailer is how you find out whether you have the problem.

**9. Watch a plan stop.** Ask Claude to plan something non-trivial, and approve the plan.

*You should see:* the turn end immediately, with *"Plan saved to plans/…. Say the word when ready to
execute."* No implementation starts. There should be a new dated file in `plans/`. Saying "go ahead"
is what starts the work.

---

## The six skills

### `/handrail:onboard`

**Reach for it when** you install Claude Code and have no global `~/.claude/CLAUDE.md` yet, or
only a rough first attempt.

Interviews you in five short rounds instead of handing you a blank template: who you are and what
you're using it for, what should never happen without a stop, how much you want to see before
Claude acts, how you want it to talk to you, and whether you already keep any kind of running
notes. Skips any round that produces nothing usable rather than padding the file with a generic
placeholder, and shows the full draft before writing it. Refuses to overwrite a file that already
looks lived-in.

### `/handrail:harden`

**Reach for it when** `onboard` just wrote your CLAUDE.md. Run it in the same session, not
someday: this plugin's own three hooks are already installed the moment handrail is, so there's
real content to document from the start. Come back to it again later whenever a new hook or skill
gets added and the file should catch up.

Reads `~/.claude/settings.json` and `~/.claude/skills/` first, so it can propose enforcement-map
rows for hooks you already have without asking you to describe them yourself. Only asks about what
the survey couldn't answer on its own. Shows the diff to the two sections it touches, not the whole
file, and names any guardrail that still has no real enforcement behind it rather than marking it
`Instruction` quietly. It documents enforcement; it does not build a hook for you.

### `/handrail:codify`

**Reach for it when** you just told Claude "always do it this way" or "make this a rule," and
don't want it to evaporate at the end of the session.

Interviews the statement into five parts (scope, trigger, the rule itself, an exception, and what
following it should look like), then routes it to whichever of four homes actually fits: your
global CLAUDE.md if it applies everywhere, a `~/.claude/rules/` file if it's tied to a file
pattern, a project's own CLAUDE.md if it's scoped to just that project, or a plain refusal to
write anything if the answers reveal this should be a hook instead. That last case is the point:
a rule that would cost real damage if missed doesn't get written as a polite request.

### `/handrail:wrap`

**Reach for it when** a session is ending and you want the next one to start warm.

Writes a dated record of what was done, what was decided **and why**, what is unfinished, and the one
specific next action. Then it reconciles your task list, closing items on the line with a done-date
rather than describing them as finished in a paragraph, updates any plan file the work advanced, and
verifies its own claims against disk before reporting.

That last part matters more than it sounds. A wrap that says a file exists when it does not is worse
than no wrap, because you will trust it.

### `/handrail:scaffold`

**Reach for it when** you start working in a folder that has no `CLAUDE.md`, or when Claude keeps
needing the same context re-explained.

Creates `CLAUDE.md`, `MEMORY.md`, `tasks.md` and `plans/`, plus `README.md`, `backlog.md`,
`CHANGELOG.md`, `decisions.md`, and `.env.example` (if the project takes secrets) if the folder is a
git repo. The four base files hold four different kinds of state: rules that rarely change, live
state rewritten each session, open work as a checklist, and approved plans as a record. Keeping them
separate is the whole trick. Mixing them is what makes such files rot.

It surveys the folder before writing anything, so the conventions come from what you are already
doing rather than from a template.

### `/handrail:consolidate-folder`

**Reach for it when** you have eleven overlapping documents about the same thing and no idea which
one is current.

Combines them into one reference document organised by topic rather than by file. The thing it does
that you could not do by skimming: **where two files disagree, it says so** instead of quietly
picking a winner. That contradiction was already in your folder, and this is what makes it visible.

**This is not a summary.** Nothing is dropped, so the output is long. That is the trade: you get
navigable and complete, not short. Reads markdown, text, Word, PowerPoint, Excel and PDF.

---

## The three hooks

A hook runs outside the model, at the tool-call layer. Claude proposes a tool call, the harness runs
the hook first, the hook returns a decision, and the harness obeys it. Claude does not get a vote.

Each of the three is described the same way in the same order, so you can scan them side by side.

### `save-plan.py`, the one to keep if you keep only one

| | |
|---|---|
| **What it does** | Saves an approved plan to `plans/YYYY-MM-DD-<slug>.md`, then ends the turn |
| **When it fires** | The moment you approve a plan. Event `PostToolUse`, matcher `ExitPlanMode` |
| **What you see** | *"Plan saved to plans/2026-08-02-your-plan.md. Say the word when ready to execute."* and the turn stops. A re-approved identical plan says *"Plan already saved (identical)"* rather than writing a second copy |
| **Why you want it** | Without it, "yes, that plan is right" and "go build it" are the same keystroke, which is only what you meant some of the time. It also means every approved plan exists as a file you can come back to next week |
| **Turning it off** | Delete the `PostToolUse` block from `hooks/hooks.json`. **Or turn off half of it:** delete the three `control` keys at the top of `main()` in `hooks/save-plan.py` to keep the plan-saving and drop only the stop |

The slug comes from the plan's own `# Plan:` heading. Two plans with the same title on the same day
get `-b`, `-c`, and so on.

### `protect-paths.py`, which refuses writes to files you never want touched

| | |
|---|---|
| **What it does** | Refuses any write to `.env` and its variants (`.env.local`, `.env.production`, and similar), `*.pem`, `*.key`, `id_rsa*`, `secrets/`, `credentials*`, `node_modules/` or `.git/`. `.env.example` and `.env.template` are explicitly allowed |
| **When it fires** | Before any file edit or write. Event `PreToolUse`, matcher `Edit\|Write\|NotebookEdit` |
| **What you see** | *"Writes to `<path>` are blocked by the protect-paths hook. If this is intentional, edit PROTECTED in hooks/protect-paths.py or make the change by hand outside Claude Code."* |
| **Why you want it** | The damage from one bad write to `.env` is not the edit, it is the commit that follows it. Paths are normalised to absolute with forward slashes first, so the patterns behave the same on Windows and macOS |
| **Turning it off** | Delete its block from `hooks/hooks.json`. More useful: edit the `PROTECTED` and `ALLOWED` lists at the top of `hooks/protect-paths.py`, both plain glob lists meant to be edited |

### `block-ai-trailer.py`, which keeps AI attribution out of commit metadata

| | |
|---|---|
| **What it does** | Refuses a `git commit` whose message carries a `Co-Authored-By: Claude` trailer, including one hidden in a `-F` or `--file` message file |
| **When it fires** | Before any shell command that creates a commit. Event `PreToolUse`, matcher `Bash\|PowerShell` |
| **What you see** | *"This commit message carries an AI co-author trailer, which this project does not use. Credit AI in the README or a tech-stack section… Remove the trailer and re-run the commit."* |
| **Why you want it** | If you would rather credit AI once in your README than in every commit's metadata forever. Reading history for the trailer stays allowed on purpose, since `git log \| grep Co-Authored-By` is how you find out whether you already have hundreds of them |
| **Turning it off** | Delete its `Bash\|PowerShell` block from `hooks/hooks.json` |

If you want this behaviour without a hook, the native setting is `attribution.commit: ""` in
`settings.json`. This hook is the backstop for a hand-written trailer or a settings file that gets
reverted.

### A note on disabling

Two things people get wrong:

- **Deleting the `.py` file is not how you turn a hook off.** The entry in `hooks/hooks.json` is what
  wires it up. Without the script it just fails, and a failing hook is noise rather than absence.
  Delete the block from `hooks/hooks.json`.
- **Re-enabling needs a reload.** Restore the block, then run `/reload-plugins` or restart. Skipping
  that step is the usual reason someone concludes the hook is broken.

---

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

That is the same test used to decide what went in this plugin. The six skills describe how to do
something, the three hooks describe what must not happen.

---

## Turning everything off

**All three hooks, keeping the skills.** Replace the contents of `hooks/hooks.json` with `{}`, then
`/reload-plugins`. The skills are unaffected, since nothing references the hooks.

**One skill.** Delete its folder under `skills/`. Skills are auto-discovered, so there is no list to
update.

**The whole plugin.** `/plugin uninstall handrail@thevemana`. To also drop the marketplace entry,
`/plugin marketplace remove thevemana`.

---

## Requirements and troubleshooting

**Python 3 on your PATH.** The skills work without it. The hooks and `consolidate-folder`'s inventory
script do not.

**If your system uses `python3` rather than `python`,** edit `hooks/hooks.json` and change `python` to
`python3` in all three `command` lines, then `/reload-plugins`. On Windows, `python` is usually right.
On macOS and most Linux distributions, `python3` is. Check with `python --version`: if that errors but
`python3 --version` works, you need the edit. This is the single most common install problem, and it
is invisible. A hook whose interpreter does not exist fails to start, and a hook that fails to start
blocks nothing.

**Telling a working hook from a silently broken one.** This is the important one. A hook with a wrong
path does nothing at all, which is indistinguishable from a hook that is working and simply has not
found anything to object to. The only reliable check is to make one fire on purpose:

```
Create a .env file in this folder with API_KEY=test
```

A refusal means the wiring is good. A created file means it is not. `python test-hooks.py` passing
`20/20` tells you the logic is sound but says nothing about whether Claude Code is calling it. The
two failures look identical from the outside, which is why both checks are worth running.

**Skills not appearing after install.** Restart, or `/reload-plugins`. Typing `/handrail` should offer
all three.

**If you already run your own AI-trailer hook globally,** this plugin's will run alongside it and both
will deny the same commit. That is harmless, since two denials are one denial, but the doubled message
reads like a bug if nobody tells you. Drop whichever copy you prefer.

---

## License

MIT.

---

Made with the help of AI, but completely thought out, tested, and vetted by humans.
