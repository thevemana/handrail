# Changelog

All notable changes to handrail are recorded here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.1.0]: https://github.com/thevemana/handrail/releases/tag/v0.1.0
