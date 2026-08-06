# Changelog

All notable changes to handrail are recorded here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-08-05

This release rests on two doc-consistency cold-reads — one for `/handrail:scaffold`'s rework, one
for `/handrail:wrap`'s — each a fresh subagent blind to the design conversation, given only the
shipped files. Not the live second-machine install test: that protocol has not been run on this
build. Shipping anyway is a deliberate call for this release, not an oversight.

### Changed

- **`/handrail:scaffold`** — four practices added as defaults, from a line-by-line comparison
  against a real, long-running CLAUDE.md hierarchy that has been in daily use for months. Most of
  what that hierarchy has beyond the skill is personal convention and was deliberately left out —
  `scaffold` bootstraps other people's folders, and nobody should inherit someone else's house
  style from it. These four carry no opinion, so they shipped as defaults:
  - **SemVer plus git tags, proposed for any git repo**, recorded in `CHANGELOG.md` on release.
    Offered alongside the file set rather than assumed, and skipped if the folder already has its
    own working version convention.
  - **A generalized verify-before-done practice.** Before calling a deliverable finished or a
    release shipped, get it checked by someone or something with zero context on the work, and have
    that check try to reproduce the claim rather than read it. Worth a line in the new `CLAUDE.md`
    if the repo ships anything.
  - **A last-check pass before finishing:** re-open every file the run touched and confirm its
    `Last updated:` line actually moved. The rule already existed in the skill; what was missing
    was a step that catches skipping it. Added because the reference hierarchy was caught failing
    this exact rule live, mid-comparison — a correct edit landed with its date stamp untouched.
  - **"Deleting or replacing an existing file" widened to "deleting, replacing, or moving."** A
    rename or a folder move breaks an inbound link exactly like a deletion does, and gets missed
    more often precisely because it doesn't feel destructive.
- **`/handrail:scaffold`** — seven fixes from two independent reviews of the 2026-08-05 rework (a
  cold-read by a fresh agent blind to the design conversation, and a separate session's own review).
  Both independently found the same defect in survey step 4, which is why it is listed first:
  - **Survey step 4 no longer acts during the survey.** It told the model to "fold in" an
    `ideas.md` or `todo.txt` and never said what happened to the original, skipping the skill's own
    deleting-and-replacing rule entirely. Now it flags the candidate, runs the reference search and
    blast-radius statement, and acts only after a yes. New sub-rule for files that are only *partly*
    a disguised task list: extract the matching content, leave the rest in place, never delete a
    whole file for the part of it that moved.
  - **New survey step 5: check existing `plans/` filenames against the naming convention.**
    `plans/README.md` documented `YYYY-MM-DD-short-slug.md` and nothing ever checked against it —
    the same category of gap step 4 already covered for task and memory files, just missing for
    plans. Renames go through the same reference-search-first rule. Old steps 5 and 6 renumbered to
    6 and 7, with both internal cross-references re-pointed.
  - **README and the skill now agree on `plans/`.** Three positions were on record at once: the
    README's walkthrough said `scaffold` writes "an empty `plans/`", the skill's own Templates
    section defines a populated `plans/README.md`, and an older internal note proposed dropping the
    folder entirely until the `save-plan` hook first fires. Resolved in favour of the populated
    folder, for three reasons in order of weight. Git does not track empty directories, so an
    "empty `plans/`" cannot be committed and is gone the moment anyone clones — the real choice was
    populated versus absent. `save-plan` ships off by default, so deferring creation to its first
    fire means the folder never appears at all for most people. And the README is the only thing
    that states the `YYYY-MM-DD-short-slug.md` convention anywhere the user will see it, which is
    also what the new step 5 checks existing filenames against. Would be worth revisiting if
    `save-plan` ever ships on by default, which removes the second reason but not the other two.
  - **`plans/README.md` template gained a `Last updated:` line.** Every other template in the file
    had one, and the skill's own Last-check step cannot be satisfied against a file that never had
    a date line to check.
  - **The `plansDirectory` settings tip says what to do with it.** Previously ambiguous between an
    offer and an FYI, and sitting immediately above a line saying skills cannot change settings.
    Now explicitly offer-and-wait, with a clause separating "a skill enforcing something" from "a
    settings edit the person approved."
  - **A line now connects approval to the Last check.** Nothing linked "approved, now build" to the
    step at the end of the file, so a model could stop after the Templates section and skip it.
  - **"Wiring into the chain" is gated behind approval in its opening line**, matching what its own
    "Become the connector" subsection a few lines later already required of itself.
  - **Eighth fix, found by dogfooding the seventh.** The deleting-and-replacing rule said to grep
    the surrounding tree for inbound references, and ripgrep honours `.gitignore` by default — as
    does `git grep`. The files most likely to hold those references (`tasks.md`, `MEMORY.md`,
    `plans/`, wrap records) are the ones normally kept out of git, so the default search skips the
    highest-density set silently and returns few hits rather than an error. Caught while searching
    for references to one of this repo's own gitignored plan files: a plain grep found zero,
    `--no-ignore` found three. The rule now specifies `rg --no-ignore --hidden -g '!.git/'` and says
    why, because the failure produces a confident "blast radius: none" rather than a visible miss.
- **`/handrail:wrap`** — five additions found by comparing this skill against a stricter
  single-user variant of it, and against a written-up incident in which task files drifted into
  fiction: items described as finished in a narrative paragraph while their checkboxes stayed open:
  - **Memory accuracy check** (new Step 4). Classifies every memory file read from or written to
    this session as Confirmed / Stale / Wrong / Unverifiable, and reports non-Confirmed results in
    the wrap file rather than auto-correcting them. Previously `wrap` would write to memory but
    never checked whether memory it read going in was still true.
  - **Memory guardrails** (same step): a 3-file-per-session cap, a diff-before-write requirement on
    any existing memory file, and a rule to supersede a wrong memory with a dated line rather than
    deleting it.
  - **Routing test for folder placement** (Step 1): "which artifact does this task change?" —
    replaces an unqualified assertion that cwd isn't always the right folder with an actual rule
    for deciding, when work spans more than one location.
  - **Version-history flag** (Steps 2, 3 and 4): if the task, plan, or memory file being written to
    is untracked or gitignored, the wrap now says so, instead of silently treating it as a normal
    versioned file.
  - **Missing-`CLAUDE.md` check** (Step 1): if the folder has no `CLAUDE.md` at all, `wrap` now
    offers `/handrail:scaffold` — the same offer-and-wait pattern it already used for a missing
    `tasks.md`, `plans/`, or `MEMORY.md`, just extended to the one file it hadn't been checking for.
  - Steps renumbered 1–6 (previously 1–5) to make room for the new memory step; the old "memory
    file is the third case" paragraph in Step 3 moved into the new Step 4 rather than being
    duplicated.
- **`/handrail:wrap` doc-consistency cold-read** — a fresh subagent, blind to the design
  conversation, traced all six steps against README.md and reported adversarially. Verdict before
  fixes: **blocking issues** (two direct contradictions in the instructions). 10 of 12 findings
  fixed directly in `skills/wrap/SKILL.md` and `README.md`; 2 judged non-issues:
  - Fixed: the memory 3-file cap read as if it could block Steps 5/6 from running at all —
    clarified the cap only stops further memory work, Steps 5 and 6 still run.
  - Fixed: Step 5's template still offered "no task list here" as a value, the exact phrase Step 2
    tells the model not to use in favor of "declined" — removed from the template.
  - Fixed: Step 4's Check sub-step said it never auto-corrects, with no stated hand-off for who
    performs a confirmed correction, or when — added a line: the correction happens in the same
    step, under the same guardrails, only after the person adjudicates.
  - Fixed: Step 4's Write sub-step only covered "no `MEMORY.md` exists," never the far more common
    case of updating an existing one — added that branch, matching how Steps 2 and 3 already treat
    "no file exists" as the fallback, not the only case.
  - Fixed: no version-history callout for memory files, unlike the ones just added to Steps 2 and
    3 — added the same check to Step 4.
  - Fixed: Step 4 didn't offer `/handrail:scaffold` as the full-set alternative, unlike Steps 1–3 —
    added it.
  - Fixed: newly-created memory files had no carve-out from Confirmed/Stale/Wrong/Unverifiable
    classification, which is meaningless against content that didn't exist before this session —
    added the carve-out.
  - Fixed: "Guardrails on any memory **edit**" header vs. "files **touched**" cap bullet used
    inconsistent scope — both now say "touched."
  - Fixed: Step 6's required chat report omitted plan-file updates — added.
  - Fixed: README's `/handrail:wrap` description never mentioned the new memory-accuracy check —
    added one clause.
  - Not fixed, judged reasonable as written: the "which artifact does this task change?" folder
    test doesn't independently resolve the multi-location tie case — it now explicitly falls back
    to Step 1's existing "main deliverable" rule instead, rather than inventing a second rule.
  - Not fixed, judged out of scope for this pass: Check's "actually read from" scope means a
    session that never opens an existing memory file can honestly report "no memory file applies"
    without an accuracy check ever running. Left as a known limitation rather than mandating every
    wrap open every known memory file, which would be a real scope increase beyond what this
    edit set out to do.

## [0.2.0] - 2026-08-03

A subagent cold-read the shipped skill files for contradictions and ambiguity, given only those
files and no memory of the design conversation; 5 of 8 findings were fixed directly in the skill
files. That check is a documentation-consistency pass, not this repo's usual second-machine
install test, no one has yet run `/handrail:collaborate` or `/handrail:judge` live on a clean
machine. Released on the strength of the doc-check, a deliberate call given the size of this
change, rather than holding for the full protocol `0.1.0` went through.

### Added

- **`/handrail:collaborate`**. Runs several independent readers at once, blind to each other, on a
  draft still in progress or on a decision the user is stuck circling. Cold-read mode gives readers
  zero context; with-info mode briefs them on purpose and audience first. Synthesis names where
  readers agreed and where they genuinely split, and does not average a real split into one
  answer. Suggests concrete fixes. Never grades.
- **`/handrail:judge`**. Runs one evaluator by default, or a panel of them, to give a decisive
  verdict, opinion, critique, concrete fixes, and a grade, on a near-finished artifact. Cold-read
  mode wires the existing blind-cold-read rule to a tool. A panel shows each judge's score before
  describing any spread, rather than opening with one averaged number.

## [0.1.0] - 2026-08-02

First release. Never previously published under any name.

### Added

- **`/handrail:onboard`**. Writes a first `~/.claude/CLAUDE.md` by interviewing the user in five
  short rounds against a portable template, rather than handing over a blank file. Refuses to
  overwrite an existing, substantial file.
- **`/handrail:codify`**. Turns a mid-session "always do it this way" into a well-formed rule
  instead of a raw quote: interviews it into scope, trigger, the rule, an exception, and an
  expectation, then routes it to one of four homes: the global CLAUDE.md, a `~/.claude/rules/`
  file, a project-level CLAUDE.md, or a refusal to write anything if the answers reveal it needs a
  hook instead.
- **`/handrail:wrap`**. Closes out a session into a dated record in `_wraps/`: what was done, what
  was decided and why, what is unfinished, and the exact next action. Reconciles the task list,
  updates plan files, then verifies its own claims against disk.
- **`/handrail:scaffold`**. Gives a folder or repo the files that let Claude resume work in it
  months later: `CLAUDE.md`, `MEMORY.md`, `tasks.md`, `plans/`, plus `backlog.md`, `CHANGELOG.md`
  and `decisions.md` if it is a git repo. Derives conventions from what the folder already contains
  rather than imposing a template, and defers to any state-file convention already stated in
  `~/.claude/CLAUDE.md` instead of its own default `tasks.md` checkbox scheme. The `tasks.md`
  format itself now lives in one place, `skills/scaffold/tasks-format.md`, which `wrap` reads too
  instead of each skill stating its own copy.
- **`/handrail:consolidate-folder`**. Combines a folder of overlapping documents into one reference
  document, surfacing contradictions between files instead of silently resolving them. Reads
  markdown, text, Word, PowerPoint, Excel and PDF.
- **`save-plan.py`** hook, on `PostToolUse` / `ExitPlanMode`. Saves an approved plan to
  `plans/YYYY-MM-DD-<slug>.md` and stops the turn, so approving a plan no longer starts the build.
- **`protect-paths.py`** hook, on `PreToolUse` / `Edit|Write|NotebookEdit`. Refuses writes to `.env`,
  `*.pem`, `*.key`, `id_rsa*`, `secrets/`, `credentials`, `node_modules/` and `.git/`. Allows
  `.env.example` and `.env.template`.
- **`test-hooks.py`**. 21 unit tests covering both hooks and the opt-in gate, runnable before
  trusting them.

**Both hooks ship off.** Nothing fires until `~/.claude/handrail-hooks.json` turns it on, per hook.
`/handrail:onboard` offers to write that file. The switch lives outside the plugin on purpose:
Claude Code auto-updates installed plugins in the background, so anything changed inside one gets
overwritten silently.

[0.3.0]: https://github.com/thevemana/handrail/releases/tag/v0.3.0
[0.2.0]: https://github.com/thevemana/handrail/releases/tag/v0.2.0
[0.1.0]: https://github.com/thevemana/handrail/releases/tag/v0.1.0
