---
name: onboard
description: Write a personal global ~/.claude/CLAUDE.md from scratch by interviewing the user section by section, instead of handing them a blank template to fill in alone. Use when the user has no global CLAUDE.md yet, asks to set up Claude Code for the first time, wants a "starter CLAUDE.md", or invokes /handrail:onboard. Do NOT use for a project-level CLAUDE.md (that is /handrail:scaffold) or to rewrite an existing, already-substantial global CLAUDE.md — offer targeted edits instead of a wholesale replacement.
---

# Onboard

A blank template asks you to know what you want before you've used the tool. This asks instead,
one small group of questions at a time, and writes the file for you.

Run the four steps in order. **Do not skip Step 1.** Writing over a file someone has already
invested in is the one mistake here that is hard to undo.

---

## Step 1 — Check the ground before asking anything

### 1a. Is Python there?

Run `python --version`, and `python3 --version` if the first fails. Record which worked.

**Do this first, before the interview, not near the end.** handrail's hooks are Python scripts.
Without an interpreter they do not run at all, and a hook command that cannot start is a
*non-blocking* error in Claude Code, so the write it was supposed to guard goes through anyway.
Nothing later in this interview may describe the hooks as live, active, or protecting anything
unless this check passed. Say what you found, in one line, and carry it to Step 4.

If neither command works, say so plainly now: the seven skills work perfectly without Python, and
the two hooks cannot run until it is installed. That is a real limit, not a footnote, and finding
it out after a twenty-minute interview is worse than finding it out in the first ten seconds.

### 1b. What already exists

Read `~/.claude/CLAUDE.md`. Three outcomes:

- **Nothing there, or it's the harness default placeholder.** Proceed to Step 2.
- **A short file, clearly a first attempt** (rough notes, a handful of lines, no real structure).
  Say what you see, confirm the person wants to start over rather than build on it, then proceed.
- **A substantial, evidently lived-in file.** Stop. Say so plainly: this skill is for a first
  file, not a rewrite of one that already works. Offer to look at a specific section they want
  help with instead, or point at `/handrail:scaffold` if what they actually want is project-level
  setup, not global.

If a file does exist and the person confirms starting over, copy it to
`~/.claude/CLAUDE-<today's date>-pre-onboard.md` before writing anything new. This is the same
archive-before-edit habit the file you are about to write will itself recommend — start it
correctly.

---

## Step 2 — Interview, in five short rounds

Read `template.md` in this skill's folder before asking anything. It is the skeleton you are
filling; the section numbers below match it.

**One question per message. Wait for the answer before asking the next.**

This rule exists because the opposite was tried and failed in a real session. Three questions were
asked in one turn; the person answered two, because a terminal gives you one Enter and one reply;
the third was quietly lost. The skill then *noticed* the missing answer and said so, after it had
already moved to the next round, leaving someone aware of a hole with no way to fill it. Naming a
gap you have made unfixable is worse than not noticing it.

Batching is tempting because it looks efficient. It is only efficient when every question gets an
answer, and in a single-reply interface they do not.

**Close every round with a summary and a fork.** State what you now believe in two or three lines,
then offer three things by name: continue, change an answer, or go back a round. Do not treat this
as optional politeness and do not collect five rounds silently to reveal a surprise draft at the
end. If a round produced nothing, say so and move on rather than skipping the checkpoint.

**Blank versus options, so this is not decided per question by feel.** Offer named choices when the
answer space is small and known, and when asking openly would make someone invent vocabulary they
do not have. Leave it open when the answer is personal and unguessable. "How much do you want to
see before I act" gets options. "Which folder must never be touched" gets a blank, because only
they know. Use structured multiple-choice where your environment supports it; otherwise list the
options plainly and let them answer with a number.

**Round 1 — Identity (§1).** Three separate questions, asked one at a time. Who they are in a
sentence or two. What this is for (one job, several clients, a mix of code and non-code work). Any
standing assumption worth stating once rather than every session, such as timezone, geography or
units. **Do not compress these into one message.** This round is where the failure above happened.

**Round 2 — Guardrails (§3).** The one question that matters most: *is there a folder, a
repository, or a class of action (pushing to production, touching a specific database, sending
anything externally) that must never happen without an explicit stop?* Most people have at least
one and have never written it down. If they say "nothing comes to mind," say that's fine and move
on — an empty guardrails section is honest, a padded one is noise.

**Round 3 — Pace (§5).** How much they want to see before Claude acts. Give them the three
common shapes rather than an open question: *(a) plan everything non-trivial and wait for a
go-ahead, (b) just start on anything reversible and check in at natural breaks, (c) somewhere
between, with a size threshold.* Ask what "non-trivial" means to them in concrete terms — new
files over some line count, more than one file touched, anything with more than one reasonable
approach — because the template's placeholder is deliberately vague until someone commits to a
number.

**Round 4 — Output and tone (§7).** How they want Claude to talk to them day to day, and whether
that changes for anything meant for someone else to read (a README, a report, an email).

**Round 5 — Where state lives (§6).** Whether they already keep any kind of running notes,
task list, or decision log for their own work, and if so, where. If they don't yet, say the
template's suggestions (`MEMORY.md`, `tasks.md`, `plans/`) are optional and can be added later via
`/handrail:scaffold` inside a specific project — the global file doesn't have to commit to a
convention nobody's using yet.

**Skip what doesn't apply.** If a round produces nothing usable ("I don't really have guardrails
yet," "no strong pace preference"), leave that section out of the draft rather than filling it
with a generic placeholder. The template's own instruction is explicit about this: a section you
can't fill with something specific is worse than no section, because it dilutes the ones that are
real.

**§2 (what's actually enforced) and §8 (skills/subagents/hooks) are not interview questions.** They
start empty and fill in over time, as real rules get real enforcement or you install real skills.
Explain this once during the interview rather than asking about mechanisms that don't exist yet on
a fresh machine.

**§9 (scope) and §10 (maintenance) are not interview questions either, and don't leave their
brackets unfilled.** Nobody starting fresh has other reference files to point to yet or a
considered opinion on review cadence, so asking would produce a made-up answer. Default them
instead: for §9, drop the "[things deliberately elsewhere]" bullet and keep only the two fixed
lines about project-level and `CLAUDE.local.md` scope. For §10, replace `[cadence]` with "whenever
a rule stops firing, or gets in the way" rather than a made-up schedule. Both can be sharpened
later once there's something real to point at or a rule that's actually gone stale.

---

## Step 3 — Assemble and show the draft

Fill `template.md` with what came out of the interview, deleting every bracketed placeholder that
didn't get a real answer along with its section if the whole section is empty. Show the full draft
before writing it anywhere. This is the one artifact in the whole interaction the person should
read start to finish, since it's the thing that shapes every future session.

Two things to flag explicitly while showing it, so nobody discovers them by surprise later:

- **This file is advisory.** Claude follows CLAUDE.md instructions most of the time, not every
  time. Anything from the guardrails round where a single miss would cause real damage belongs in
  a hook, not a paragraph. Say so, and point at this plugin's own `protect-paths.py` as a worked
  example if their guardrail resembles what it already does.
- **This is a floor, not a finished file.** The right size is "everything here is a live rule,"
  not "everything I might ever want." It will grow as real sessions surface real needs — that's
  normal, and better than trying to anticipate them all now.

---

## Step 4 — Write and verify

Write the draft to `~/.claude/CLAUDE.md`. Then check, don't assert:

1. The file exists at that path and reading it back renders correctly.
2. No bracketed placeholder (`[like this]`) survived into the written file.
3. Line count is reported to the person, against the rough sense that a first file should be small
   — under 100 lines is normal, and that's a feature, not a shortfall.

Tell the person where the file landed, and that the next real signal is watching whether Claude
actually follows the guardrails round in a real session — that's the test a template sitting on
disk can't run for itself.

**Then say this explicitly, don't leave it implied:** §2 (what's actually enforced) and §8 (how the system
extends) are deliberately thin in a first file, because on day one there is usually nothing installed
to describe. They are the sections to come back to once real hooks or skills exist, and the file is
theirs to edit directly when that day arrives.

### Then offer the hooks, accurately

handrail ships two hooks and **both are off until the person turns them on.** Installing the plugin
wires them up; it does not start them. Do not describe them as live, active, running or protecting
anything until the file below says so and Step 1a found an interpreter.

Offer them one at a time, naming what each actually does:

- **`save-plan`** writes an approved plan to `plans/` and then stops the turn, so approving a plan
  never silently starts the work. It blocks nothing else.
- **`protect-paths`** refuses writes to `.env` files, `*.pem`, `*.key`, `secrets/`, `credentials`
  and `.git/`. This one intercepts every file edit, so say that out loud before they accept it.

If they want either, write `~/.claude/handrail-hooks.json`:

```json
{
  "save-plan": true,
  "protect-paths": false
}
```

Only the hooks set to exactly `true` run. A missing file means none of them do.

**If Step 1a found no Python, do not write this file.** Say that the hooks cannot run yet, that
installing Python is what changes it, and that this file is the one thing to create afterwards.
Writing an enabling config for scripts that cannot execute produces the precise failure this whole
step exists to avoid: someone believing they are protected when they are not.

Then §2 (what's actually enforced) has honest rows to fill: one per hook they actually turned on,
and none for the ones they did not.

---

## Notes for customising this

The five rounds above are deliberately the high-leverage ones, not an exhaustive tour of every
template section. If a particular round consistently produces nothing useful for the people you
run this on, or a section the template treats as optional turns out to matter more than expected,
edit this skill rather than working around it in conversation — the same rule `/handrail:wrap`
states for itself. This file is yours once installed.
