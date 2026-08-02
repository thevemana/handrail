---
name: codify
description: Capture something the user just said should be a standing rule, and turn it into a real one, not just appended verbatim, but interviewed into scope, trigger, the rule itself, any exception, and how you'd know it's being followed, then routed to one of four homes depending on the answers — inline in the global CLAUDE.md, a new or existing ~/.claude/rules/ file, a project-level CLAUDE.md, or flagged as needing a hook instead of a written rule. Use when the user says something like "make this a global rule", "always do X from now on", "add this to my CLAUDE.md", "remember this as a rule" (not to be confused with Claude Code's own memory feature, which this is not), or names a correction they want to stick permanently. Do NOT use for one-off preferences that only apply to the current task, and do NOT use if no global CLAUDE.md exists yet (point to /handrail:onboard first).
---

# Codify

The moment a rule is worth keeping is usually mid-conversation, not during a sit-down interview.
This is that moment, turned into a real rule instead of a raw sentence pasted into a file.

**Not a memory feature.** This writes to `~/.claude/CLAUDE.md` or `~/.claude/rules/`, both files
Claude reads at session start or on file touch. It has nothing to do with Claude Code's own Auto
Memory system. If the user says "remember this" meaning "recall it next session" rather than
"make this a rule," that's a different feature — ask if it's unclear which they mean.

---

## Step 1 — Confirm there's a file to add to

Read `~/.claude/CLAUDE.md`. If it doesn't exist, stop and point at `/handrail:onboard` — there's
nowhere for a new rule to live yet, and writing one into a blank file isn't this skill's job.

---

## Step 2 — Interview the raw statement into five parts

Don't write down what the user said verbatim. Ask, briefly, for whatever wasn't already implied by
how they said it. Ask **Scope** first — it decides which of the other four questions even matter,
and it decides Step 3's routing before Step 3 starts.

- **Scope.** Does this apply to everything you do, or just this project or area? If just here, is
  there already a project-level `CLAUDE.md` to add it to, or does one need to exist first (see
  Step 3, case D)?
- **Trigger.** Within that scope, when exactly does this apply — every session regardless of task,
  or only when touching a specific kind of file, folder, or action? "Always" is a valid answer; so
  is "only when editing a CLAUDE.md" or "only in git repos."
- **Rule.** The actual instruction, stated as something Claude can follow, not just a description
  of what went wrong. "Don't do X" is weaker than "when Y, do Z instead."
- **Exception.** Is there a case where this shouldn't apply? Most rules have at least one, and an
  unstated exception is how a rule gets a workaround culture instead of a clean edge case.
- **Expectation / verification — the question that overrides everything above.** If Claude ignored
  this occasionally, what would it actually cost? A correction, or real damage? This one can
  reverse the Scope and Trigger answers entirely: see case C below.

Skip asking about a field the user's original statement already answered clearly.

---

## Step 3 — Route to one of four homes

Four destinations, checked in this order, because Expectation overrides everything before it and
Scope decides between the remaining three.

**A. Applies everywhere, every session → inline in `~/.claude/CLAUDE.md`.** Fold it into the
section that already matches its kind (a guardrail → §3, a pace preference → §5, an output rule →
§7). Written in that section's existing voice — a Guardrails rule reads as a plain "must not"
bullet, not a labelled Scope/Trigger/Rule block. The five fields from Step 2 are what make sure the
rule is well-formed before it's written; they don't have to survive as visible labels here.

Bump the file's `Last updated:` line to today in the same edit. A rule appears in a file whose date
says it hasn't changed in months, and the next reader trusts the date over the content.

**B. Applies everywhere, but only when a specific file pattern is touched → `~/.claude/rules/`.**
Check first for an existing file there whose `paths:` already covers the same pattern, and append
rather than creating a near-duplicate. Create `~/.claude/rules/` if it doesn't exist yet — this may
be the first rule anyone's added. Unlike case A, render all five fields explicitly — a rules file
is single-topic and self-contained, so the structure earns its space:

```markdown
---
paths:
  - "<glob pattern>"        # this is Scope, made mechanical
---
# <topic>
Last updated: YYYY-MM-DD

## <Rule name>
**Added:** YYYY-MM-DD
**Trigger:** <the specific situation or action, within the paths above, that activates this>
**Rule:** <the guidance itself, stated as an instruction>
**Exception:** <when it doesn't apply — or "none stated" if the user confirmed there isn't one>
**Expectation:** <what following this looks like, or how a miss would be noticed>
```

**Naming the file.** Name it after what the glob governs, kebab-case, singular: `**/*.yaml` →
`yaml.md`, `migrations/**` → `migrations.md`, `**/*.test.ts` → `tests.md`. When the pattern has no
obvious subject, name it after the rule's topic instead. The point is that the next rule about the
same thing lands in the same file by default rather than by luck, which is what makes the
check-before-creating step above actually work.

**Dates are not decoration here.** A rule you can't date is a rule you can't audit. `**Added:**`
tells you how long it has been in force, which is the first thing you need when deciding whether a
rule that keeps getting in the way was a good idea. Update the file's `Last updated:` line whenever
you append. Use today's real date; never invent one or copy the date from another entry.

**C. One miss would cause real damage → not a rule at all, regardless of what Scope said.** Say so
plainly: this belongs in a hook, which this skill does not write. If it resembles what
`protect-paths.py` or `block-ai-trailer.py` already do (a path pattern to refuse, a commit-message
pattern to refuse), point at editing those directly — they're built to be edited. If it's genuinely
novel, say building a new hook is real, separate work with its own verification needs, and stop
there rather than writing a paragraph that only asks nicely for something that needs to be
guaranteed.

**D. Scoped to one project or area, not everywhere → that project's own `CLAUDE.md`.** If it
doesn't have one yet, offer `/handrail:scaffold` first rather than creating a bare file here — a
scaffolded CLAUDE.md has a shape this rule should join, not precede. If one exists, add it under
the existing "Conventions" or "Gotchas" section, whichever fits, in that file's own voice, same as
case A.

---

## Step 4 — Show it, write it, verify it

Show exactly what's being added and where, not a diff of the whole file. Get a yes. Write it, then
confirm: the file exists, the addition reads correctly in place, and — for a `paths:`-scoped rule —
the frontmatter is valid YAML with the pattern the user actually described, not a guess at one.

Tell the user where it landed in one line. If it was routed to "needs a hook" instead of written
anywhere, that's the whole report — say so, and stop.
