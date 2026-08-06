# handrail

MIT licensed, open source.

*A guiding mechanism for working with Claude Code with more confidence and speed.*

Already know you want this? Skip straight to [Install](#install).

Claude Code only knows what you tell it, and it forgets the moment a session ends unless something
writes it down. handrail is that something.

| What gets in the way | What handrail does about it | Where |
|---|---|---|
| AI memory is built by hand, and goes stale the moment you close the window | A **CLAUDE.md** that says how you work, a **MEMORY.md** that survives between sessions, a `wrap` that records what happened and why | `onboard`, `scaffold`, `wrap` |
| No receipts. You're trusting a synthesis, not seeing the work | Checks its own claims against disk before reporting done. Says exactly where two documents disagree instead of picking a winner | `scaffold`, `wrap`, `consolidate-folder` |
| A new vocabulary to learn every time the field moves | Seven **skills** (commands you type as `/handrail:name`), small interviews instead of a blank template, distilled from practices tested across many people | `onboard`, the whole skill set |
| Claude's pace and tone don't match yours, and you can't make it adapt | Interviews for pace and tone once, and lets any new preference become a standing rule | `onboard`, `codify` |
| Mid-conversation you say "always do it this way," and it's gone by next session | Catches the sentence, asks a few short questions, routes it to the right home on its own | `codify` |
| One opinion on a draft or a decision isn't enough to trust, but composing several yourself takes as long as writing the thing | Independent takes, blind to each other, that don't get averaged into one smoothed-over answer: feedback while you're still shaping it, or a verdict when it's time to ship | `collaborate`, `judge` |

You could do this by hand, keep CLAUDE.md updated yourself, some people do. handrail is for closing
the gap between meaning to and actually doing it while a session is moving.

Everything here is optional and everything here is editable. Once installed, these files are yours.

---

## Install

**Before you start:** you need Claude Code itself running, and nothing else, `thevemana/handrail` is
a public GitHub repo, so no account or login is required. (The two hooks need Python 3 and are off
until you turn them on; see [Hooks, if you want enforcement](#hooks-if-you-want-enforcement) below.
Skills need neither.) Nothing here calls out to any external service: the hooks are local scripts that only read stdin
and check file paths, and the skills add no network behavior beyond what your Claude Code session
already does. Reversible any time, in one command in the terminal or one menu item in the desktop
app; see [Turning everything off](#turning-everything-off).

Type both of these **inside a running Claude Code session**. These are Claude Code's own `/`
commands, so they go in the prompt where you talk to Claude, not in a shell. If you are using the
desktop app they are not available at all, so use
[On the Claude Code desktop app](#on-the-claude-code-desktop-app) below instead.

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
| after the restart | Typing `/handrail` offers `onboard`, `codify`, `wrap`, `scaffold`, `consolidate-folder`, `collaborate` and `judge` |

The install form is `<plugin>@<marketplace>`, not a bare plugin name. Here that is
`handrail@thevemana`: the plugin, then where it came from.

### On the Claude Code desktop app

Use the **Code** tab. Plugins installed there do not carry over to the Cowork tab, which draws its
configuration from your claude.ai account rather than from `~/.claude`.

The `/plugin` commands above are not available in the desktop app. Install through the interface
instead:

1. Click **+** next to the prompt box and choose **Plugins**
2. Choose **Add plugin** to open the plugin browser
3. Click **+** again and choose to add a marketplace from a repository
4. Paste `https://github.com/thevemana/handrail`
5. Select **handrail** and install it

The app reports the plugin as installed and ready. If typing `/handrail` in the prompt box does not
offer the seven skills, restart the app.

To remove it later, use **Manage plugins** in the same **+** menu rather than the uninstall command
below. The desktop app and the CLI share the same configuration, so installing on either one covers
both on that machine.

---

## Try it

Five minutes, seven things to type. Each one says what you should see.

**1. Write your global CLAUDE.md.** If you don't have one yet, or only have a thin first attempt:

```
/handrail:onboard
```

*You should see:* it checks what's already at `~/.claude/CLAUDE.md` first, then asks a handful of
questions in short rounds rather than handing you a blank template. It shows you the full draft
before writing anything. A blank file or a rough handful of lines both still get the normal
interview; it only refuses once the file looks genuinely lived-in, and then it offers to help with
one section instead of a rewrite. That refusal is a feature, so try it on purpose.

**2. Catch a rule on the fly.** This one asks questions back instead of saving your sentence
verbatim, so try it with a rule you'd actually want kept. Anywhere, mid-conversation, say something
like:

```
From now on, always show me exactly what's about to change before you edit a file in this repo.
```

*You should see:* it asks a few short questions (does this apply everywhere or just here, what
would a miss actually cost) rather than pasting your sentence straight into a file, then tells you
where it's landing before writing anything.

**3. Scaffold a project.** Pick any project folder, open Claude Code there, and type:

```
/handrail:scaffold
```

*You should see:* it lists the folder first and asks about anything it cannot infer, then writes
`CLAUDE.md`, `MEMORY.md`, `tasks.md` and a `plans/` folder holding a README that says how plans get
named and what shape they take. Open `CLAUDE.md`. It should describe
conventions your folder actually uses, not a generic template. If it reads generic, tell it what it
missed. The file is yours to correct.

**4. Close a session properly.** Once you've done substantial work, something building toward a
real decision or milestone, wrapping it up is worth the habit: it keeps a running record of what
you decided and why, not just what changed. After a bit of that kind of work, try:

```
/handrail:wrap
```

*You should see:* a new file under `_wraps/`, named `YYYYMMDD-wrap-<title>.md`, plus a short summary
in chat naming where it landed. Open the file and read the **What Went Wrong** table. That is the
section that pays for itself, because a recorded dead end stops you walking into it twice.

**5. Consolidate a folder of notes.** Point it at a folder you already have:

```
/handrail:consolidate-folder ~/notes/some-project
```

*You should see:* a file manifest first, before any reading happens, listing what is in scope. Then
one long document. **Read the contradictions section first.** That is the part you could not have
got by reading the files yourself.

**6. Get more than one take on a draft.** Point it at something you are still shaping:

```
/handrail:collaborate ~/drafts/resume.md
```

*You should see:* it either infers cold-read or with-info from how you phrased the request and says
which one it picked, or asks if that's unclear. Then several independent readers, blind to each
other, followed by a synthesis naming where they agreed and where they genuinely split, without
smoothing the split into one average.

**7. Get a verdict before something ships.** Once a draft is close enough to send, ask for a check:

```
/handrail:judge ~/drafts/resume.md
```

*You should see:* one judge by default, opinion, critique, concrete fixes, and a grade. Ask for a
panel of judges instead and each score shows on its own before any talk of a spread, never one
averaged number hiding a real disagreement.

Want to see the hooks refuse you? Turn them on first, they ship off, then
[docs/hooks.md](docs/hooks.md#try-them-yourself) has two more things to try.

---

## The seven skills

### `/handrail:onboard`

**Reach for it when** you install Claude Code and have no global `~/.claude/CLAUDE.md` yet, or
only a rough first attempt.

Interviews you in six short rounds instead of handing you a blank template: who you are and what
you're using it for, what should never happen without a stop, how much you want to see before
Claude acts, how you want it to talk to you, whether you already keep any kind of running notes,
and what you want Claude to do when two things it is reading disagree. Skips any round that
produces nothing usable rather than padding the file with a generic placeholder, and shows the full
draft before writing it. Refuses to overwrite a file that already looks lived-in.

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
rather than describing them as finished in a paragraph, updates any plan file the work advanced,
checks any memory file it touched for drift and flags what's stale or wrong rather than rewriting it
outright, and verifies its own claims against disk before reporting.

**Before writing a new one, it reads the last few wraps.** If the same next action has carried
across three wraps in a row, it says so under its own heading, names those files, and quotes the
line that keeps coming back, then stops there without telling you what it means. Three, not two:
twice is an ordinary week. A record written one session at a time cannot show you something that
only appears across sessions, however honest each entry is, and a project moving normally never
grows that heading.

**You do not need any of those files first.** If there is no task list, no `plans/`, or no
`MEMORY.md`, it says so rather than skipping quietly, and offers to create one, or points you at
`/handrail:scaffold` for the whole set.

That last part matters more than it sounds. A wrap that says a file exists when it does not is worse
than no wrap, because you will trust it.

### `/handrail:scaffold`

**Reach for it when** you start working in a folder that has no `CLAUDE.md`, or when Claude keeps
needing the same context re-explained.

Proposes `CLAUDE.md`, `MEMORY.md`, `tasks.md` and `plans/`, plus `README.md`, `backlog.md`,
`CHANGELOG.md`, `decisions.md`, and `.env.example` (if the project takes secrets) if the folder is a
git repo. The four base files hold four different kinds of state: rules that rarely change, live
state rewritten each session, open work as a checklist, and approved plans as a record. Keeping them
separate is the whole trick. Mixing them is what makes such files rot.

It surveys the folder first and shows you the whole set before writing a single file, so the
conventions come from what you are already doing rather than from a template. **Nothing is created
until you say yes.** And if it wants to retire something you already have, an `ideas.md` that is
really a task list, it searches the folder for anything linking to that file and tells you what
would break, before it asks.

**If the folder disagrees with itself, the survey says so and leaves it that way.** Two task lists
with different open items, a README describing a layout you no longer have, a status line a later
note contradicts. You get both claims, both file paths, and no verdict. Conventions derived from a
folder that contradicts itself, without anyone saying that it does, are how one of the two versions
quietly becomes the official one.

### `/handrail:consolidate-folder`

**Reach for it when** you have eleven overlapping documents about the same thing and no idea which
one is current.

Combines them into one reference document organised by topic rather than by file. The thing it does
that you could not do by skimming: **where two files disagree, it says so** instead of quietly
picking a winner. That contradiction was already in your folder, and this is what makes it visible.

**This is not a summary.** Nothing is dropped, so the output is long. That is the trade: you get
navigable and complete, not short. Reads markdown, text, Word, PowerPoint, Excel and PDF.

### `/handrail:collaborate`

**Reach for it when** you have a draft or a plan still in progress and want more than one reaction
to it, or you are stuck circling the same decision without landing anywhere.

Runs several independent readers at once, blind to each other, so one does not just echo another.
Cold-read mode gives them zero context and lets them react to what is actually on the page;
with-info mode briefs them on purpose and audience first. Either way, the synthesis names where
readers agreed and where they genuinely split, and will not smooth a real split into one
comfortable middle answer. It suggests concrete fixes. It never grades.

### `/handrail:judge`

**Reach for it when** you want to know if something is actually ready, not more feedback while you
are still shaping it.

Runs one evaluator by default, or a panel of them when you want more confidence than a single read
gives. Cold-read mode is the blind check worth running before calling anything final: the judge
gets no framing and has to work out what the artifact is for on its own. Every run ends the same
way, an opinion, a critique, concrete fixes, and a grade, and a panel shows each judge's score
before it says anything about the group, rather than opening with one flattened number.

---

## Hooks, if you want enforcement

Skills are things you ask for. Hooks are things that happen whether you ask or not, which is why
they matter for the handful of rules you can't afford to have skipped.

Two small Python scripts do this: saving an approved plan before it starts building, and refusing
writes to `.env` and other secrets.

**Both are off until you turn them on.** Installing handrail wires them up; it does not start them.
Nothing intercepts anything until you say so, per hook, in `~/.claude/handrail-hooks.json`:

```json
{
  "save-plan": true,
  "protect-paths": true
}
```

`/handrail:onboard` offers to write this for you. A plugin that starts blocking your file writes the
moment you install it is not a good introduction to anything, so handrail asks first.

They need Python 3 on your PATH (check with `python --version`). If you don't have it, six of the
seven skills still work exactly as described and the hooks simply cannot run, the exception is
`consolidate-folder`'s inventory helper (see
[Requirements and troubleshooting](#requirements-and-troubleshooting)).

Full reference, what each hook does, how to turn either off, and why hooks exist at all instead
of just more CLAUDE.md rules: [docs/hooks.md](docs/hooks.md).

---

## Turning everything off

**One skill.** Delete its folder under `skills/`. Skills are auto-discovered, so there is no list to
update.

**The whole plugin.** `/plugin uninstall handrail@thevemana`. To also drop the marketplace entry,
`/plugin marketplace remove thevemana`. On the desktop app neither command exists; use **Manage
plugins** in the **+** menu next to the prompt box instead.

**Just the hooks, keeping the skills?** See [docs/hooks.md](docs/hooks.md#a-note-on-disabling).

---

## Requirements and troubleshooting

**Skills work with nothing extra installed.** No Python, no account beyond Claude Code itself,
nothing to configure.

**Python 3 is only needed for the two hooks** (and `consolidate-folder`'s inventory script). Check
with `python --version`. If it errors, or you want to know exactly what each hook does and how to
turn one off, see [docs/hooks.md](docs/hooks.md).

**Skills not appearing after install.** Restart, or `/reload-plugins`. Typing `/handrail` should
offer all seven. On the desktop app `/reload-plugins` is not available either, so restart the app.

---

## License

MIT.

---

Made with the help of AI, but completely thought out, tested, and vetted by humans.
