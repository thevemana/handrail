---
name: wrap
description: Close out a work session. Writes a dated wrap file recording what was done, what was decided and why, what is unfinished, and the exact next action, then reconciles any task list, updates any plan file, and verifies its own claims against disk, so the next session resumes without re-explaining. Use when the user signals a session is ending or wants continuity for next time ("that's a wrap", "wrap this up", "wrap up", "wrapup", "let's call it here", "done for today", "before I close this out", "leave notes for next session"), and offer it proactively at a phase boundary in multi-session work. Do NOT use to finish a coding task, to compact or export the conversation, to write a commit message, PR description, or CHANGELOG entry, or to hand work to a subagent.
---

# Wrap

That's a wrap. Claude forgets everything when a session ends, so this writes down what matters and
the next one starts warm instead of from zero.

Run the five steps in order. **Steps 2 and 3 are conditional** — if the project has no task list or
no plan file, say so explicitly, offer to create one, and move on. Saying "no task list here" is a
completed step. Skipping silently is not.

**Steps 1, 4 and 5 always run.** Step 5 especially: verification is not conditional on anything, and
a session with nothing to reconcile still has to prove that what it wrote is true.

---

## Step 1 — Name it and place it

**Title:** 3 to 5 words, kebab-case, from the main thing worked on. `auth-refactor`, `csv-importer`.

**Filename:** `YYYYMMDD-wrap-<title>.md`. Date first so files sort chronologically.

**Folder:** the folder that owns the work, which is not automatically the one the session started in.
If the session ran from a repo root but the work was all in one subproject, the wrap belongs with
the subproject. Work spanning several areas goes where the main deliverable lives, with the others
named in the file.

Put it in a `_wraps/` subfolder. Create it on the first wrap in a folder. If loose wrap files are
already sitting at that folder's root, move them in during the same edit and say so.

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

**A memory file is the third case.** If the folder has no `MEMORY.md` or equivalent and this session
established state worth carrying (where things stand, what is half-finished, what the next session
needs to know before touching anything), offer to create one. Do not offer it for a session that
produced nothing durable; an empty `MEMORY.md` is worse than none, because it reads as "nothing is
happening here" when the truth is nobody filled it in.

---

## Step 4 — Write the file

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
**Tasks updated:** [each file touched and what changed; or "no task list here"; or "no task list,
created one at <path>"; or "no task list, declined"]
**Plans updated:** [each file touched and what changed; or "no plan used"; or "no plans/ here,
created one"; or "no plans/, declined"]
**Verification:** [see Step 5]
```

The `What Went Wrong` table is the highest-value section and the one most often skipped. A recorded
dead end stops the next session from walking into it again.

---

## Step 5 — Verify, then report

**Do not assert this ran. Check it.**

1. The wrap file exists at the path you claimed, and re-read it renders correctly.
2. Every file path listed under Notes actually exists.
3. Every task item you marked closed is genuinely `[x]` on disk, not just described as closed.
4. Nothing in the file claims work that did not happen.

A failed check gets fixed now, not noted for later.

Then tell the user, in chat: where the file landed, the task-list health numbers and any cleanup
flag, and anything you could not verify. Keep it to a few lines.

---

## Notes for customising this

The conventions above are deliberately mild so they work on a fresh machine. If your project already
has its own task format, plan format, or memory file, edit this skill to match rather than making
Claude guess. This file is yours once installed — a skill you have adapted to your actual project
beats a generic one.
