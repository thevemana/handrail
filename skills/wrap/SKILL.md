---
name: wrap
description: Close out a work session. Writes a dated wrap file recording what was done, what was decided and why, what is unfinished, and the exact next action, then reconciles any task list, updates any plan file, and verifies its own claims against disk, so the next session resumes without re-explaining. Use when the user signals a session is ending or wants continuity for next time ("that's a wrap", "wrap this up", "wrap up", "wrapup", "let's call it here", "done for today", "before I close this out", "leave notes for next session"), and offer it proactively at a phase boundary in multi-session work. Do NOT use to finish a coding task, to compact or export the conversation, to write a commit message, PR description, or CHANGELOG entry, or to hand work to a subagent.
---

# Wrap

That's a wrap. Claude forgets everything when a session ends, so this writes down what matters and
the next one starts warm instead of from zero.

Run the six steps in order. **Steps 2, 3 and 4 are conditional** — if the project has no task list,
no plan file, or nothing worth carrying in memory, say so explicitly, offer to create it, and move
on. Saying "no task list here" is a completed step. Skipping silently is not.

**Steps 1, 5 and 6 always run.** Step 6 especially: verification is not conditional on anything, and
a session with nothing to reconcile still has to prove that what it wrote is true.

---

## Step 1 — Name it and place it

**Title:** 3 to 5 words, kebab-case, from the main thing worked on. `auth-refactor`, `csv-importer`.

**Filename:** `YYYYMMDD-wrap-<title>.md`. Date first so files sort chronologically.

**Folder:** the folder that owns the work, which is not automatically the one the session started in.
If the session ran from a repo root but the work was all in one subproject, the wrap belongs with
the subproject. Work spanning several areas goes where the main deliverable lives, with the others
named in the file.

When it isn't obvious which folder that is, use one test: **which artifact does this task change?**
A file that lives in one location belongs there. A decision, a plan, or how a conversation went
belongs wherever that's tracked, even if the session ran somewhere else. If the work genuinely
touched more than one location roughly equally, fall back to the rule above: it goes where the main
deliverable lives, and the others get a one-line pointer — never a second copy of the same content.

Put it in a `_wraps/` subfolder. Create it on the first wrap in a folder. If loose wrap files are
already sitting at that folder's root, move them in during the same edit and say so.

**Check for a `CLAUDE.md`.** If the folder has none, say so and offer `/handrail:scaffold` — same
rule as everywhere else in this skill: name the exact path, wait for a yes, create nothing without
one. Don't build scaffolding logic here; route to the skill that already does it properly.

---

## Step 2 — Reconcile the task list (if there is one)

Look for a `tasks.md`, `TODO.md`, or equivalent. Check the folder you are writing into and its
parents — work here often closes an item tracked one level up. Format and checkbox legend:
`../scaffold/tasks-format.md` — that file is the canonical definition, not restated here.

- **Close on the line, not in prose.** A finished item becomes `[x]` with a done-date in the same
  edit. Writing "we finished X" in a narrative paragraph is not closing X. That is the specific
  mechanism by which task files rot into fiction.
- **Advanced is not done.** Work that moved but did not finish gets a dated note under the item and
  the box stays unchecked. When unsure, leave it open and name the gap.
- **Add** items for loose ends this session surfaced.

**Health check.** Report open, closed, and total line counts for each file touched. Flag it as worth
a cleanup if the file is over roughly 400 lines, if closed items outnumber open ones, or if you find
an item marked open that is verifiably done. Report the flag; do not do the cleanup unprompted.

**Version history.** If the file you're writing to is untracked or gitignored, say so in the wrap
file. A file can be correctly excluded from git for a shipping reason and still silently lose every
bit of history the moment that happens — better to name that tradeoff now than have someone discover
it by accident once the narrative it held is the only copy that ever existed.

**If there is no task list anywhere, say so, then offer to fix it.** The check having run is not the
end of it: this session produced next actions, and with nowhere to put them they live only in a wrap
file nobody may open. Offer two options and let the user pick:

- **Just what's needed here** — a minimal `tasks.md` in this folder, following `tasks-format.md`,
  pre-filled with the open items this session actually surfaced.
- **The full set** — point them at `/handrail:scaffold`, which surveys the folder first and creates
  the whole state-file set with conventions derived from what is already there.

Create nothing without a yes, and name the exact path before writing. If they decline, record "no
task list, declined" rather than "no task list here", so the next session knows it was offered and
turned down rather than never considered.

---

## Step 3 — Update plan files (if any were used)

Any plan created this session, plus any existing plan the work advanced. Check the project's
`plans/` directory. A plan is never left frozen at its approval state.

Maintain a header on each: `Approved:` (never overwrite or invent a date), `Status:`
(`Started` / `In progress` / `Done` / `Abandoned`, where `Done` means the whole plan, not one part
of it), and `Last updated:`. Append one dated line per change under a `## Change Log` heading.

If no plan was used, say so and skip. If a plan was used but there is no `plans/` directory to keep
it in, offer the same two options as Step 2: create `plans/` here and file this one plan in it, or
run `/handrail:scaffold` for the whole set. Same rule — name the path, wait for a yes.

**Version history.** Same check as Step 2 — if the plan file itself lives outside git's view (or the
project has no version control at all), say so, for the same reason: a plan's change log is the only
record of what was approved and when, and that's worth knowing is unversioned.

---

## Step 4 — Memory: write, then check

**Write.** If the folder has an existing `MEMORY.md` or equivalent, update it with this session's
new state rather than leaving it frozen — same rule as Steps 2 and 3 for tasks and plans. If the
folder has none and this session established state worth carrying (where things stand, what's
half-finished, what the next session needs to know before touching anything), offer to create one.
Do not offer it for a session that produced nothing durable; an empty `MEMORY.md` is worse than
none, because it reads as "nothing is happening here" when the truth is nobody filled it in. If
there is no memory file anywhere, offer the same two options as Steps 2 and 3: a minimal file here,
or `/handrail:scaffold` for the whole set. Name the path, wait for a yes.

**Version history.** Same check as Steps 2 and 3 — if the memory file lives outside git's view, say
so in the wrap file.

**Check.** Before closing, look at every memory file this session actually read from, or wrote to,
and classify each one: **Confirmed** (still true), **Stale** (was true, now dated), **Wrong**
(contradicted by something this session found), or **Unverifiable** (no way to check from here). A
file created fresh in the Write step above has no prior content to check against — skip it here.
Lead with "was anything wrong this session," not "was anything used." Before concluding "no memory
file applies," confirm that by checking whether one exists, not by the absence of a reason to open
it. Put every non-Confirmed result in the wrap file with the evidence and stop there — the person
adjudicates. If the person confirms a correction, that edit happens now, in this same step, under
the guardrails below — never folded silently into the Write sub-step above.

Guardrails on any memory file touched — read for Check or written in Write — this session:

- **Cap it at three.** A fourth means stop touching memory files and move on to Step 5 with what's
  covered so far. The cap limits memory work, not the rest of the wrap — Steps 5 and 6 still run.
- **Diff before writing** to any existing memory file. Show the before and after; never silently
  overwrite one.
- **Never delete a memory line.** Supersede it with a new, dated line instead — a wrong memory dated
  today is itself useful evidence of when the drift actually happened.

If no memory file applies at all this session, say so and move on.

---

## Step 5 — Write the file

Use this structure.

```
# Wrap: [Title] — [YYYY-MM-DD]

## Overview
[Two sentences. What was accomplished, and what is immediately next.]

## What We Did
[Prose, not bullets. The arc and where things landed, not a step-by-step log.]

## Decisions Made

| Decision | Reasoning |
|---|---|
| [what was decided] | [why, including what was rejected] |

## Next Actions and Open Threads
- [Pending action, unresolved question, or known gap]

Next session: start with [one specific action].

## Durable Facts
[Only non-obvious things that outlive this session. Not what re-reading the code would tell you.
Empty is a valid answer.]

## What Went Wrong

| What was tried | What happened | Resolution |
|---|---|---|
| [attempt or breakage] | [the error or discovery] | [fix, or "dead end, do not retry"] |

## Notes

**Files created or modified:** [full paths, one per line, labelled created or modified]
**Tasks updated:** [each file touched and what changed; or "no task list, created one at <path>"; or
"no task list, declined"]
**Plans updated:** [each file touched and what changed; or "no plan used"; or "no plans/ here,
created one"; or "no plans/, declined"]
**Memory updated:** [what was written, and where; or "no memory file applies"]
**Memory accuracy:** [any non-Confirmed classifications from Step 4, with evidence; or "nothing
flagged"]
**Verification:** [see Step 6]
```

The `What Went Wrong` table is the highest-value section and the one most often skipped. A recorded
dead end stops the next session from walking into it again.

---

## Step 6 — Verify, then report

**Do not assert this ran. Check it.**

1. The wrap file exists at the path you claimed, and re-read it renders correctly.
2. Every file path listed under Notes actually exists.
3. Every task item you marked closed is genuinely `[x]` on disk, not just described as closed.
4. Every memory file claimed written, or checked for accuracy, exists at the stated path.
5. Nothing in the file claims work that did not happen.

A failed check gets fixed now, not noted for later.

Then tell the user, in chat: where the file landed, the task-list health numbers and any cleanup
flag, any plan files updated, any memory-accuracy rows awaiting a decision, and anything you could
not verify. Keep it to a few lines.

---

## Notes for customising this

The conventions above are deliberately mild so they work on a fresh machine. If your project already
has its own task format, plan format, or memory file, edit this skill to match rather than making
Claude guess. This file is yours once installed — a skill you have adapted to your actual project
beats a generic one.
