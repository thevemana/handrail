---
name: judge
description: Give a decisive verdict on an artifact — opinion, critique, concrete fixes, and a grade or score — either as a single evaluator or as a panel of judges whose individual scores are shown alongside each other rather than silently averaged. Use when the user wants to know if something is ready, asks to "grade this," "score this," "review this," or wants a final check before sending or shipping something (a resume, README, deck, PRD, pitch, design). Works in two modes: cold-read (the judge gets zero framing and must reconstruct what the artifact is for and whether it holds up — this is the repo's blind-cold-read release rule, wired to a tool) or with-info (the judge is briefed on purpose and audience first). Do NOT use this while the user is still drafting and wants collaborative feedback rather than a verdict — that's /handrail:collaborate. Do NOT silently average panel-of-judges scores into one number without showing the individual scores first.
---

# Judge

One evaluator (or a panel of them) giving a decisive verdict on a finished or near-finished
artifact — opinion, critique, concrete fixes, and a grade. This is the tool for "is this ready,"
not "help me improve this while I'm still working on it" (that's `/handrail:collaborate`).

**This is where the blind-cold-read rule lives as a tool.** The global CLAUDE.md already says:
before calling any build released or any submission final, run a blind cold read — one or two
readers with zero context, told to reproduce every claim live rather than just read it. Running
`/handrail:judge` in cold-read mode *is* that check.

---

## Step 1 — Confirm the trigger and the artifact

Fires on: "is this ready," "grade this," "score this," "review this before I send it," "final
check," or any moment the artifact is about to ship, be submitted, or be sent to someone whose
opinion matters. If the user instead wants suggestions while still iterating, point at
`/handrail:collaborate` and ask which they actually want if it's unclear.

If no artifact was given yet (a path, a folder, or pasted text), ask for it before doing anything
else — don't guess at what's being judged.

---

## Step 2 — Resolve mode

- **cold-read** — zero framing. The judge doesn't know what the artifact is supposed to
  accomplish or who it's for; it has to reconstruct that from the artifact itself, and its grade
  reflects whether the artifact carries its own weight without a briefing. Default for anything
  described as a final check before shipping, matching the repo's existing blind-cold-read rule.
- **with-info** — the judge is told the purpose, audience, and what "good" looks like, then grades
  against that stated bar.

Decide the same way as `/handrail:collaborate` Step 2: explicit statement wins, strong phrasing
gets inferred (state the inference in one line before running), genuine ambiguity gets asked.

---

## Step 3 — Resolve single judge vs. panel of judges

- Default to a **single judge** — one thorough, decisive pass.
- Switch to a **panel of judges** (3, occasionally more) when the user asks for multiple opinions,
  wants more confidence in the verdict than one reader can give, or the artifact is high-stakes
  enough that one judge's blind spot is a real risk (a submission, a release, something going to an
  external audience).
- If running a panel, judges run independently and blind to each other — same mechanism as
  `/handrail:collaborate` Step 4, same reasoning: independence is what makes disagreement in the
  scores mean something.

Name the choice back to the user in one line (single judge, or panel of N) before running it.

---

## Step 4 — Run the judge(s)

Send all judge calls via the `Agent` tool in a single message (multiple tool-use blocks if it's a
panel), so panel judges run concurrently and blind to each other. Each judge gets:

- The artifact, verbatim.
- The mode framing from Step 2.
- An instruction to produce: an opinion, a critique (what's working, what's not), concrete fixes,
  and a score or grade on whatever scale fits the artifact (a letter grade, a 1–10, a pass/fail —
  pick one and state it, don't leave it implicit).

**If it's a panel, pick the scale once, before running any judge, and pass the same scale to
every judge in its prompt.** A 1–10, a B+, and a pass/fail from three different judges can't be
compared, and Step 5's spread only means something if every judge scored on the same terms.

Per the repo's Agent/Workflow model policy, this is mechanical evaluation work — pass
`model: "sonnet"` (or this session's equivalent lower tier) on each judge call. Reserve the
session's default/top-tier model for the synthesis step below when it's a multi-judge panel and the
disagreement needs real judgment to characterize.

---

## Step 5 — Report the verdict

- **Single judge:** report the opinion, critique, fixes, and score directly — this is already the
  verdict, no further synthesis needed.
- **Panel of judges:** show each judge's score individually before anything else — never open with
  an averaged number. Then say whether the panel agrees or splits, and if it splits, say so plainly
  rather than resolving it into one "on balance" grade. A 9-4-8 spread is not a 7; it's three judges
  who disagree, and the user should see that before deciding what to do with it.
- In both cases, end with the concrete fixes, since those are what the user acts on regardless of
  which mode or judge count was used.
