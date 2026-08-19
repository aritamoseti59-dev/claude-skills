---
name: sellable-mobile-apps
description: End-to-end pipeline for building and shipping mobile apps with Claude Code — Expo/React Native + Supabase, from MVP design through store submission and monetisation. Use this whenever the user wants to build, design, scope, ship, or monetise a mobile app or app idea, or mentions React Native, Expo, Expo Go, EAS, App Store or Play Store submission, in-app purchases, paywalls, or app retention. Also use it when they describe an app concept and want help making it real ("I want to build an app that..."), when they ask how to make an app that actually sells or makes money, when they want a habit/calorie/fitness/productivity tracker or any AI-powered mobile app, and when they need a pre-launch security audit or App Store review checklist. Prefer this over ad-hoc coding: the ordering of its stages is the point, and building in the wrong order is the failure mode it exists to prevent.
license: MIT
---

# Sellable Mobile Apps

A fixed pipeline for taking a mobile app from idea to store submission. The stack is
replaceable; **the order is not**. Most failed app builds are correctly-written code
applied in the wrong sequence — designing after the database is live, testing only on
desktop, auditing security after launch, bolting monetisation on at the end.

## Provenance — read once

This skill was derived from a single 4-hour course transcript (Nick Saraev, *How to
Build Mobile Apps with Claude Code*, 2026). Two things follow:

- Sections marked **[from the course]** reflect one practitioner's method, captured from
  one reading of one video. They are opinionated and unverified, not industry consensus.
  Where the reasoning is given, it's given so you can judge it rather than obey it.
- Sections marked **[added]** are **not from the course** — most importantly the entire
  monetisation module, which the course does not cover despite appearing to. Keep this
  boundary visible when you explain your reasoning to the user; they should always know
  which half of the advice carries the source's authority.

## When the builder doesn't code

Assume this by default unless they show otherwise. Most people who want an app can describe
exactly what it should do and have never opened a terminal, and this pipeline works fine for
them — but only if the division of labour is explicit.

**They own the product. You own the execution.** Their judgement is real on: what the app
does, who it's for, what the core loop should feel like, what to cut, what to charge. Your
job is every command, file, config value, and debugging step. Don't hand over a command and
assume they'll know what it does or whether it worked — run it, then say what happened.

Practical rules that matter more than they sound:

- **Define each technical term in a clause on first use, then move on.** "RLS — the setting
  that stops one user reading another's rows" costs six words and prevents silent confusion.
  Not a tutorial, not silence.
- **Surface money before the step, not after.** Apple's developer programme is $99/year,
  Google's is $25 one-off, Supabase and model APIs bill by usage. Someone who doesn't build
  software has no reason to expect these, and finding out at submission is a bad surprise.
- **Flag anything hard to undo before doing it** — publishing, submitting for review, anything
  public or paid. Ask first.
- **Explain the why, briefly, at each stage.** They're learning by watching. The reasoning is
  what transfers to their next app; the syntax isn't, and they can always ask you again.
- **Don't ask them to review things they have no basis to judge.** "Does this code look
  right?" wastes everyone's time. "Should tapping the glass fill it instantly or animate?"
  gets you a real answer, because that's their domain.
- **Errors are normal and worth saying so.** A first-time builder reads a red stack trace as
  having broken something. Say plainly that this is the expected rhythm, paste it into the
  loop, and fix it.

The pipeline below doesn't change. Only who does which part.

## Start here

Before touching code, establish two things with the user:

1. **Which rung of the architecture ladder is the target?** Build in rungs and ship at
   any of them:
   `Local, no API, no DB` → `Local + API` → `Local + API + DB` → `Cloud + API + DB` →
   `Cloud + API + Auth + DB`
   Each rung adds exactly one capability and stays independently testable. Naming the
   target rung up front prevents the most expensive mistake in the whole pipeline —
   adding a database before the design has settled.

2. **Has the MVP been designed?** Not "specced" — designed, using the five-step framework
   below. Its output *is* the build prompt. Skipping it produces an app with ten core
   functions and no reason to reopen it.

### If the user arrives mid-pipeline **[added]**

Most people won't arrive at Stage 1 with nothing built. They'll turn up at Stage 7 saying
"my app works, how do I ship it?" — which means the earlier stages either happened
informally or didn't happen at all.

Don't restart them at Stage 1, and don't just answer the question they asked. Work backwards
and check the stages whose omission has **no observable symptom**, because those are the ones
a working app hides:

- **Security audit (6)** — an insecure app runs perfectly. Nothing about it feels wrong until
  the key is scraped or the bill arrives. Almost always the skipped stage.
- **Auth/RLS on the database (5)** — a single-user test never reveals that every user can read
  every row.
- **Production-build testing (4d)** — Expo Go masks it completely.
- **Retention hook (1.5)** — an app with no reason to return still demos beautifully.

Design and surface-area problems, by contrast, are visible the moment you open the app — the
user already knows about those. Lead with the invisible ones, briefly say why you're raising
something they didn't ask about, then answer what they actually asked.

## Stage 1 — MVP design (before any code) [from the course]

Work through all five with the user. Resist writing code until every slot is filled.

**1. Core function.** The one thing that, if you stripped everything else away, would
still make it the app. A habit tracker's core function is: create a habit, tap it, it
logs. Not the colours, not the settings page.

**2. Core loop.** Turn the core function into an **action → reward cycle, ideally under
30 seconds**. The reward must be *sensory*, not informational: haptics, a chime, an
animation, confetti on completion. Escalating rewards work well — the course's example is
Opal, whose gem grows more elaborate the longer your streak runs.

**3. Accessory features.** Only what supports the loop. History and charts, customisation,
counted-vs-binary variants, optionally social. Anything that doesn't feed the loop is a
candidate for deletion.

**4. Surface area check.** Cap the app at **5–7 screens**. The test to apply: *one
run-through should be enough to onboard a new user.* Beginners ship ten core functions and
a hundred screens; complexity is the default failure, not a risk.

**5. Retention hook.** Design a deliberate **unfinished state** the user must return to.
The course's default is an N-day challenge (3 days), which is structurally retentive
because completing it *requires* three separate sessions across 72 hours. Push
notifications reinforce it.

> **On step 5, be straight with the user.** The course is candid that this is dark-pattern
> territory — engineered incompletion is manipulation, however ordinary. Say so once, offer
> the honest alternatives (genuine periodic value, streaks the user opts into, notifications
> they configure), and build whichever they choose. Don't present manipulation as neutral craft,
> and don't refuse to build a streak feature either. It's their product.

Once all five are filled, the spec is written — feed it to Claude Code as one block. See
`references/prompt-library.md` for the exact shape that works.

## Stage 2 — Build

Dump the whole spec at once and let Claude do a complete first build.

When Claude proposes tackling it in phases, push back. It conserves effort by default:

> `I'd like us to do all of it, including phase 1 through 4. Once done, open in Chrome, not Expo, so I can test locally.`

Immediately after the first rough build, run `/init` to generate CLAUDE.md, then `/clear`.
CLAUDE.md teaches Claude the app's architecture on every future session without re-reading
every file — it lowers cost and stops it hunting for paths. Re-run `/init` once the MVP is
complete, since the file now describes a different app.

## Stage 3 — Design (while state is still local)

**This is the stage most people move, and moving it is expensive.** While all state is
local, design churn costs nothing. Once a live database exists, every layout change that
touches data means a new Supabase schema, deprecated old rows, and a much larger testing
loop. Finish the design *before* you persist anything.

Approach, in order:
- **Emulate, then diverge.** Screenshot an app whose layout you admire and have Claude
  emulate it — you inherit a proven layout and a component library in one step. Then
  change palette, type, and corner radius so the result is not a clone.
  **[added]** The divergence step is not optional. Shipping a visual clone of a named
  commercial app risks both App Store rejection and a trademark complaint. If the user
  wants to stop at "looks exactly like X", tell them why that's a bad idea.
- **Set a palette and enforce it.** Generate a scale, paste it in whole, and require every
  icon and emoji to be monochrome within it. Mixed-colour emoji is the single most common
  reason a vibe-coded app looks cheap.
- **Lux levers:** *reduce* corner rounding (rounded-everything is the default look),
  monochrome icons, one considered display typeface.
- **Harmonise across pages.** Claude restyles what it can see, so pages drift apart. Fix
  the cause, not the symptom: have it screenshot *every* page and itemise defects before
  changing anything.
- **When text prompts stop landing, switch to the visual loop.** If the same instruction
  bounces twice, Claude is misunderstanding the layout rather than ignoring you. Hand it
  Chrome DevTools MCP and let it close the loop itself:
  > `open up in your own Chrome window and screenshot through the app. Enumerate all of the minor incongruencies in design — spacing, margins, alignment — and then fix each in turn.`

## Stage 4 — Test on four surfaces, in this order

Each surface catches a class of defect the previous one cannot, and fixes get cheaper the
earlier you catch them.

1. **Desktop browser** (`localhost:8081`) — fast iteration, zoom, inspect.
2. **Phone mirror** — quick swipe-through with a mouse, no device juggling.
3. **The physical phone via Expo Go — not optional.** Push notifications, haptics, chime
   audio, thumb reach, scroll feel, long-press, and safe-area/notch overlap exist *only*
   here. The course's own examples: icons vertically clipped, and the clock overlapping the
   Dynamic Island — neither visible on desktop.
4. **The production build on a physical device — [added].** All three surfaces above run
   through Expo Go, which means you can pass every one of them without ever executing the
   binary you actually submit. Production builds differ in ways that reliably bite:
   environment variables resolve differently, native permissions are requested for real,
   release-mode optimisations change timing, and anything that worked only because Expo Go
   ships its own native modules will now fail. Run an EAS build and install it before you
   consider testing finished — see `references/shipping.md`.

Budget 10–15 extra minutes for this loop every time. It is not a formality; it is where
device-only defects surface.

**Build testability into the app itself.** Any streak, timer, or multi-day mechanic cannot
be QA'd in real time, so ask for a dev panel: `simulate full challenge completion`,
`force complete challenge`, `reset onboarding`, `clear all data`. Likewise, simulate
30 days of history rather than waiting for it, and render push notifications as in-app
toasts so they're testable in the browser. Verifying a simulation is far cheaper than
discovering the bug after a full three-surface round trip.

## Stage 5 — Database and auth

Auth is not a separate decision. The moment a database exists, it must know whose rows are
whose — adding storage without identity produces an app where every user sees everyone's
data.

Design for **local-first caching**: keep local storage as the immediate read layer so the
app feels instant, then sync to the database periodically. Round-tripping every read to the
network is the difference between a snappy app and a laggy one.

Two things to get right at creation time:
- **Enable automatic RLS (row-level security)** when creating the Supabase project. This is
  what prevents the default-open-policy finding in the security audit later.
- **Choose the region nearest your users.** Distance is latency, and it's painful to change.

**[added] Secrets handling — deviate from the course here.** The course pastes an API key
into chat and a Supabase connection string alongside it, while stating you shouldn't. Follow
the stated rule, not the demonstration: put keys in `.env`, confirm `.env` is in
`.gitignore`, and never paste a connection string or database password into a conversation.
Chat history persists locally, so a pasted secret ends up in more places than the one you
intended. The publishable/anon key is designed to be public; nothing else is.

Then **test again, all three surfaces.** The database changed how the app works and
introduced a new failure surface.

## Stage 6 — Security audit (two passes)

The course's claim: almost everyone skips this, and it's the main thing separating apps
that go somewhere from apps that leak. The realistic goal is not perfect security — it's
raising the cost of attacking you above the cost of attacking someone else.

Run it **only after all three test surfaces pass** and the app is otherwise launch-ready.
Run it **from a cleared context** — an auditor primed by the conversation that wrote the
code will excuse the code it just wrote.

Then run the whole audit **a second time, from another cleared context**, because fixing
one finding routinely creates another. Full procedure and the audit prompt itself:
`references/security-audit.md`.

## Stage 7 — Ship

Production preparation, EAS build, store accounts, the privacy-policy requirement, and the
full App Store Connect field checklist live in `references/shipping.md`. Read it before
starting submission — several items (a reviewer test account, a hosted privacy policy, a
physical Android device for Play) block submission and are easy to discover too late.

## Stage 8 — Monetisation **[added — not from the course]**

**Be honest with the user about this.** The source course has a chapter titled "Monetizing
Your Skills"; it is 90 seconds of advertising for the author's community and contains no app
monetisation methodology. There is no paywall, no subscription integration, no pricing
strategy, no acquisition, no analytics in four hours of material. The one genuinely useful
line is an aside: *pass user requests through your own API key, absorb the inference cost,
charge a subscription with enough margin.* That's the model in a sentence, and it's correct
as far as it goes.

Everything in `references/monetisation.md` is therefore **ours, not the course's** — revenue
model selection, the margin arithmetic for AI features, paywall placement, IAP integration,
and the instrumentation you need to know whether any of it works. Read it when the user asks
how the app makes money, and tell them where the material comes from.

## Steering moves that apply throughout [from the course]

These are the highest-transfer part of the source and worth internalising:

| Situation | Move |
|---|---|
| Claude hands you commands to run yourself | `do this for me in a new terminal window` — it was trained on written guides, so it instructs rather than acts |
| It keeps launching terminals inline | Over-specify: `Make sure it's a fresh terminal, e.g. NOT inside of this thread, but actually on my computer terminal` — an inline server gives no scannable QR code |
| It proposes phases | `I'd like us to do all of it, including phase 1 through 4` |
| It asks you to go set something up first | `I don't yet have X set up, but I'll do that now. Work on everything that you can up until that point.` — never let a human-side blocker idle the agent |
| You have an unrelated fix in mind | Queue it immediately; don't wait for the current task to finish |
| Something errors | Paste the raw error text verbatim, no commentary |
| Context is getting long | `/compact` at 250–300k tokens — quality degrades past ~200k. Do other work while it runs |
| You want to see what it loaded | `Ctrl+O` |
| The spec is long | Dictate it. These specs are long and conversational by design; detail is what makes them work |

Full prompt text for each stage: `references/prompt-library.md`.

## Reference files

- `references/prompt-library.md` — verbatim prompts for every stage, ready to adapt
- `references/security-audit.md` — the two-pass audit procedure and the audit prompt
- `references/shipping.md` — production build, store accounts, submission checklist
- `references/monetisation.md` — **[added]** revenue models, paywalls, IAP, unit economics
- `references/stack.md` — Expo/Supabase specifics, version gotchas, AI-feature architecture

## What not to inherit from the source

The course demonstrates several things it also advises against, or that don't survive
contact with a real product. Don't copy these:

- **"Dangerously skip permissions"** — the course enables it for speed. Don't default to it.
  Mention it exists; let the user opt in knowingly.
- **Secrets pasted into chat** — see Stage 5.
- **Email confirmation disabled** to reduce signup friction — fine for a demo, but it permits
  unlimited fake signups. Flag the trade-off for anything shipping.
- **Two AI passes ≈ "secure"** — it's low-hanging-fruit removal, and worth doing. It is not a
  security review. Anything touching health data, financial data, or bank OAuth connectors
  needs a real one.
- **Skipping TestFlight** — the course skips it for filming reasons and says you shouldn't.
  Ship to real testers before the public.
- **The headline claims** — the $300K/month business, the $50–100M Cal AI exit, "better than
  90% of the App Store". These are the author's, unverified. Don't repeat them as fact.
