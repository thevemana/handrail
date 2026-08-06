# Changelog

All notable changes to handrail are recorded here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-08-06

Three skills already handled *continuity* well — carrying what happened into the next session. None
of them handled *reconciliation*: what to do when two sources say different things, or when a check
quietly didn't run. Retrieval failing is visible; reconciliation failing is not, which is why it was
the half that had gone unwritten. This release closes that gap in the three skills that write state,
adds no new skills, and deliberately invents no new vocabulary to do it.

**Verification:** the hook unit tests pass (21/21) and the plugin manifest validates. Neither says
anything about how a skill behaves in a real session. **This release ships without the live
second-machine install test, and that is a deliberate call, not an oversight** — the same one on
record for 0.2.0 and 0.3.0, which makes this the third consecutive release shipped on doc checks
alone. A full install-test protocol was written for this build — 115 checkable rows across 10 parts,
with 13 fixtures and 5 blocking gates — and none of it has been run; the equivalent for 0.3.0 has
not been run either. A doc-consistency cold-read of the three changed skills, which 0.3.0 did have,
was also not done for this one. Recorded here so the gap is on the record rather than discovered
later.

**One thing this release could not fix.** Four of the changes below (say what you didn't check,
check the copy that will actually be read, the survey's unread-limits line, and putting unverified
claims in the wrap file) all guard failures that leave no trace — which by the new triage rule in
`/handrail:onboard`'s own template means they *should* be hooks, not written instructions. They
can't be. A `PreToolUse` hook intercepts a file operation; none of these is a file operation. They
are about how a conclusion gets reached, which is exactly the layer a hook cannot see. Naming the
gap here rather than leaving it as an unmarked hole in the argument.

### Changed

- **`/handrail:onboard`** — the template gained the reconciliation rules it had no words for, and
  the interview gained the round that produces them:
  - **A "when things don't match" rule in §4**, five lines and no labels: show both sides, say where
    each came from, say which one you'd bet on, then stop and let the person decide. Never settle a
    conflict silently — a conflict resolved without being mentioned is the one nobody gets the chance
    to catch. Conflict preservation is the centre of the argument this plugin makes and it was
    absent from the plugin entirely.
  - **"Say what you didn't check" (§4).** Every answer that came from searching, reading or
    verifying now ends with one line on what it did not cover. A search that quietly skipped half of
    what it should have read returns few results rather than an error, so an incomplete answer looks
    exactly like a clean one.
  - **"Check the copy I'm actually going to use, not the one you have open" (§4).** A claim can be
    true in the file you read and false in the copy someone else opens — a published version behind
    the working one, a cached install, a different branch. This is the error that survives review,
    because the claim really was verified, against the wrong copy.
  - **"If I couldn't defend it with this window closed, you made the decision, not me" (§5).**
    Anything handed over for approval comes with the reasoning in plain words and the one or two
    things it turns on. Being faster without being more right is not worth having.
  - **§2 is now sorted on whether a failure would be noticed, not on how bad it would be.** The
    table gained a "would I notice if it got skipped?" column and the triage rule below it was
    rewritten to sort on that answer first. A rule whose failure is visible can live in a markdown
    file, because a visible miss gets corrected; a rule that can be skipped without leaving a trace
    needs a hook, whatever the damage would have been. Severity is the second question now, not the
    first.
  - **A sixth interview round, on disagreement.** It shows the answer the template already carries
    and asks whether to keep it, rather than asking cold — one extra exchange, not a round of
    open-ended thinking. Long questionnaires fail quietly, so a default-and-confirm was the only
    shape that could carry this without lengthening the interview.
  - **Round 2 gained a second question:** *what kind of wrong answer would you not notice?* The
    existing guardrails question only surfaces damage someone can already picture. This one surfaces
    the failures that look identical to success, and it is what gives §2's new column its first
    honest rows. Nobody volunteers these unprompted.
  - **Step 3 now says the file ships with no confidence scale, and why.** The words arrive with the
    project that needs them, not on day one when there is nothing to rate. Stops someone importing a
    vocabulary they have nothing to use it on, and makes the absence read as a decision.
  - **Plainer words in the file people keep.** §1 "Identity and standing context" → "Identity and
    always-on context"; "Standing assumptions" → "Things that are always true"; §2 "Enforcement map"
    → "What's actually enforced"; "Triage rule for anything new" → "Deciding where a new rule goes";
    §6 "Cascade rule" → "How these files nest". Skill files keep their precise vocabulary — those
    are read by Claude, once, and compression is a virtue there. The template is read repeatedly by
    a person who may be on their first day. The test is not whether a word is difficult, it is who
    reads the line.
- **`/handrail:scaffold`** — the survey already read every file's headers to derive conventions and
  never asked whether they agreed with each other. It does now:
  - **A new survey step: report where the folder disagrees with itself, and do not resolve it.**
    Two task lists with different open items, a README describing a layout that no longer exists, a
    status line contradicted by a dated note elsewhere. Each is reported as a pair — both claims,
    both paths, both dates — and left open. Deriving a convention from a folder that contradicts
    itself, without saying that it does, is how one of the two versions becomes permanent without
    anyone choosing it. The headers were already being read, so this costs almost nothing.
  - **The survey now states its own limits.** It reads the first 5 to 10 lines of each file and goes
    one level into subfolders; that is now said out loud in the report, because a survey's limits are
    invisible in its own output and the confident-looking version is the one that gets acted on.
  - **The `CLAUDE.md` template gained "Where the real answer lives" and "Things that don't match".**
    The first names, per subject, which file settles it and what that rests on — turning "one fact,
    one owner" from a rule into something operable. The second holds contradictions with both sides
    intact; resolving one means deleting the row and saying so, not editing one side into agreement.
  - **Four plain words for how well supported a claim is:** Confirmed, One source only, Sources
    disagree, Not found. Project tier only. Each label describes the evidence, so none of them needs
    looking up, and the column is left out entirely until some subject genuinely has two sources — a
    fresh scaffold rendering "one source only" four rows down just teaches people to stop reading
    the column.
  - **The `MEMORY.md` template's decision rows carry what they were based on**, with "judgment call,
    nothing checked" as a perfectly good value, and the template gained a "Things that don't match
    yet" section. A decision written into memory with reasoning but no source reads as settled fact
    to the next session, which has no way to tell the checked ones from the ones that merely sounded
    right at the time.
  - **The missing `decisions.md` template is written.** It was named in the git-repo file set and had
    no template, so every scaffolded repo invented its own shape. It carries a `Based on:` field and
    a note to write the entry when the call is made rather than at release, since reconstructed
    reasoning is how a guess gets recorded as an analysis.
  - **Writing rule 4 extended:** `live / built / designed / assumed` gained `unconfirmed`. `assumed`
    means nobody checked; `unconfirmed` means someone tried and could not. Extending a vocabulary
    that was already plain, rather than replacing it.
  - **Verify-before-done gained the wrong-copy case**, matching the new template rule: check the copy
    that will actually be used, not the one you have open.
- **`/handrail:wrap`** — the largest single change in this release is that a wrap now reads the ones
  before it:
  - **A new `## Same as last time?` section, which appears only when it fires.** Before writing,
    `wrap` reads the last two or three wraps in the folder. If the same next action or open thread
    has carried across three consecutive wraps, it says so, names the files and quotes the recurring
    line — and stops there, without diagnosing or fixing it. Three is the threshold, not two: twice
    is an ordinary week. This exists because of a documented case where four to six rebuilds happened
    over twelve days and every session ended with a working artifact and a wrap that said done, which
    is precisely why it took twelve days to notice. A per-session log that never looks backwards
    cannot catch a per-project pattern, however honest each entry is. A healthy project never grows
    the heading.
  - **`Decisions Made` gained a "Based on" column** and **`Durable Facts` entries now say where each
    came from.** Durable Facts is the section most likely to be read as established fact months
    later and it carried no evidence at all — the highest-risk manufactured-confidence surface in the
    plugin's own output.
  - **"Confirmed" now has to say how it was checked.** Step 4 required evidence for Stale, Wrong and
    Unverifiable and none for Confirmed, which is backwards: Confirmed is the one verdict that tells
    the next reader to stop checking.
  - **What couldn't be verified goes in the file, not only in chat.** The chat disappears when the
    session ends and the file is what the next session opens, so a wrap carrying no caveats reads as
    one where everything was checked.
  - **When the three-file memory cap stops the check, the files it didn't reach are named** — the
    same move as the existing "no task list, declined". A wrap that silently checked three of six
    memory files reads exactly like one that checked all six.

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

[0.4.0]: https://github.com/thevemana/handrail/releases/tag/v0.4.0
[0.3.0]: https://github.com/thevemana/handrail/releases/tag/v0.3.0
[0.2.0]: https://github.com/thevemana/handrail/releases/tag/v0.2.0
[0.1.0]: https://github.com/thevemana/handrail/releases/tag/v0.1.0
