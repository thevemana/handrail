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
   is about reading content to derive conventions, and it gets expensive fast. Step 6 goes deeper,
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
   nobody named. **Flag it here; do not fold it in yet.** Folding one file into another is a
   deletion wearing a friendlier word, so it goes through the deleting-and-replacing rule below:
   search for inbound references first, state the blast radius in the proposal, act only after a
   yes. If the file is only *partly* doing one of the four jobs — a notes file with a todo section
   and a pile of unrelated content around it — propose extracting the part that matches and
   leaving the rest exactly where it is. Never delete a whole file on account of the part of it
   that moved.
5. **If a `plans/` folder already exists, check its filenames against the convention.** The
   template below names plans `YYYY-MM-DD-short-slug.md`. Flag anything that doesn't match — an
   auto-generated name, an undated title — and propose a rename. A rename breaks inbound links
   exactly like a deletion does, so the same rule applies: search for references to the old
   filename first, put the blast radius in the proposal, rename only after a yes. If the folder
   has its own consistent working convention already, keep it and say so; what is not acceptable
   is a folder running two conventions at once with nobody choosing between them.
6. **Map the `CLAUDE.md` chain, three levels each way.** Walk up to three parent folders and down to
   three levels of subfolders, and record every `CLAUDE.md` you find and every one you don't. Stop
   early going up at a repo root, a home directory, or a drive root — never walk past one. Read the
   ones you find, nearest first, so the new file repeats none of them. What you are building is a
   picture of where this folder sits in an existing chain, which decides almost everything below.
   Report the map before proposing anything, as a list of paths with `has CLAUDE.md` / `none`
   against each.
7. **Read `~/.claude/CLAUDE.md`** if it exists, specifically for an already-stated state-file
   convention: a `tasks.md` checkbox scheme, a `MEMORY.md` shape, a `plans/` format. If one is
   stated there, use it instead of the defaults in the Templates section below — a global
   convention wins over this skill's own default the moment one exists. If the global file is
   silent on it, or doesn't exist, fall back to the defaults as usual.
8. **Say where the folder disagrees with itself, and do not settle it.** Everything above is a pass
   over the folder's own claims about itself, and nothing so far asks whether those claims agree.
   The headers are already read, so this costs one more look at what is in context. Go looking for
   two files stating the same thing differently: two task lists with different open items, a README
   describing a layout the folder no longer has, a status line contradicted by a dated note
   somewhere else, two files each behaving as the source of truth for one subject. Report each as a
   **pair** — both claims, both paths, both dates where they have them — and stop there.

   **Do not pick a winner, and do not quietly write the version you find more convincing into the
   new `CLAUDE.md`.** Deriving a convention from a folder that contradicts itself, without saying
   that it does, is how one of the two versions becomes permanent without anyone having chosen it —
   and the person approving the scaffold is the only one who can choose. If nothing contradicts, say
   "nothing contradicts". That is a finding, not an empty section.

**Say what the survey did not read.** It read the first 5 to 10 lines of each file and went one
level into subfolders, so everything below those lines and everything deeper is unread, and every
convention proposed above is derived from headers rather than whole files. State that in the report
alongside the findings. A survey's limits are invisible in its own output: an incomplete read that
does not say so is indistinguishable from a complete one, and it is the confident version that gets
acted on.

If the folder is empty or nearly so, say so plainly. The scaffold will be generic, and that is fine,
but do not present a generic file as if it were derived from anything.

## Then propose, and wait

State what you will create, what you will change, and what you found that the person may not know
about their own folder (competing task lists, orphaned files, broken links, files that contradict
each other), plus what the survey did not read. Wait for a yes.

This matters more than it sounds. Scaffolding touches a parent file and sometimes deletes a
redundant one, and both are hard to notice afterward.

Once you have the yes: write the file set from the templates below, wire the new file into the
`CLAUDE.md` chain, then run **Last check before finishing** at the end of this file. The pass is not
done when the files exist; it is done when that check has run.

## The file set

Always: `CLAUDE.md`, `MEMORY.md`, `tasks.md`, `plans/`.

If it is a git repo, add: `README.md`, `backlog.md` (the idea-to-ship ledger), `CHANGELOG.md`,
`decisions.md` (why non-obvious calls were made), `.env.example` if it takes secrets. Do not add
these to a notes folder. A notes folder with a `CHANGELOG.md` is noise.

## For git repos: two practices worth proposing

Not mandates — offer these as sensible defaults when scaffolding a git repo, unless the folder
already has its own working convention (survey step 2 would have found it).

- **Versioning.** SemVer (`X.Y.Z`), tagged in git, recorded in `CHANGELOG.md` on release. This is
  the standard pairing, not a house style — worth naming even before anyone asks, so a project
  doesn't drift into ad hoc version strings.
- **Verify before calling anything done.** Before marking a deliverable finished or a release
  shipped, have it checked by someone or something with zero context on the work. Self-review
  reliably misses what a fresh read catches — the check should try to reproduce the claim, not just
  read it. Worth a line in the new CLAUDE.md's Conventions section if the repo ships things.
  **Check the copy that will actually be used, not the one you have open.** A claim can be true in
  the working tree and false in the copy someone else gets: a tag that exists locally and not on the
  remote, a README rendered from a different branch, an install still serving a cached older
  version. This is the error that survives review, because the claim really was verified — against
  the wrong copy.

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
   designed, assumed, or unconfirmed. `assumed` means nobody checked; `unconfirmed` means someone
   tried to check and could not, which is a different thing and worth its own word. Prose hides the
   gap between what exists and what was intended.
5. **Write for the agent, not for the human.** A note that says "remember to check X" only fires if a
   human rereads it. The same note as "before doing Y, check X" is an instruction that fires on its
   own. This is the single most common defect in these files.
6. **Date the file.** A `Last updated:` line under the title, and update it when you edit.

## Deleting, replacing, or moving an existing file

**Search for inbound references before proposing the change, not after** — a rename or a folder
move breaks a link exactly the same way a deletion does, and gets missed more often because it
doesn't feel destructive. Grep the whole surrounding tree for the filename, the old path, and for
wiki-style `[[links]]` to it. State the blast radius in the proposal so the person is approving the
real change and not a smaller one.

**Search with the ignore rules turned off** — `rg --no-ignore --hidden -g '!.git/'`, or the
equivalent for whatever tool you have. Ripgrep, and anything built on it, honours `.gitignore` by
default, and so does `git grep`. The files most likely to reference the thing you are about to move
are exactly the ones normally kept out of git: `tasks.md`, `MEMORY.md`, `plans/`, wrap records,
scratch notes. A default search skips them silently, without reporting that it skipped anything, so
it returns few hits rather than an error. That turns a missed reference into a confident "blast
radius: none," which is worse than not having checked, because the person approves a bigger change
than the one they were shown.

When a file is retired, renamed, or moved, preserve item ordering if anything references its
contents by number, and leave a short banner in each file whose links you retarget saying what
moved and when. If a "source of truth" file exists for the area (an index, a canon doc), its
resolution note is the one place this is guaranteed to get read later — don't skip it even if every
other link got fixed.

## Wiring into the chain

A `CLAUDE.md` that nothing links to is discoverable only by accident. Use the map from survey step 6
and wire the new file in both directions, then say what you wired. Every wiring edit lands in a file
other than the one being scaffolded, so all of it goes in the proposal with the exact paths, before
anything is written — the same rule the connector case below states for itself.

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

## Where the real answer lives
For anything two files could both claim: which one settles it, and what that rests on.

| Subject | Settled by | Based on | How well supported |
|---|---|---|---|
| [what the claim is about] | [the file, command, or person that settles it] | [what that rests on] | [Confirmed / One source only / Sources disagree / Not found] |

**Confirmed** — checked against the thing itself, not against another document.
**One source only** — one place says so and nothing contradicts it.
**Sources disagree** — two places say different things, and it is not settled yet.
**Not found** — nothing here answers it.

## Things that don't match
Contradictions found and not yet resolved. Each row keeps both sides. Resolving one means deleting
the row and saying so, not editing one side into agreement with the other.

| What | One side says | The other says | Found |
|---|---|---|---|
| [subject] | [claim, and where it came from] | [claim, and where it came from] | YYYY-MM-DD |

## Subfolders
Only those with their own `CLAUDE.md`. A subfolder without one inherits this file and needs no row.

| Folder | What it owns |
|---|---|
| [name/](name/CLAUDE.md) | [what that folder is the source of truth for] |

## Gotchas
[Anything that has already gone wrong here, or that would if someone assumed the obvious thing.]
```

**On those two sections.** `Where the real answer lives` is what turns "one fact, one owner" from a
rule into something someone can actually operate: it names the owner per subject instead of leaving
it implied. Fill it from the survey — the load-bearing files it found are the candidates.

**Leave the last column out until some subject in the table has more than one source.** A freshly
scaffolded folder has one source for everything, and a column reading `One source only` four rows
down teaches people to stop reading the column before it has ever told them anything. Add it the
first time two sources exist for one subject; that is when it starts carrying information. Each
label says what the evidence is, so nobody has to look up what it means — keep it that way, and do
not swap in shorter words that need a legend to decode.

`Things that don't match` starts empty in most folders and should stay empty rather than being
filled with hypotheticals. It exists so that a contradiction found during the survey (step 8) has
somewhere to live besides the chat log, and so the next person to find the same one can see it was
already known and deliberately left open.

### MEMORY.md

```markdown
# MEMORY.md — [folder name]
Last updated: YYYY-MM-DD

Live state only. Open work is in tasks.md and is not duplicated here. Rewrite this file each
session rather than appending.

## Session summary
[Two or three sentences on what just happened.]

## Decisions made
- [Decision]: [why] — based on: [the file, command, test, or person it rests on, or "judgment call,
  nothing checked"]

## Open threads
- [Thread]: [status] — next action: [what]

## Things that don't match yet
- [What disagrees with what, and where each side came from] — open since YYYY-MM-DD

## Artifacts produced
- [path]: [what it is]

## Recommended first action next session
[One specific sentence.]
```

**Every decision row carries what it was based on**, and "judgment call, nothing checked" is a
perfectly good value. A decision written here with reasoning but no source reads as settled fact by
the next session, which has no way to tell the checked ones from the ones that merely sounded right
at the time. The empty column is what does the damage, not an honest one.

`Things that don't match yet` is the session-level counterpart to the `CLAUDE.md` section of almost
the same name: that one holds contradictions about the folder that are expected to persist, this one
holds the ones this session ran into and could not settle. Both keep both sides.

### tasks.md

Canonical format, checkbox legend, and template: `tasks-format.md` in this folder. Read it before
writing a `tasks.md` — this section used to duplicate it inline and that's exactly the kind of
second copy that drifts, so it doesn't anymore.

### plans/README.md

```markdown
# plans — [folder name]
Last updated: YYYY-MM-DD

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

### decisions.md

Git repos only, alongside `README.md`, `backlog.md` and `CHANGELOG.md`. It holds the *why* behind
calls that would otherwise be re-argued from scratch by whoever arrives next, including whoever that
is six months from now with no memory of this week.

```markdown
# Decisions — [project name]
Last updated: YYYY-MM-DD

Why the non-obvious calls were made. One entry per decision, newest at the bottom. Numbered, and the
numbers are never reused or renumbered, because other files cite them.

## 1. [The decision, written as what is true now, not as the question that was asked]

**Decided:** YYYY-MM-DD
**Based on:** [what this rests on — a test result, a measurement, a document read, someone's
answer — or "judgment call, nothing measured". Say which; they are not the same and only one of
them is checkable later.]

[Two or three paragraphs. What was decided and the reasoning, in enough detail that someone who
disagrees can see where they'd have to attack it.]

**Rejected:** [the alternative, and why it lost. An entry with nothing rejected is usually a note
rather than a decision — consider whether it belongs here at all.]

**Would revisit if:** [the specific thing that would change the answer. "If it stops working" is not
specific.]
```

**Write the entry when the call is made, not at release.** Reconstructed reasoning is how a guess
gets written down as an analysis — by the time anyone sits down to fill this in retroactively, the
alternatives that were live at the time have already been forgotten.

**Offer this one and wait for a yes; do not apply it quietly.** Setting `plansDirectory: "plans"` in
`~/.claude/settings.json` makes Claude Code auto-save its plan-mode output into `plans/` in every
project, so a plan survives even if nobody remembers to file it. It is one line, but it sits in a
file outside this folder and it changes behaviour in every project rather than only this one, which
is exactly why it needs the same yes as any other edit outside the scaffold. Make the edit once it
has one. (What the closing section rules out is a skill *enforcing* something on its own; a settings
change the person approved is a different thing.)

## Last check before finishing

Before announcing the result, re-open every file this pass touched or created and confirm its
`Last updated:` line matches today. A correct edit with a stale date is still a miss — it's what
makes a later session trust the wrong version over the right one. This is cheap to check and easy
to skip anyway; check it.

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
