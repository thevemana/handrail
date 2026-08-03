---
name: collaborate
description: Get independent, blind-to-each-other reactions and concrete suggestions on a draft or an open decision — from multiple perspectives at once, without collapsing their disagreement into a single averaged answer. Use when the user is still shaping something (a draft, a plan, a pitch) and wants feedback from more than one angle, or when the user is visibly stuck choosing between options — going back and forth, restating the same tradeoff, saying "I don't know" or "not sure which way to go." Works in two modes: cold-read (readers get zero framing and react blind) or with-info (readers are briefed on purpose and audience first). Do NOT use this for a final go/no-go verdict, a grade, or a score — that's /handrail:judge. Do NOT auto-run when stuck-ness is only mildly implied — offer it first and let the user opt in.
---

# Collaborate

Multiple independent readers, working *with* the user to improve a draft or clarify a decision —
not grading it. The value is disagreement surfaced honestly, not smoothed into one voice.

**Not a verdict tool.** If the user wants "is this good enough," "grade this," or "final check
before I send it," that's `/handrail:judge`, not this. If it's ambiguous which the user wants, ask.

---

## Step 1 — Confirm the trigger and the artifact

Two situations this fires on:

- **A draft or plan that isn't finished** — the user wants feedback while still iterating.
- **The user is stuck between options** — repeating the same tradeoff, saying they're not sure,
  going in circles on a decision rather than a document.

For the second case, offer it rather than run it silently: *"You've gone back and forth on this a
few times — want a few independent takes on it, blind to each other, to see if there's real
disagreement or you're just missing one angle?"* Only proceed once the user says yes.

For the first case (an explicit ask — "get some feedback on this," "what do a few different people
think of this draft") just proceed to Step 2.

Either way, if no artifact or decision has actually been given yet (a path, a folder, pasted text,
or a stated set of options), ask for it before doing anything else — don't guess at what's being
read.

---

## Step 2 — Resolve mode

Two modes, and they change what goes in each reader's prompt, nothing else:

- **cold-read** — the reader gets the artifact (or the decision + its options) with zero framing.
  No stated purpose, no stated audience. They have to reconstruct what it's for and react to what's
  actually on the page. Fits "does this explain itself to a stranger."
- **with-info** — the reader is told the purpose, audience, and what "good" looks like before
  reacting. Fits "does this land for the people it's actually for."

**Decide which:**
1. If the user states it explicitly (a flag, or clear phrasing like "cold read this" / "read this
   blind"), use that.
2. If phrasing strongly implies one — "does this even make sense to someone who doesn't know the
   backstory" implies cold-read; "will this land with a hiring manager" implies with-info — infer
   it, but say which mode was picked and why in one line before running readers.
3. If genuinely ambiguous, ask directly rather than guess — the two modes answer different
   questions, and guessing wrong wastes the whole run.

---

## Step 3 — Resolve the readers

- If the user names perspectives ("a skeptical peer and a hiring manager," "what would my target
  user think"), use those.
- If none are named, default to 3 — enough to see real disagreement without the synthesis turning
  into a list. Pick perspectives that fit what's being read: for a draft, a target reader, a
  skeptical peer, and a domain expert; for a decision, one perspective per option's strongest
  case, plus one optimizing for whatever the user has said matters most (speed, risk, cost, and
  so on). For an artifact type not covered by either example (code, a spreadsheet, a business
  plan), pick 3 perspectives a real stakeholder in that kind of artifact would actually hold —
  don't default to the draft list just because it's written down first.
- Name the chosen readers back to the user in one line before running them, so a bad default can be
  swapped before the fan-out runs.

---

## Step 4 — Run readers independently, blind to each other

Send all reader calls via the `Agent` tool in a single message with multiple tool-use blocks, so
they run concurrently — and so none of them can see another's output before producing its own. Each
one gets:

- The artifact or the decision + its options, verbatim.
- Its assigned perspective.
- The mode framing decided in Step 2 (purpose/audience stated, or deliberately withheld).
- An instruction to react as a collaborator, not a grader: what's confusing, what they'd tighten,
  what they'd cut, and 2–3 concrete suggested fixes stated as actions ("cut the second paragraph,"
  not "the second paragraph could be tightened") — explicitly **no score, no grade, no pass/fail
  verdict**.

Per the repo's Agent/Workflow model policy, this is mechanical fan-out — pass `model: "sonnet"` (or
this session's equivalent lower tier) on each reader call rather than letting it inherit the
session's default tier.

---

## Step 5 — Synthesize without averaging

Report back in this shape:

- **Where readers agreed** — the suggestions that showed up from more than one angle unprompted.
- **Where they genuinely split** — stated as a split, not resolved into a single "on balance"
  answer. If three readers land three different places, say so; don't pick a winner for the user.
- **Concrete fixes**, attributed to whichever reader raised them, so the user can weigh the source.

Never collapse a real disagreement into an averaged middle position — that defeats the reason this
exists instead of one single Agent call.

---

## Step 6 — Report

One short synthesis, not a transcript of all N reader outputs unless the user asks to see them
individually. If a decision was the subject (not a draft), end with what the split implies for the
choice — still without picking it for the user.
