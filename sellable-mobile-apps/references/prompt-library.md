# Prompt library

Verbatim prompts from the source course, organised by pipeline stage. Adapt the specifics;
keep the shape. Where a prompt's phrasing is doing real work, that's noted.

Everything here is **[from the course]** unless marked otherwise.

---

## Setup

```
I want to build a mobile app with Expo and React Native. Set up my workspace for me.
```

```
I'm going to build a mobile app using Claude, Expo and React Native. Should work on all
devices. Scaffold me out the workspace in the current folder.
```

No template download needed — Claude already knows Expo's project structure.

---

## Stage 1–2 — MVP spec and build

### The framework prompt (the most important prompt in the skill)

State the framework *as a framework*, then fill each slot. Naming the five parts up front
makes Claude organise its plan around them rather than producing a flat feature list.

```
I'm using an app framework where I define a core function, then a core loop, then
accessory features, then minimize the surface area, and then finally add some sort of
retention hook. My goal is to build [APP DESCRIPTION].

My core function will be [THE ONE THING — what the user creates/does and what gets
recorded].

The main action to reward cycle will revolve around [WHAT THE USER DOES] and [HOW THEY'RE
REWARDED]. It needs to be visually stimulating, there needs to be some form of haptic
feedback, and ideally there's some sort of sound like a chime. Also we need some form of
challenge — if they're embarking on a [N]-day challenge, which might occur immediately
after onboarding, at the end of that challenge we also need to reward them for the
fulfilment of their efforts.

The accessory features for this app are going to be [LOGGING / HISTORY / CHARTS /
CUSTOMISATION]. Be aware that [BINARY ITEM] is different from a volume-based [ITEM] where
you need to do it three or four times a day.

For surface area check, just make sure that we don't have more than somewhere between five
to seven screens in our app. We want it to be as simple as possible.

In terms of retention hook, we want to create challenges for the user and have some sort of
ongoing thing that checks in with them via push notifications once a day or maybe a couple
of times a day.

We'll do all of this locally to start and then eventually migrate this over to a database
later.
```

The final line matters — it names the rung on the architecture ladder and stops Claude
reaching for a database on day one.

### Forcing a complete build

```
I'd like us to do all of it, including phase 1 through 4. Once done, open in Chrome, not
Expo, so I can test locally.
```

### Memory

```
/init
```
Run after the first rough build, then `/clear`. Re-run once the MVP is complete so
CLAUDE.md describes the finished app rather than the prototype.

---

## Stage 3 — Design

### Emulate a reference app

```
I love the design of the app that I just screenshotted over to you. I want you to start by
emulating that design. Right now the design is pretty weak. I'd like you to upgrade it so it
more or less looks exactly like this app does, just without the logo — rather than call it
[THEIR NAME], call it [YOUR NAME]. After we're done modifying the design and building in a
reasonable library of components, I'll modify the design so that the end result looks a
little different.
```

**[added]** Follow through on that last sentence. Stopping at the emulation stage leaves you
with a clone, which is both an App Store rejection risk and a trademark problem.

### Palette and type

```
Update colour scheme so it looks like this: [PASTE FULL PALETTE]. Also make sure all icons
and emojis are monochrome, e.g. they're of the same colour as that palette. Important we
stick to that palette from now on. Also focus on reducing the corner rounding just a tad to
make it feel higher end.
```

### Harmonise across pages

```
I'm noticing that there are slightly different types of designs on each different page. For
instance the homepage has an outline around each card, whereas the profile page doesn't. I
want you to remove outlines around all cards and favour clean, minimalistic design over busy
design. Also the homepage is very compressed and stacked up top — distribute each of the
elements a little more organically.

Make sure that when you do a test, you actually run through every single page, take a
screenshot of it, and itemize anything that may be sub-optimal before modifying it on your own.
```

### Self-looping design pass

```
Go through the design page by page and then itemize and enumerate a list of all possible
improvements you can make to make it higher-end, sleeker, and more lux. Self loop as many
times as you need to implement all of that design functionality.
```

### The visual loop (when text prompts stop landing)

```
Open up in your own Chrome window and screenshot through the app. Enumerate all of the minor
incongruencies in design — so spacing, margins, alignment on left and right sides, etc. — and
then fix each in turn. E.g. [SPECIFIC EXAMPLE] is still out of alignment. Want this fixed in
a mobile responsive way.
```

Reach for this when the same instruction bounces twice — that's the signal Claude is
misreading the layout, not ignoring you.

---

## Stage 4 — Testing

### Start the dev server (phrasing matters)

```
Start an expo server for this in a new terminal window.
```

If it keeps launching inline:

```
Open up a fresh terminal for me, and then run the Expo server. I'll take a QR code pic and
then use that to open on my phone. Make sure it's a fresh terminal, e.g. NOT inside of this
thread, but actually on my computer terminal.
```

An inline server produces no scannable QR code, so this isn't cosmetic.

### Build a dev/test panel

```
I need some sort of testing view for a developer so that I can modify the day of the
challenge, or at least trigger the event that occurs when we hit 3 days out of the 3-day
kickstart. Right now I just have to trust that it's working, but I'd like to really have it
work.
```

Typically yields: `simulate full challenge completion`, `force complete challenge`,
`reset onboarding`, `clear all data`.

### Simulate state

```
I'd like to test this out with simulated history. Come up with a way that I can quickly
generate or test these, because I'm going through an end-to-end test right now.
```

### The QA round closer

```
With all that in mind, go through everything top to bottom, implement those changes, and
then just open it up in another Chrome tab. I'll test it.
```

### Errors

Paste the raw error text. No commentary, no summarising — the stack trace is the signal.

---

## Stage 5 — Database and auth

```
I'd like to add a database to this project. In addition to a database, I also want local
caching so the user has a very immediate and snappy experience when they use the app. We're
going to be using Supabase. And in addition, we're going to need to set up user
authentication so that you know which user is accessing which data. Help me through this
process.
```

### Parallelising a blocker

When Claude asks you to go set something up first:

```
I don't yet have Supabase set up, but I'll do that now. Let's go with email and password.
Work on everything that you can up until that point.
```

Then, once cleared: `logged in`

### Version control

```
Create a GitHub repo for this, and a readme, then push.
```

Worth doing early and specifically because you're letting an agent edit the codebase — you
want a cheap path back to a working state. Note that renaming a project folder ends the
current Claude session, so rename before you're deep in one.

---

## AI features

```
I'd like to implement [FEATURE] into our application. I want you to use Claude as the
backend and then send the request via Supabase Edge Functions. Use pretty smart models —
let's use the Sonnet models. And you'll also have to update the database to ensure that it
works alongside the flow diagram that I'm attaching.
```

Attaching a screenshot of a hand-drawn architecture diagram works well. Zoom out before
screenshotting so you're not spending context on unreadable detail.

### Always sample generated output before shipping it

```
Go through and send me 10 examples of [GENERATED CONTENT TYPE].
```

You're prompt-engineering the *inner* prompt — the one your app sends at runtime — and you
can't do that without seeing its range. Refinements from the course:

```
Modify the prompt so Claude does not output any em dashes. Em dashes are very typically AI,
and the more we have the less humanlike the messages seem.
```

```
Add some emojis to these titles specifically. I just want the titles to have emojis, I don't
want anything else to have emojis.
```

---

## Stage 6 — Security

Two passes, each from a cleared context. Full procedure in `security-audit.md`.

**Pass 1:** `/clear` → paste the audit prompt →
```
Run through and fix all of these errors end to end. After you're done, test and ensure
they're 100% solved.
```

**Pass 2:** `/clear` → paste the *same* audit prompt again →
```
Great work. Fix all things even if they're partial. Once sorted, let me know if the changes
produced new vulnerabilities.
```

---

## Stage 7 — Shipping

```
Generate app.json and eas.json for production. Include the app name, bundle identifier,
version, a 1024x1024 icon, splash screen, and an Android adaptive icon. Check that all
required permission declarations are present for the features this app actually uses.
```

```
I'm submitting an app called [NAME] to the App Store. Here are the submission guidelines
[PASTE]. Create a privacy policy and a support page for it.
```

Generating compliance pages from the store's own published requirements is the single
biggest time saving in the submission process.
