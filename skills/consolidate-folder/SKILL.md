---
name: consolidate-folder
description: For a folder of overlapping documents about the same thing, where nobody can tell any more which one is current. Combines them into one reference document organised by topic rather than by file, and where two files disagree it says so instead of silently picking a winner. Nothing is dropped, so this is not a summary and the output is long. Duplicates are collapsed, and a per-file coverage check at the end proves nothing was missed. Use when the user says "consolidate this folder", "merge these notes into one doc", "combine all these files", "turn this folder into a single document", or "/consolidate-folder <path>". Reads markdown, text, Word, PowerPoint, Excel and PDF. Do NOT use for summarising or shortening, for combining source code files, or for git branch or file merges.
---

# Consolidate folder

Eleven documents about the same thing, written at different times, and no way to tell which one is
current. This turns them into a single reference document that loses nothing.

The thing it does that a summary cannot: **where two files disagree, it says so instead of quietly
picking one.** That contradiction was already in the folder. This is what makes it visible.

A warning that belongs up front — this is not a summary. Nothing is dropped, so the output is long.

Requires Python 3 for the two scripts below. No packages to install.

---

## Step 1 — Pre-flight inventory (mandatory, before reading anything)

Run this first and paste its manifest into your working notes:

```
python "${CLAUDE_PLUGIN_ROOT}/skills/consolidate-folder/scripts/inventory.py" "<folder>"
```

If `python` is not found, try `python3`, then `py -3`. If none exist, tell the user Python 3 is
required and stop. Do not fall back to reading the folder by hand, because the scope gate is the
thing that stops a run from failing halfway through with nothing to show.

**The manifest is a contract, not a suggestion.**

- Every `PROCESS` and `EXTRACT` row must appear in the final Source Index.
- Every `FAIL`, `REVIEW`, and `NOTE-ONLY` row must appear in Gaps or Conflicts.
- Files reported identical by hash are **one** source, not two.
- If the script exits `SCOPE: STOP`, read nothing. Report the numbers and agree a narrower scope or
  a batched plan with the user first.

Before writing the final document, reconcile the two lists row by row. Any manifest row you cannot
account for goes in Gaps. Do not imply complete coverage you did not achieve.

Why this exists: a coverage checklist written at the end, from a context that may already have
dropped content, confirms whatever that context still believes. A list generated mechanically before
any reading is the only version that is actually a check.

---

## Step 2 — Read everything, by type

Read every file in full before drafting anything. Organising around the first two files you read is
the standard failure here.

- **Markdown, text, code, config:** read directly. If a `.txt` or `.md` renders as mojibake or shows
  NUL bytes between characters, it is probably UTF-16. Re-read it accordingly rather than merging
  garbled text.
- **Word, PowerPoint, Excel (`.docx` `.pptx` `.xlsx`):** the Read tool cannot open these. Run:
  ```
  python "${CLAUDE_PLUGIN_ROOT}/skills/consolidate-folder/scripts/extract-office-text.py" "<absolute-path>"
  ```
  Use an absolute path. Add `--include-chrome` for Word headers and footers or PowerPoint speaker
  notes. It routes by file *content* rather than extension, so a mislabelled file still works.
  A non-zero exit means the file was **not** read: record it in Gaps with the script's error
  message, never as processed.
  Word keeps headings, tables, hyperlinks and footnotes, and skips tracked-change deletions.
  PowerPoint yields one `## Slide N` section per slide, in deck order. Excel yields one
  `## Sheet: <name>` section per sheet as a markdown table, preserving empty cells so columns stay
  aligned, and resolving shared strings and cached formula values.
- **PDF:** the Read tool handles these, but caps at 20 pages per call and needs an explicit page
  range above 10 pages. Check the page count and read in ranges. A long PDF read without a range
  returns part of the document and reports no error, which is a silent-loss trap.
- **Legacy `.doc` `.ppt` `.xls`, `.pages`, `.key`, `.numbers`:** not supported. These are not zip
  archives and cannot be read without a converter. Do not guess contents from the filename. List
  them in Gaps as "not processed, format not supported" and tell the user that converting to the
  modern equivalent would include them.
- **Images, video, archives:** do not merge or recreate. Reference them: what the file is, what it
  shows, where it lives.

---

## Step 3 — Merge conceptually, not textually

The judgement that makes this worth running.

- **Merge two mentions only when they express the same underlying concept.** Same words is not the
  test; same meaning is.
- **When unsure, keep them distinct and flag the ambiguity.** A superseded draft and a current rule
  can read almost identically. Collapsing them destroys the distinction, and the reader has no way
  to recover it.
- **Never silently pick a winner between conflicting statements.** State both, name which source
  said what, and put it in Conflicts. If two files disagree on a number, a date, or a rule, that
  disagreement is the single most useful thing this run will produce. Resolving it quietly is the
  one unrecoverable mistake.
- **Same basename, different content:** cite both by path relative to the folder (`v2/notes.md`, not
  `notes.md`), never by basename alone.

---

## Step 4 — Structure the output

**Organise by topic, never by source file.** A document with one section per input file is a
concatenation, not a consolidation.

Give each section an inline `*Source:*` line naming which files fed it, so provenance stays
recoverable without the structure being dictated by it.

Standard shape, adapt where the material genuinely calls for something else rather than forcing it:

```
# [Folder name] — consolidated

## Overview
## [Topic sections, as many as the material needs]
## Conflicts
## Gaps and Not Processed
## Source Index
```

**Output path.** Default to `consolidated-<folder-name>.md` in the folder's **parent** directory,
not inside the folder itself. Writing it inside means a second run reads the first run's output as
another source and double-counts every claim, and a third run compounds it.

Before writing, check whether the target exists. If it does, show its size and modification date and
ask whether to overwrite or write to `-2.md`. Never overwrite silently.

**This skill is read-only on its inputs.** Never modify or delete a source file, even if the user's
phrasing ("consolidate and clean up this folder") sounds like it invites tidying.

---

## Step 5 — Reconcile and report

Walk the Step 1 manifest row by row against the Source Index. Report to the user: files processed,
files not processed and why, conflicts found, and anything you could not verify.

If the counts do not match, say so plainly. An honest "48 of 54 files, here are the 6 and why" is
worth far more than a clean-looking document that quietly dropped a third of the material.

---

## Known limits

- Word extraction skips tracked-change deletions and unresolved comments by design, and reports
  when a file contained headers, footers, or comments it did not take. Skipping deletions is not an
  omission: a regex extractor unwraps them into live text, which resurrects deleted content and
  fabricates conflicts between documents that do not actually disagree.
- Excel reads cell values only. Charts, pivot tables, and conditional formatting are not extracted,
  and the script says so when a workbook appears to hold nothing else.
- PowerPoint reads slide text and tables. Images, and text baked into images, are not read.
- Very large folders are gated at 40 files per pass. Above that, batch it and produce a partial
  document per batch rather than attempting one run.
- Encrypted or password-protected documents fail cleanly and land in Gaps.
