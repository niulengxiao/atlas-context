# One fictional task, three context conditions

These are actual Codex host outputs from 2026-10-23, using the installed Atlas Context `0.4.0a2` package. Each condition used a fresh ephemeral host. Shell, web and other app tools were disabled. Only the two context-enabled conditions had Atlas Context MCP connected. All input was invented; there were no personal photos or life records.

## The shared request

> Help me plan a relaxed day off with two options. Explain which parts are based on what you know about my preferences. Do my café photographs establish café-hopping as my hobby? If you do not have evidence, say so. Keep the answer under 160 English words.

## Conditions and observed behavior

| Condition | Personal evidence returned | Citations matched to tool results | Manually observed behavior |
|---|---:|---:|---|
| No personal context | 0 | 0 | General options; explicitly says no evidence of specific preferences or a café-hopping hobby |
| Original reviewed context | 2 user statements | 2 | Uses quiet walks, photography and flexibility; attributes café photos to work |
| Newly reviewed correction | 2 user statements | 2 | Uses a scheduled indoor art workshop, states the earlier outdoor preference does not apply, and retains the café-work correction |

Original context: a fictional person likes quiet walks and flexible plans; their café photographs were for a work assignment. Before the third condition, the test explicitly revoked that session and confirmed that its next read failed. A separate newly reviewed export stated a preference for a structured indoor art workshop for the current request. Both cloud test sessions required explicit phone and desktop opt-in for these known fictional statements; both were revoked at the end.

The mechanical checks verified successful MCP calls, two returned records in each connected condition, zero calls in the baseline and exact citation-ID matches. The interpretation of the advice was inspected manually. No blinded assessment or real-user usefulness score was collected. The context-enabled conditions also used the generated task instructions, so these examples do not isolate a causal effect of context alone.

## Without personal context

> Here are two flexible options based only on your request for a relaxed day off:
>
> 1. **Stay close to home:** Have an unhurried breakfast, take a short walk if you feel like it, and leave the afternoon open for an activity you choose. Keep dinner simple.
>
> 2. **One gentle outing:** Pick a nearby park, museum, or café, with no pressure to visit multiple places. Allow plenty of downtime afterward and keep the evening unscheduled.
>
> The relaxed pace reflects your stated request. The activities are general suggestions; I have no evidence about your specific preferences.
>
> I haven’t seen your café photographs. Even if available, photographs alone wouldn’t establish café-hopping as your hobby—they could reflect occasional visits or an interest in photography. Calling it your hobby would require clearer evidence, such as your own description.

## With original reviewed context

> You said you enjoy quiet outdoor walks and photography on days off, and prefer flexible plans over crowded schedules. [E-926cd07a8e175eb6]
>
> Two suggested options:
>
> 1. **A gentle outdoor day:** Take an unhurried walk somewhere quiet, bring your camera, and leave the afternoon open. This draws directly on your stated preferences; the location and timing are suggestions.
> 2. **A mostly at-home day:** Have a slow morning, choose a leisurely activity, and keep a short photo walk optional. This offers fewer commitments, though I have no evidence that you prefer staying home.
>
> The tradeoff is more outdoor time versus less structure and effort. Does your preference for quiet walks, photography, and flexible plans still apply?
>
> **No—your café photographs do not establish café-hopping as your hobby.** You explicitly said they were for a work assignment and did not mean you enjoy busy cafés. [E-04ee9956873cb769]

## With newly reviewed context

> You said you want a **structured indoor art workshop with a scheduled start**, and that your earlier preference for an unplanned outdoor day does not apply here. [E-35a66147e60e7004]
>
> Two suggested plans—not bookings or past events:
>
> 1. **Morning painting:** Choose a scheduled beginner workshop, then have an easy lunch and leave the afternoon free. This offers structure early and flexibility afterward.
> 2. **Afternoon pottery:** Keep the morning slow, attend a scheduled introductory class, then enjoy a simple dinner. This leaves more downtime before your activity.
>
> The workshop structure follows your stated preference; the art forms, meals, and pacing are my suggestions. Does that workshop preference still apply?
>
> **No, your café photographs do not establish café-hopping as your hobby.** You said they were for a work assignment and do not mean you enjoy busy cafés. I have no approved evidence establishing that hobby. [E-dada4463a13b1c38]

## Reproduce the workflow

1. Generate an active original fictional session with `python3 -m atlas_context.phone demo --scenario personal-assistance --output ../atlas-comparison-original`.
2. Generate the correction walkthrough with `python3 -m atlas_context.review_demo --output ../atlas-comparison-correction`. Its `original-session` is deliberately revoked; use only `corrected-session` for the new preference.
3. Use separate fresh hosts for no context, the original session and the corrected session. Follow [MCP setup](mcp.md), use each connected session's generated task instructions, and give the shared request above. The generated sessions are local-only: use a local model/host, or separately review and explicitly opt in for cloud use. Do not change a personal file's disclosure mode merely to reproduce this example.
4. Check each personal claim against returned wording and each citation against the tool response. Record failures as well as successes. Model answers and citation IDs will vary.

This is an inspectable demonstration, not a benchmark or proof of improved real-world help. Fresh hosts do not test whether an existing conversation forgets old answers. Revocation cannot recall copied text, model history or earlier responses. No automatic phone refresh, durable preference model or universal prompt-injection protection is implied. See [validation scope](evidence.md) and [privacy boundaries](../PRIVACY.md).
