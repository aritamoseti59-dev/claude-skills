# Claude pass — "Claude Design FULL Tutorial: Beginner to Pro"

Source: https://youtu.be/CJ4ndXv3CkY (Productive Dude, 37:11 total)
Window read: 02:52 → 22:52. Evidence: 50 scene-selected frames @512px + English auto-captions.
Focus: how to build websites properly.

> Scope note: the website material runs 02:52 → 17:53. From 17:53 the video pivots to
> motion-graphic ad creation, which is out of focus for this question. Sections below
> cover the website half; the ad half is noted only where it changes the method.

---

## 1. WHAT IS BEING BUILT

A brand-first website production workflow inside **Claude Design**, a GUI surface in Claude.
The presenter builds a fictional roofing company ("Apex Roofing") end to end: first a reusable
**design system** (logo, fonts, colour ramps, components, motion, spacing), then publishes it,
then generates a **multi-page marketing website** from that design system — landing page plus
dedicated service pages — with image slots left as labelled placeholders that get filled in a
second pass from externally generated images. No code is written or shown at any point in
this window; the entire build is prompt-and-GUI.

The actual thesis, stated at ~08:48: the design system is "the standard that points the rest
of your assets in a certain direction." Build that first, and the website is a render of it.

## 2. STACK AND PREREQUISITES

| Thing | Detail seen | Cost |
|---|---|---|
| Claude Design | "Design systems" tab, "Create design system", "New design", "Back to projects" | Claude subscription |
| Opus 4.8 (high) | Runs the design system generation; ~5 min, backgrounded | incl. |
| Sonnet 4.6 (medium effort) | Separate normal Claude chat, used as a research side-channel for fonts/colours | incl. |
| Higgsfield | External image generation, separate tab | **paid, tier not shown** |
| Recraft V4.1 | Higgsfield model, **vector mode** → real SVG output, used for the logo | — |
| "Seedream 4.5" (heard as "Cdream") | Higgsfield photoreal model, 4K, used for site imagery | — |
| Google Fonts | Source of the type pairings | free |
| Figma `.fig`, GitHub repo, local folder | Offered as design-system inputs — **presenter explicitly declines all three** | — |

On-screen note in the upload panel: *"This doesn't upload the whole codebase; Claude will copy
selected files. For large codebases, we recommend attaching a frontend-focused subfolder."*

## 3. COMMANDS AND CONFIG, VERBATIM

**There are no terminal commands in this window.** Nothing is typed into a shell, no package
is installed, no repo is cloned. Everything below is GUI field content.

Design-system setup fields (frame t=03:24):
- `Company name and blurb (or name of design system)` — placeholder text: *"e.g. Mission Impastabowl: fast-casual pasta restaurant with in-store touchscreen kiosk, mobile app and website"*
- `Link code from GitHub` → `https://github.com/owner/repo`
- `Link code from your computer` → "Drag a folder here or browse"
- `Upload a .fig file` → "Drop .fig here or browse"
- `Add fonts, logos and assets` → "Drag files here or browse"
- `Any other notes?`

Values entered:
- Name: `Apex Roofing`
- Blurb: `A midwestern roofing company serving southwest michigan and surrounding areas.`
- Fonts: chose **option 04** from four generated pairings. Two visible on screen: `Heading — Barlow Condensed / Body — DM Sans` ("Structured, modern, trades-forward") and `Heading — Raleway / Body — Source Sans 3` ("Premium, clean, trustworthy").
- Colours: chose **option 01**, described as "nice and bold". Palette named `"Slate & Rust"` — hex values partially readable: `Midnight Slate #1B2B3A`, `Steel Blue #2E4A60`, `Rust #B84C2B`, `Warm Off-White #F2EFE9`, `White #FFFFFF`. Other options offered: "charcoal and amber".

Design system document sidebar sections: `Brand, Colors, Components, Spacing, Type, Motion, Display`.
Publishing controls: `Published` toggle + `Default` checkbox + `Use this system` / `New design`.

Website prompt outputs — values visible in the built site:
- Nav: `Home` · `Services` (dropdown) · `Location`; phone `(269) 555-0142`; `Free quote` button
- Hero headline: `Built to last. Done right, the first time.`
- Eyebrow: `RESIDENTIAL ROOFING · SW MICHIGAN`
- Trust row: `A+` (Better Business Bureau) · `500+` (4.7 star average) · `Local` (family owned) · `4.7 500+ reviews` · `Licensed & insured`
- Section heading: `Roofing services, done right.`
- Services: `Roof repair`, `Roof replacement`, `New construction`
- Service areas: Kalamazoo (said as "Kazoo"), Portage, Battle Creek, Three Rivers, Paw Paw
- Quote form fields: `Full name`, `Phone`, `Email`, `Address / ZIP`, `Service needed`, `How soon?`, `Anything we should know?` → `Get my free quote`
- Second hero CTA variant: `Let's get you a roof that lasts.` / `Request your free quote`
- Image placeholders rendered as labelled pinstriped boxes, e.g. `Service card — Roof repair  svc-repair 3:2 1200×800`, `hero-bg 16:9`

Headline variants offered by the tweak panel: `built to last` / `local people` / `storm response`.
Brand toggle: `subtle` / `balanced` / `bold` (chose balanced). Form position: below / right. Form style: inline / card.

## 4. THE BUILD ORDER

1. **Design systems tab → Create design system.** A dialogue offers "create one here" or
   "create it using Claude Code for better fidelity" — he takes the in-app path.
2. **Give it an identity first.** Company name + elevator-pitch blurb. He is explicit that the
   point of this field is identity, not accuracy.
3. **Skip the import paths.** GitHub / local folder / Figma are all offered; he says he
   "doesn't typically use these top three" and instead uploads fonts, logos and assets directly.
4. **Make the logo elsewhere, as SVG.** Higgsfield → Recraft V4.1 → vector mode. Rationale given:
   SVG scales to billboard or t-shirt without loss, and the text and colours stay editable
   without "crazy Photoshop work". His generated logo said "Durable Roofing" — wrong name — and
   he keeps it anyway *because* SVG text is editable later.
5. **Use a second, cheaper Claude chat as a research channel.** Sonnet 4.6 at medium effort,
   because "we're not running the most capable model, we're just running a model that can do
   some basic web search". Ask for **four** Google-font pairings, with an explicit taste
   constraint: *"I don't want something that looks cliche, but I also don't want something too
   adventurous."*
6. **Repeat for colour.** Four palettes, with a stated emotional target: *"invoke trust and
   still keep it feeling like a local small town roofing company."*
7. **Paste the winners into "Any other notes"**, plus corrective instruction for the logo:
   *"right now the SVG logo that we've dropped in says durable roofing. I want it to say Apex
   roofing in our fonts."*
8. **Decide scope before generating — this is the pivotal step.** He explicitly tells it
   *not* to build a site yet: *"I want you to create a brand guide and have all of the web
   components, motion graphic ideas, logo variations, color usage for backgrounds, where and
   when to use fonts. Don't want you to create an actual website or anything like that."*
9. **Continue to generation.** Opus 4.8 high, quoted at ~5 minutes, runs in background.
10. **Review the output as a living document**, then set `Published`, optionally `Default`.
11. **New design → select the design system → write the site prompt.** His prompt is long and
    structural, and specifies: hero + quote form top-right, services section, location section,
    repeat hero with the same form in a different layout at the bottom, nav with anchor links
    for on-page sections but *real dedicated pages* for services, services nav item as a
    dropdown popover.
12. **Ask for image placeholders plus a prompt and an aspect ratio for each**, deferring images
    to a later pass. This is what makes the two-pass image workflow possible.
13. **Answer the clarifying questions.** Claude interrupts before building with "quick questions
    before I build the Apex roofing site" — services list, phone, trust stats, service areas,
    form fields, whether to build service pages now, and which tweakable options to wire in.
    He checks **all** tweakables.
14. **Watch it build live** via the file dropdown → open `index` → preview.
15. **Generate the images in Higgsfield** at the exact aspect ratios requested, download, rename
    `image1…image9` to match the prompt numbering.
16. **Drag them in and map them by number**: *"insert these images based upon the number and how
    it corresponds to the prompt."*

## 5. GOTCHAS

- **`Claude Fable 5 is currently unavailable`** — visible error banner in the side chat.
- **4K Higgsfield output produces giant files.** Workaround given: "save image as" WEBP, or
  generate at non-4K.
- **Strip layout instructions from image prompts.** He deletes "room at bottom for CTA" from a
  prompt because "it might think that I want text there in this image generation tool".
- **Name your image files to match the prompt numbers**, or the mapping step has nothing to bind to.
- **Think ahead about what the design system is for.** If you know it's a website, ask for
  website cards, headings, buttons and an initial layout. If you don't know yet, ask for a
  scalable brand guide and no site.
- **The clarifying-questions round is expected, not a failure** — he calls it "pretty common".
- **Use a separate normal Claude chat for ideation**, not Claude Design — his stated reason is
  purely speed: *"it's just a lot quicker than asking a general question to Claude Design."*

## 6. WHAT THE VIDEO DOES NOT SHOW

- **Deployment.** At 17:53 he says "I am going to show you how to deploy this website today" and
  then immediately defers it to pivot to ads. Deployment falls outside this window entirely.
- **Any code.** No HTML, CSS, JS, framework, repo, package manager, build step or terminal
  appears in 20 minutes. What the generated site actually *is* as an artifact is never shown.
- **Both generation steps cut to a finished state.** The 5-minute design-system run and the
  website build are both elided.
- **What Claude Design is, where it lives, and what plan it needs** — established before 02:52,
  outside the window.
- **Higgsfield's price or plan tier**, despite being load-bearing for logo and imagery.
- **Responsive / mobile behaviour.** Everything is shown at desktop width. No mobile preview.
- **Accessibility, performance, SEO, or semantic markup** — never mentioned once.
- **Where the quote form submits.** A lead-capture form is the site's entire conversion goal and
  no backend, email hook, or CRM is discussed.
- **Custom domain, hosting, or what happens after "publish".**
- **Editing or versioning the design system after the fact**, beyond "it's a living document".
