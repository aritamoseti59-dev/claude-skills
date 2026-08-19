# SPEC.md — Design-system-first website building in Claude Design

Reconstructed from https://youtu.be/CJ4ndXv3CkY (Productive Dude, "Claude Design FULL
Tutorial: Beginner to Pro"), window 02:52–22:52, by two independent readers:

- **Reading A** — `/watch`: 50 scene-selected frames + English auto-captions, read locally.
- **Reading B** — `notes/gemini-pass.md`: Gemini 3.6 Flash reading the video natively, 2 samples.

Every line is labelled. **CONFIRMED** = both readers agree. **SINGLE SOURCE** = one reader only,
unverified. **CONFLICT → RESOLVED** = readers disagreed and a 1024px frame was pulled to settle it.

Per the method, all timestamps, durations and counts from both readings have been discarded
except where a frame was read directly.

---

## 1. What this is

**CONFIRMED.** A brand-first website production workflow inside **Claude Design**, a GUI surface
in Claude. No code is written, shown, or edited at any point. The build is entirely prompt-and-GUI.

**CONFIRMED.** The governing idea: build a **design system** first, publish it, then generate the
website *from* it. The presenter states the reason plainly — the design system is "the standard
that points the rest of your assets in a certain direction." The website becomes a render of the
brand rather than a thing with a brand bolted on afterwards.

**CONFIRMED.** Worked example is a fictional roofing company, "Apex Roofing" — a landing page plus
dedicated per-service pages, with images deferred to a second pass.

## 2. Stack and prerequisites

| Tool | Role | Cost |
|---|---|---|
| **Claude Design** | Design systems + site generation | Claude subscription — **CONFIRMED** |
| **Opus 4.8 (High)** | Generates the design system and the site | incl. — **CONFIRMED** |
| **Sonnet 4.6 (Medium effort)** | Separate normal-chat research channel for fonts/colours | incl. — **CONFIRMED** |
| **Higgsfield** | External image generation | **paid; tier never shown** — **CONFIRMED** |
| **Recraft V4.1**, vector mode | SVG logo generation | — **CONFIRMED** |
| **Seedream 4.5** | 4K photoreal site imagery | — **CONFIRMED** |
| Google Fonts | Type pairings | free — **CONFIRMED** |

**CONFIRMED.** Claude Design offers three import paths — GitHub repo, local folder, Figma `.fig` —
and the presenter declines all three, uploading fonts/logos/assets directly instead.

**CONFIRMED** (read from frame). Upload panel note: *"This doesn't upload the whole codebase;
Claude will copy selected files. For large codebases, we recommend attaching a frontend-focused
subfolder."* And for Figma: *"Parsed locally in your browser — never uploaded."*

## 3. The method — order of operations

This is the part worth keeping. The order is the technique.

1. **CONFIRMED.** Design systems tab → *Create design system*. The dialogue offers in-app creation
   or *"create it using Claude Code for better fidelity"*. He takes the in-app path.
2. **CONFIRMED.** Name + elevator-pitch blurb first. Purpose is to establish identity, not accuracy.
   Entered: `Apex Roofing` / `A midwestern roofing company serving southwest michigan and surrounding areas.`
3. **CONFIRMED.** Generate the logo **elsewhere, as SVG** — Higgsfield → Recraft V4.1 → vector mode.
   Stated rationale: SVG scales from t-shirt to billboard losslessly, and text/colour stay editable
   without Photoshop work.
4. **CONFIRMED.** Use a **second, cheaper Claude chat** as a research channel. Sonnet 4.6 at medium
   effort, because *"we're not running the most capable model, we're just running a model that can
   do some basic web search."* His stated reason for using a side chat at all is speed: *"it's just
   a lot quicker than asking a general question to Claude Design."*
5. **CONFIRMED (verbatim, both readers).** Font prompt:
   > I want you to list out some Google fonts that would go well together for this company and this
   > brand. Give me four variations of different heading and body fonts that would look good and
   > unique for this brand. I don't want something that looks cliche, but I also don't want
   > something too adventurous. Tell me the best four options for Google fonts.
6. **CONFIRMED (verbatim).** Colour prompt, note the explicit emotional target:
   > I'm going with option four for the fonts. Now I want you to present four color palettes for
   > this company that would invoke trust and still keep it feeling like a local small town
   > roofing company.
7. **CONFIRMED.** Paste the winners into `Any other notes?`, plus a corrective instruction for the
   logo: *"right now the SVG logo that we've dropped in says Durable Roofing. I want it to say
   Apex Roofing in our fonts."*
8. **CONFIRMED — the pivotal step.** Scope the design system *before* generating. He explicitly
   forbids a website at this stage:
   > I want you to create a brand guide and have all of the web components, motion graphic ideas,
   > logo variations, color usage for backgrounds, where and when to use fonts. Don't want you to
   > create an actual website or anything like that. I just want to see what components we can
   > create assets with in the future.
   **CONFIRMED.** The corollary he states: if you *do* know it's for a website, ask for website
   cards, headings, buttons and an initial layout up front.
9. **CONFIRMED.** *Continue to generation* → Opus 4.8 High, runs in background. **Both readers cut
   to the finished state; the generation itself is never shown.**
10. **CONFIRMED.** Review the output as a living document → set `Published`, optionally `Default`.
    Sidebar sections read from frame: `Brand, Colors, Components, Spacing, Type, Motion, Display`.
11. **CONFIRMED.** *New design* → select the design system → write the site prompt.
12. **CONFIRMED.** Answer the clarifying-questions round. Claude interrupts before building:
    *"I have everything I need from the design system. Before I build, a few content questions so
    the trust signals and service pages are right — not guesses."* He calls this round "pretty
    common" — it is expected behaviour, not a failure.
13. **CONFIRMED.** Watch it build live: file dropdown → open `index` → preview.
14. **CONFIRMED.** Generate images in Higgsfield at the exact aspect ratios Claude requested,
    download, rename `image1…imageN` to match the prompt numbering.
15. **CONFIRMED (verbatim).** Map them back: *"insert these images based upon the number and how it
    corresponds to the prompt."*

## 4. The site prompt

**CONFIRMED** (both readers, near-identical). The structural prompt — reproduced because its shape
is the transferable part:

> I want you to create a basic landing page style website that has our free quote form at the top
> of the page on the right hand side and a hero section with some information about our roofing
> company like the fact that we're local and we're a trusted roofing company. I want you to add
> placeholders for all of the background images and all of the images for cards and things and
> **give me a prompt for each of those** so that I can prompt some images and **give me also the
> aspect ratio that you need** for those images, and then I will give those to you after for the
> image phase. […] Then below that I want a services section, then a location section, then a
> bottom hero section that shows the same free quote form just with a bit of a different layout
> for people who scroll all the way to the bottom. We also want a nav and some headers. In the nav
> I want it to start at home, which would be the hero, and have anchor links in there. But for
> services we'll have a service page that each of those cards are linked to […] and services in
> the nav should be a drop-down popover.

Three things make this prompt work, and they generalise beyond roofing:

- **CONFIRMED.** It names *sections in order*, not a vibe.
- **CONFIRMED.** It distinguishes **anchor links** (on-page) from **real routed pages** (services).
- **CONFIRMED.** It defers images by asking for *placeholders + a prompt + an aspect ratio for each*.
  This is what makes the two-pass image workflow possible at all.

## 5. Values entered — verbatim

**CONFLICT → RESOLVED (frame, 1024px, t=08:52).** The colour palette. Reading B reported
`Midnight Slate #182B3A` and a malformed `#F2FE9` / `#FEFE9` — its two samples disagreed with each
other, which is the tell. The frame reads:

```
Deep navy anchors authority. Brick-red accent nods to roofing craft without being on-the-nose.
Midnight Slate  #1B2B3A
Steel Blue      #2E4A60
Rust            #B84C2B
Warm Off-White  #F2EFE9
White           #FFFFFF
```

Palette chosen was **OPTION 01 "Slate & Rust"**; OPTION 02 was "Forest & Grain". Reading A is
correct here; **do not use Reading B's hex values.**

**CONFLICT → RESOLVED (frame, t=07:35).** The fonts. Reading A saw the *options list* —
`OPTION 01 Barlow Condensed / DM Sans`, `OPTION 02 Raleway / Source Sans 3`, `OPTION 03 Fraunces…`.
Reading B saw the *pasted notes field* and reported the selection as **`Instrument Sans +
Plus Jakarta Sans`**. These are not in conflict: he chose "option four", which is below the fold in
every Reading A frame. Reading B gave the same answer in both samples, and the prose immediately
following it in the notes field matches a frame Reading A read verbatim ("…share structural DNA but
have just enough difference in character to give clear heading vs. body hierarchy. Sharp and
professional — leans more tech/SaaS adjacent, which could actually differentiate a roofing company
in a sea of rustic serif logos."). **Treat `Instrument Sans + Plus Jakarta Sans` as the selection.**

**CONFLICT → RESOLVED (frame, t=13:58/14:12).** The questionnaire. Reading B's sample 2 listed six
services; sample 1 listed three. The frame shows checkboxes, and only these are ticked:

- **Services selected:** `Roof replacement`, `Roof repair`, and `new construction` typed into *Other*.
  (Unselected options also on screen: Storm damage response, Roof inspection, Gutter installation
  & repair, Siding, Commercial roofing.) Sample 2 was reading options as selections — **the exact
  failure the two-sample rule exists to catch.**
- **CONFIRMED (frame).** Service areas — **all seven ticked**: `Kalamazoo`, `Portage`,
  `Battle Creek`, `Three Rivers`, `Paw Paw`, `Mattawan`, `Plainwell`. Reading A undercounted from
  audio alone; Reading B was right.
- **CONFIRMED (frame).** Phone: `use a placeholder for now`. Field hint: *"Leave blank and I'll use
  a placeholder like (269) 555-0100."*
- **CONFIRMED (frame).** Trust stats, verbatim: `A+ rating on Better Business Bureau` /
  `500+ 4.7 star average on Reviews` / `Local and Family Owned`.
- **CONFIRMED (frame).** Form fields offered: Full name, Phone, Email, Address / ZIP,
  Service needed (dropdown), Message / details, How soon (timeline).
- **CONFIRMED (frame).** Service pages: `Yes — build full service pages now`.
- **CONFIRMED (frame).** Tweakables, all four ticked: `Hero layout variations`,
  `Quote-form style (card vs. inline)`, `Accent intensity (how much rust)`, `Headline copy options`.

**CONFIRMED.** Resulting site, read from frames: nav `Home · Services ▾ · Location`, phone
`(269) 555-0142`, `Free quote` button. Hero: **"Built to last. Done right, the first time."**
Eyebrow `RESIDENTIAL ROOFING · SW MICHIGAN`. Trust row `A+ · 500+ · Local`. Services section
"Roofing services, done right." Bottom hero variant: "Let's get you a roof that lasts."
Headline tweak options: `built to last` / `local people` / `storm response`. Brand toggle:
`subtle / balanced / bold` (chose balanced).

**CONFIRMED.** Image placeholders render as labelled pinstriped boxes carrying their own spec,
e.g. `Service card — Roof repair · svc-repair · 3:2 · 1200×800`, `hero-bg 16:9`.

**SINGLE SOURCE (Reading B).** The generated image prompts, e.g. hero 16:9: *"Wide cinematic photo
of a roofing crew installing dark charcoal architectural asphalt shingles on a two-story SW Michigan
home; warm late afternoon light, slightly desaturated; clean roof ridge line, shallow depth of
field; framing leaves darker open space on the left third for text."* Reading A saw this panel but
at 512px could not read it. Plausible and stylistically consistent — **unverified.**

## 6. Gotchas

- **CONFIRMED.** Higgsfield 4K output produces files too large to upload. Fix: "save image as" WEBP,
  or generate below 4K.
- **CONFIRMED.** Strip layout language from image prompts. He deletes *"room at bottom for CTA"*
  because the image model "might think that I want text there".
- **CONFIRMED.** A wrong company name in a generated logo is not a problem *if it's SVG* — the text
  is editable downstream. His logo said "Durable Roofing" throughout and he kept it deliberately.
- **CONFIRMED.** File naming is load-bearing. `image1…imageN` must match the prompt numbering or the
  mapping step has nothing to bind to.
- **CONFIRMED (frame).** `Claude Fable 5 is currently unavailable` — banner visible in the side chat.
- **CONFIRMED.** Decide what the design system is *for* before generating it. Wrong scope here costs
  you the whole downstream chain.

## 7. What the video does not show

- **CONFIRMED.** **Deployment.** At ~17:53 he says he'll show how to deploy "today", then pivots to
  ads instead. Nothing about hosting, domains, or publishing appears in this window.
- **CONFIRMED.** **Any code.** No HTML/CSS/JS, no framework, no repo, no terminal, no build step in
  20 minutes. *What the generated site actually is as an artifact is never established.*
- **CONFIRMED.** Both generation steps cut to a finished state.
- **CONFIRMED.** Responsive/mobile behaviour — everything shown at desktop width only.
- **CONFIRMED.** Accessibility, performance, SEO, semantic markup — never mentioned.
- **CONFIRMED (A).** Where the quote form submits. Lead capture is the site's entire purpose and no
  backend, email hook or CRM is discussed.
- **CONFIRMED.** Higgsfield's price or plan tier, despite being required for logo and imagery.
- **CONFIRMED (A).** What Claude Design is and what plan it needs — established before 02:52.

---

## OPEN QUESTIONS

The most valuable output here. These are the things the tutorial never actually taught, which is
precisely the list that will break later.

1. **What is the deliverable?** Never shown. Is the generated site exportable HTML/React, a hosted
   Claude artifact, or something that only lives inside Claude Design? Everything about
   maintainability, version control and deployment depends on this answer, and the video answers none of it.
2. **How does it deploy, and to where?** Promised on camera, then dropped. Outside this window — may
   be covered after 22:52.
3. **Where does the form POST?** A lead-capture site whose form has no shown destination is not a
   working site.
4. **Is the output responsive?** Untested and unmentioned. Desktop-only footage.
5. **What does the design system actually constrain?** It is asserted to "point assets in a
   direction", but the video never demonstrates the site *violating* the system, so its enforcing
   power is unproven.
6. **Editing after generation.** Called a "living, breathing document" — but no edit, re-generation,
   or downstream-propagation of a design-system change is ever demonstrated.
7. **Is Higgsfield actually required?** It is used for both logo and imagery, but nothing in the
   Claude Design flow appears to depend on it specifically. Substitutability untested.
8. **Cost.** Two paid tools, neither priced on screen.
