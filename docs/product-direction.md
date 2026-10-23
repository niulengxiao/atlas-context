# Personal agents with a life context you control

**Vision:** help your agent understand the experiences behind your requests, the things that interest you and the tradeoffs you say matter to you. Useful continuity means less repeated explanation, sources you can inspect and room to change your mind.

Atlas Context is intended for developers building personal agents and for people who want to carry a selected, reviewed part of their life context into those agents. Its open-source contribution is a selected-photo reflection flow plus a reusable review and retrieval layer, not a claim of complete life understanding or broad adoption.

## The intended experience

```text
Selected everyday photo clues
              ↓
A question about their meaning
              ↓
Your explanation, correction or refusal
              ↓
Exact wording and disclosure review
              ↓
Task-scoped context with sources
              ↓
More relevant help, with reasons you can check
```

The current companion implements a small version of this path. The system picker supplies up to five chosen images. Apple's on-device Vision classifier selects a tentative scene question from a fixed allowlist (outdoors, food/café, creative or unknown). The person supplies the meaning. Confirmation turns their exact words into an unselected export candidate; edits invalidate confirmation. Existing review, transfer and MCP controls then apply. This is template-based clarification, not an autonomous dialogue or generative image analysis. A long-term preference profile is not implemented.

## A fictional walkthrough

These examples are invented. The first two explanations are runnable in the companion's **Try fictional walk-through** and the Python `personal-assistance` scenario. They are not real user data or outputs from a generative image model.

| Selected clue | A question before interpretation | The person's explanation | Candidate context, only after explicit review |
|---|---|---|---|
| Photos of weekend walks | What do you enjoy about these walks? | I go to slow down. I prefer quiet routes and time without a schedule. | The reviewed wording of that preference, attributed to the person |
| Several cafe photos | Are these places you enjoy visiting, or were the photos for another purpose? | They were for a menu design project. | No cafe-hopping preference; the explanation is shared only if separately selected |
| A small photography portfolio | What role does photography have in your life? | I started learning in 2023 and still see it as a hobby. | A self-reported experience with its reviewed period, if permitted |

For a weekend-planning task, the generated `personal_assistance` instructions ask a connected agent to use relevant approved statements, cite the basis for personal facts, distinguish suggestions from past events, offer alternatives and check whether a preference still applies. The statement about cafés must not be silently converted into an interest in café hopping. A language model and trusted host must be configured separately; the phone itself makes no generative model call.

## What understanding means here

- **Experiences:** what the person says happened and why it mattered, with the available evidence kept distinct.
- **Interests and preferences:** statements the person confirms and chooses to share, with scope and room for change.
- **Perspective:** relevant goals and tradeoffs the person explicitly describes. An agent can consider those while still surfacing missing information, alternatives and costs.
- **Continuity:** the agent uses current, authorized context rather than expecting the person to repeat everything. The current alpha's one-hour sessions are a disclosure mechanism, not a long-term memory system.

Photo frequency alone does not establish meaning. Keep an observation, an uncertain hypothesis and a person's explanation distinct. The user may correct or decline a suggestion without accepting a label. Approval to disclose wording is not independent verification of that wording.

## Privacy is part of the experience

Select a small set rather than defaulting to a complete archive. The companion processes selected pixels locally and holds previews only in memory; no originals, classifier labels or photo identifiers enter its export. Apple's picker may download a selected iCloud photo. The exact outgoing text and metadata appear before saving. An explanation may be more private than its source photo, so selecting a photo does not authorize an interpretation or its disclosure.

Let the person choose context for a particular purpose and recipient, inspect sources and stop subsequent reads. The existing MCP interface does not expose media or approval controls. Host-selected recipient labels are not authenticated identities; local policy does not prevent an untrusted host from copying files. Cloud use discloses approved text, and revocation cannot recall earlier copies. See [PRIVACY.md](../PRIVACY.md).

Corrections on the original phone do not currently update previous desktop exports. Revoke the old session and review a new export. Automatic refresh, preference versioning and durable correction controls need separate implementation.

## A small first trial

Use fictional fixtures first. Then, only in a separately authorized private trial, let a person choose a small representative set, explain a few important moments and review candidate context for one ordinary task. Real data and answers stay outside the source release; sending any of it to a cloud model requires a decision about the exact text.

Compare help for the same task with and without approved context. Ask the person to assess:

1. Does the answer use the preference they actually stated, with the right source?
2. Does it avoid adding an unsupported interest or personality judgment?
3. Is the result more useful for this task, with an explanation they recognize?
4. Can they correct outdated context and stop subsequent access?

Record corrections and failures as well as positive feedback. No user trial, preference-learning benchmark or broad improvement claim is established by the current synthetic transport checks.

## Current foundation and next work

| Area | Status |
|---|---|
| Exact-wording review, source attribution and scoped retrieval | Implemented in Python |
| Selective phone export, full JSON review and desktop connection | Reusable SwiftUI component and fictional companion demo implemented |
| Read-only MCP, expiry checks and future-read revocation | Implemented; tested with protocol clients and limited fictional Codex examples |
| Selected-photo clue extraction and user clarification | Implemented: local Vision, fixed scene questions, user explanations, confirmation invalidation; no generative dialogue |
| Editable, changing interests and long-term life context | Planned |
| Contextual-help path | Implemented task purpose and fictional corrected-preference scenario; usefulness comparison and independent feedback remain planned |
| Production Atlas Memoir integration and physical-device transfer | Unverified |

See the [runnable phone handoff](phone-handoff.md), [validation evidence](evidence.md) and [roadmap](../ROADMAP.md). The vision describes what to build toward; the evidence page describes what has actually been checked.
