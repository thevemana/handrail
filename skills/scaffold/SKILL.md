---
name: scaffold
description: Set up a folder or repo so Claude Code can work in it reliably across sessions. Creates CLAUDE.md, MEMORY.md, tasks.md and plans/ (plus backlog/CHANGELOG/decisions if it is a git repo), deriving the conventions from what the folder already contains rather than imposing a template. Use when asked to "scaffold this folder", "set this up for Claude", "add the usual files", or when starting work in a folder that has no CLAUDE.md. Do NOT use to create application code, config files, or project boilerplate.
---

# Folder scaffolding for Claude Code

Give a folder the small set of files that let Claude pick up work in it months later without being
re-briefed. Nothing here is specific to one person's setup. This skill is self-contained: it assumes
no rules from any other CLAUDE.md.

## The idea in one paragraph

Claude Code reads a `CLAUDE.md` at the start of every session, and reads nested ones when it touches
files in those folders. That makes the filesystem, not the chat log, the durable memory. Four files
carry four different kinds of state, and keeping them separate is the whole trick: **rules** that
rarely change, **live state** that is rewritten each session, **open work** as a checklist, and
**approved plans** as a record. Mixing them is what causes the files to rot.

| File | Holds | Changes |
|---|---|---|
| `CLAUDE.md` | Conventions and rules for this folder | Rarely |
| `MEMORY.md` | Where things stand right now | Every session, rewritten not appended |
| `tasks.md` | Open and recently closed action items | As work opens and closes |
| `plans/` | Approved plans, one file each | On approval |

## Before writing anything: survey

**Do not start from the template.** The template is the floor. The value is in what the folder is
already doing that nobody has written down.

1. **List the folder,** including subfolders one level down. One level is deliberate here: this pass
   is about reading content to derive conventions, and it gets expensive fast. Step 5 goes deeper,
   but only looking for `CLAUDE.md` files, which is cheap.
2. **Read the first 5 to 10 lines of every existing file.** Headers reveal conventions faster than
   full reads and cost far less context. Look for:
   - Naming patterns. Are files dated (`topic-YYYY-MM-DD.md`) or not? A date usually means "frozen
     snapshot"; no date usually means "living document." That distinction is worth writing down.
   - Repeated header structures. A status line, a "source:" line, a companion link.
   - Cross-references between files, and which files get cited most (those are load-bearing).
   - Subfolder roles that differ from the parent.
3. **Check whether it is a git repo.** `git rev-parse --is-inside-work-tree`. This decides the file set.
4. **Check for files that already do one of the four jobs** under a different name. An
   `ideas.md`, a `todo.txt`, a `notes-to-self.md` is usually a `tasks.md` or a `MEMORY.md` that
   nobody named. Fold it in rather than creating a competing second list.
5. **Map the `CLAUDE.md` chain, three levels each way.** Walk up to three parent folders and down to
   three levels of subfolders, and record every `CLAUDE.md` you find and every one you don't. Stop
   early going up at a repo root, a home directory, or a drive root — never walk past one. Read the
   ones you find, nearest first, so the new file repeats none of them. What you are building is a
   picture of where this folder sits in an existing chain, which decides almost everything below.
   Report the map before proposing anything, as a list of paths with `has CLAUDE.md` / `none`
   against each.
6. **Read `~/.claude/CLAUDE.md`** if it exists, specifically for an already-stated state-file
   convention: a `tasks.md` checkbox scheme, a `MEMORY.md` shape, a `plans/` format. If one is
   stated there, use it instead of the defaults in the Templates section below — a global
   convention wins over this skill's own default the moment one exists. If the global file is
   silent on it, or doesn't exist, fall back to the defaults as usual.

If the folder is empty or nearly so, say so plainly. The scaffold will be generic, and that is fine,
but do not present a generic file as if it were derived from anything.

## Then propose, and wait

State what you will create, what you will change, and what you found that the person may not know
about their own folder (competing task lists, orphaned files, broken links). Wait for a yes.

This matters more than it sounds. Scaffolding touches a parent file and sometimes deletes a
redundant one, and both are hard to notice afterward.

## The file set

Always: `CLAUDE.md`, `MEMORY.md`, `tasks.md`, `plans/`.

If it is a git repo, add: `README.md`, `backlog.md` (the idea-to-ship ledger), `CHANGELOG.md`,
`decisions.md` (why non-obvious calls were made), `.env.example` if it takes secrets. Do not add
these to a notes folder. A notes folder with a `CHANGELOG.md` is noise.

## Writing rules

These are what separate a scaffold that helps from one that becomes a second source of drift.

1. **Say only what is unique to this folder.** A nested `CLAUDE.md` inherits everything from its
   parents automatically. Restating a parent rule creates two copies that will disagree later.
2. **One fact, one owner.** If something could change (a status, a rule, a count), exactly one file
   states it and the others link to it. An undated restatement in a second file is how drift starts.
   A dated snapshot that names its source is fine.
3. **`tasks.md` never rolls up children.** Full format, checkbox legend, and the cascade rule:
   `tasks-format.md` in this folder — that file is the canonical definition, referenced by `wrap`
   too, so don't restate it here or anywhere else.
4. **Prefer a table with a status column** over prose, whenever describing how something works. Give
   each row a real name from the filesystem or the code, and mark whether it is live, built,
   designed, or assumed. Prose hides the gap between what exists and what was intended.
5. **Write for the agent, not for the human.** A note that says "remember to check X" only fires if a
   human rereads it. The same note as "before doing Y, check X" is an instruction that fires on its
   own. This is the single most common defect in these files.
6. **Date the file.** A `Last updated:` line under the title, and update it when you edit.

## Deleting or replacing an existing file

**Search for inbound references before proposing the deletion, not after.** Grep the whole
surrounding tree for the filename and for wiki-style `[[links]]` to it. State the blast radius in
the proposal so the person is approving the real change and not a smaller one.

When a file is retired, preserve item ordering if anything references its contents by number, and
leave a short banner in each file whose links you retarget saying what moved and when.

## Wiring into the chain

A `CLAUDE.md` that nothing links to is discoverable only by accident. Use the map from survey step 5
and wire the new file in both directions, then say what you wired.

**Link up.** The new file's header names its nearest ancestor with a `CLAUDE.md`, as a relative path:
`Inherits from [parent](../CLAUDE.md)`, or `../../CLAUDE.md` if the nearest one is two levels up.
Name the actual nearest one, not the immediate parent folder, or the link points at a file that
isn't there.

**Link down.** The `## Subfolders` section lists every subfolder within three levels that has its own
`CLAUDE.md`, each with a relative link and one line on what that folder owns. A subfolder with no
`CLAUDE.md` of its own is not listed — it inherits this file and needs no entry.

**Register upward.** If the nearest ancestor has an index or routing table, add a line to it pointing
at the new file. If it has a `CLAUDE.md` but no index, say so rather than inventing a table in
someone else's file, and offer to add one.

**Become the connector when you land in the middle of an existing chain.** If the map shows a
`CLAUDE.md` both above and below this folder, those two were previously linked to each other,
skipping the level you are now adding. Inserting a file without re-pointing them leaves a chain that
routes around the new file, which is the same as not having it. So:

1. Point the new file up at the ancestor and down at the descendants, as above.
2. **Re-point the descendants.** Each descendant whose `Inherits from` link targets the old ancestor
   now targets the new file instead. This is an edit to someone else's file, so it goes in the
   proposal with the exact paths, before anything is written.
3. **Re-point the ancestor's index.** A row that pointed straight at a descendant now points at the
   new file, with the descendant listed as a child of it. Do not delete the descendant's row without
   saying so; a row vanishing from an index is how a folder becomes invisible.
4. Leave a one-line dated note in each file you re-pointed, saying what moved and when, per the
   deleting-and-replacing rule above.

**Announce the result plainly**, as a before-and-after of the chain, not as prose. Name every file
you edited and every link you changed. Someone reading the summary should be able to see the shape
of the chain without opening anything.

**When nothing is above or below**, say so. A standalone `CLAUDE.md` with no chain is a normal and
fine outcome; it just needs stating, so nobody assumes a link was made that wasn't.

## Templates

Floors, not ceilings. Replace the bracketed parts and delete any section the folder does not need.

### CLAUDE.md

```markdown
# CLAUDE.md (folder name)
# Inherits from [nearest ancestor](../CLAUDE.md). Describes this folder only; does not restate
# parent rules. Delete this line if no ancestor has a CLAUDE.md.
Last updated: YYYY-MM-DD

## What this folder is
[One paragraph. What lives here, and just as important, what does not and where that goes instead.]

## Conventions
[The patterns derived from the survey. Naming, file structure, anything a newcomer would otherwise
have to infer by reading everything. Table if there is more than one kind of file.]

## Subfolders
Only those with their own `CLAUDE.md`. A subfolder without one inherits this file and needs no row.

| Folder | What it owns |
|---|---|
| [name/](name/CLAUDE.md) | [what that folder is the source of truth for] |

## Gotchas
[Anything that has already gone wrong here, or that would if someone assumed the obvious thing.]
```

### MEMORY.md

```markdown
# MEMORY.md — [folder name]
Last updated: YYYY-MM-DD

Live state only. Open work is in tasks.md and is not duplicated here. Rewrite this file each
session rather than appending.

## Session summary
[Two or three sentences on what just happened.]

## Decisions made
- [Decision]: [why]

## Open threads
- [Thread]: [status] — next action: [what]

## Artifacts produced
- [path]: [what it is]

## Recommended first action next session
[One specific sentence.]
```

### tasks.md

Canonical format, checkbox legend, and template: `tasks-format.md` in this folder. Read it before
writing a `tasks.md` — this section used to duplicate it inline and that's exactly the kind of
second copy that drifts, so it doesn't anymore.

### plans/README.md

```markdown
# plans — [folder name]

Approved plans land here, one file per plan, named YYYY-MM-DD-short-slug.md:

  # Plan: [title]
  Approved: YYYY-MM-DD
  Status: not started | in progress | done | abandoned

  ## Goal
  ## Approach
  ## Outcome        ← filled in after, including anything that deviated from the plan

If a plan changes materially mid-execution, update the same file and note what changed. Do not
start a second one.
```

Optional, and worth turning on: setting `plansDirectory: "plans"` in `~/.claude/settings.json` makes
Claude Code auto-save its plan-mode output here in every project, so a plan survives even if nobody
remembers to file it.

## What this skill cannot do

**A skill cannot install hooks or change settings.** It runs inside the model's reasoning, so
everything above is advisory: it will be followed most of the time, not every time.

For anything where a single miss would cause real damage (pushing to main, deleting production data,
committing a secret, overwriting a file without confirmation), a `PreToolUse` hook in
`~/.claude/settings.json` is the correct implementation, because it runs outside the model and blocks
the action unconditionally. Say so when the situation calls for it rather than adding another rule to
a markdown file and hoping.

The useful way to hold this: **captured in a note fires never, written as an instruction fires
usually, enforced by a hook fires always.** Move a rule up that ladder when the cost of a miss
justifies it, and not before.
