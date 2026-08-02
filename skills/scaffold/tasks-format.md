# tasks.md format

Canonical definition, referenced by `scaffold` (which creates the file) and `wrap` (which
reconciles it). If you're reading this from another skill, this is the one place the format is
defined — don't restate it, link back here.

**This is the default, not a mandate.** If `~/.claude/CLAUDE.md` already states its own
`tasks.md` convention (see `scaffold`'s survey step 6), that wins — use it instead of what's below.

## Checkbox states

`[ ]` open · `[x]` done · `[-]` cancelled · `[~]` in progress · `[@]` blocked on someone else ·
`[?]` needs a decision before it can move.

## Optional date and priority markers

`➕` created · `📅` due · `✅` done · `❌` cancelled · `⏫` high priority · `🔽` low priority.

## Cascade rule — pointer, not rollup

A `tasks.md` never copies a child folder's tasks into itself. If a subfolder has its own
`tasks.md`, the parent adds one line pointing to it. To find all open work under a folder, walk
down the pointers — never assume a parent file is exhaustive. Rollups go stale silently; pointers
can't.

## Template

```markdown
# tasks — [folder name]
Last updated: YYYY-MM-DD

## Open
- [ ] [Task] ➕ YYYY-MM-DD
  [Context: why it matters, what it blocks, what to check first.]

## Subfolders with their own tasks.md
- [subfolder/](subfolder/tasks.md) — [one line on what is open there]

## Recently closed
- [x] [Task] ✅ YYYY-MM-DD
```
