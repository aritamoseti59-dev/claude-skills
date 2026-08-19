---
name: design-system-site
description: Build a website brand-first — establish design tokens (colour, type, spacing, motion) as the single source of truth, then generate pages that consume only those tokens, with images deferred as a placeholder manifest. Use this whenever the user wants to build, generate, redesign, or scaffold a website, landing page, marketing site, or multi-page site — even if they just say "make me a site for X", "build a landing page", "I need a website for my business", or paste a brand brief. Also use it when a site already exists but its styling is ad hoc and needs consolidating into a system. Prefer this over writing pages directly: pages written before tokens are the failure mode this skill exists to prevent.
license: MIT
user-invocable: true
argument-hint: "<what the site is for> [brand notes, or a link to existing assets]"
---

# design-system-site

Build the system first. Then render pages from it.

The instinct when asked for a website is to start writing the hero section. That produces a
site where every colour is a decision made once and never revisited, and where "make the
brand warmer" means grepping for hex codes. Building the token layer first inverts that:
the pages become a *render* of the brand, and changing the brand is one edit.

## Provenance

This method was reconstructed from a video tutorial (Claude Design, "Apex Roofing" build) via
two independent readings. Lines are marked:

- **[VIDEO]** — demonstrated on camera, verified against frames.
- **[UNVERIFIED]** — one reader only. Reasonable, not confirmed. If it doesn't work, say so
  rather than working around it silently.
- **[ADDED]** — not in the video at all. The tutorial shipped a lead-capture site with no form
  destination, no mobile view, and no accessibility or SEO. Those gaps are filled here and
  labelled, so you always know what came from the source and what didn't.

Full spec with per-line labels: read `references/provenance.md` when the user asks where a
recommendation came from, or when something in this skill turns out to be wrong.

## Step 1 — Scope before you generate

**[VIDEO]** This is the step that pays for itself. In the source tutorial the presenter
explicitly tells the model *not* to build a site yet — he asks only for a brand guide, because
he hasn't decided what it's for. Committing to pages before you've committed to a system means
the system gets retrofitted to the pages, which is backwards.

Establish, and say back to the user before writing anything:

- **What the site is for.** Lead capture, storefront, documentation, portfolio, brochure. This
  determines what components exist at all.
- **How many real pages vs. anchored sections.** A nav item that scrolls is a very different
  build from a nav item that routes. Get this explicit — the video's prompt separates them by
  hand and that is why its nav came out right.
- **Whether a brand already exists.** Existing logo, fonts, colours, or a live site to match?
  If yes, extract tokens from what exists rather than inventing new ones.

If the user hasn't said, ask. Guessing scope is the expensive mistake here, not the slow question.

## Step 2 — Brand research, as a separate cheap pass

**[VIDEO]** Do this as its own step with a *cheaper* model or a web search, not as part of the
build. The tutorial's presenter runs font and colour research in a separate chat on a smaller
model, and his stated reason is speed: he isn't asking for design work, he's asking for
recall of what Google Fonts pair well.

Ask for **four options, not one**, and constrain by feel rather than by aesthetic vocabulary.
The video's prompts, which generalise well:

> List Google fonts that would go well together for this company and this brand. Give me four
> variations of different heading and body fonts. I don't want something that looks cliche, but
> I also don't want something too adventurous.

> Present four colour palettes for this company that would invoke **trust** and still keep it
> feeling like a **local small town** business.

Naming the emotional target ("invoke trust", "local small town") is doing the real work in that
second prompt. "Give me a nice palette" returns the average of all palettes. Ask for four and
let the user pick — they will know instantly which one is right, and they cannot tell you in
advance what it was.

Record the winner with its *rationale*, not just values. The rationale is what keeps later
decisions consistent when someone asks for "a warmer variant".

## Step 3 — Write the token layer, and only the token layer

Create the tokens before any markup exists. Read `references/tokens.md` for the scaffold and
naming conventions.

The rule that makes this work: **no page file may contain a raw colour, font family, font size,
or spacing value.** Every one of them resolves to a token. When you catch yourself typing
`#1B2B3A` or `padding: 24px` into a component, that value belongs in the token layer and the
component should reference it.

Cover, at minimum:

- **Colour** — brand ramp, neutrals, and semantic roles (success / warning / error). Semantic
  roles matter more than they look: they're what stops the sixth developer inventing a seventh red.
- **Type** — a heading face and a body face, with a scale. Two families is usually right; three
  is usually someone losing an argument.
- **Spacing** — one scale, used everywhere.
- **Elevation / radius / motion** — even if minimal. Motion tokens especially, because animation
  added later without tokens is where consistency goes to die.

**[VIDEO]** The tutorial's design system carried exactly these sections: Brand, Colors,
Components, Spacing, Type, Motion, Display. That grouping has held up.

Then write a **component inventory** — the parts the site is made of (button, card, form field,
nav, section header), each rendered once against the tokens. Build this before pages. Pages
assemble components; they don't invent them.

## Step 4 — Ask the content questions before building

**[VIDEO]** In the tutorial, the model interrupts before building with: *"Before I build, a few
content questions so the trust signals and service pages are right — not guesses."* That
interruption is the correct behaviour, and it is worth imitating deliberately.

Ask for the specifics that cannot be inferred and that are embarrassing to get wrong:

- Real service/product names, in the user's own words
- Trust signals with actual numbers — ratings, years in business, certifications, review counts
- Locations or service areas, if relevant
- Which fields the primary form needs
- Phone/email, or explicit permission to use a placeholder

Offer a **"decide for me"** on each. Some users want to be asked; some want you to move. Both
are fine, but placeholder content invented silently is not — it has a way of reaching production.

## Step 5 — Generate pages from the system

Now write pages. Each page assembles components; each component consumes tokens.

**[VIDEO]** Structure the page as an explicit ordered list of sections before writing markup —
hero, then services, then location, then a repeat of the primary conversion block in a
different layout for people who scrolled past the first one. That last one is a real
conversion pattern, not a filler section.

**[VIDEO]** Distinguish clearly, in the nav and in the routing:
- **anchor links** for on-page sections
- **real routed pages** for anything with its own content (each service, each product)
- **dropdown/popover** where a nav item has children

**[ADDED]** Also do these, none of which the video covers:
- **Semantic markup.** One `<h1>`, landmarks (`<header> <nav> <main> <footer>`), real `<button>`
  and `<a>` elements. This is most of accessibility for free.
- **Responsive from the start.** The tutorial is desktop-only footage throughout. Build mobile-first
  or you will rebuild.
- **Form destination.** The video ships a lead-capture site whose form goes nowhere. Decide where
  it posts — mail service, form endpoint, CRM — and if the answer is "nowhere yet", make it fail
  loudly rather than appear to succeed. A form that silently discards leads is worse than no form.
- **Basic SEO.** Title, description, Open Graph tags, sane heading order.

## Step 6 — Defer images with a manifest

**[VIDEO]** This is the sharpest technique in the source, and it generalises far beyond websites.

Do not block page generation on images. Instead emit a **placeholder for every image slot**, and
alongside it a manifest entry carrying everything needed to produce that image later:

| field | why |
|---|---|
| `id` | numbered, e.g. `image-01` — the number is what binds the asset back to the slot |
| `slot` | where it goes: `hero-bg`, `service-card-repair` |
| `aspect` | `16:9`, `3:2` — the layout already knows this; the generator doesn't |
| `dimensions` | e.g. `1200×800` |
| `prompt` | a full generation prompt, ready to paste |

Read `references/image-manifest.md` for the format and a worked example.

Then the user generates images however they like, names the files by number, drops them in, and
you map them back by number. **[VIDEO]** The mapping instruction that works: *"insert these images
based upon the number and how it corresponds to the prompt."*

**[VIDEO]** Two gotchas from the source, both real:
- **Strip layout language out of image prompts.** "Leave room at the bottom for a CTA" makes an
  image generator render *text*. Describe the photograph; let CSS handle the layout.
- **Watch file size.** 4K generations are frequently too large to use directly. WebP, or generate
  smaller.

**[VIDEO]** For logos specifically, prefer **SVG** — it scales without loss and its text and
colours stay editable. The tutorial's generated logo had the *wrong company name* on it for the
entire build and that was fine, precisely because SVG text can be swapped afterwards.

## Step 7 — Expose a few tweakables

**[VIDEO]** The tutorial wires live controls into the generated site — hero layout, form style
(card vs inline), accent intensity, headline copy variants — and toggling them is how the user
actually decides. This is worth copying: people cannot judge "bold vs balanced" from a
description, only from seeing it flip.

Keep it to a handful of consequential switches. Ten toggles is a preferences panel, not a
design decision.

## Step 8 — Run it before you call it done

**Serve it over HTTP.** `python -m http.server 8765 --directory <site>` and open localhost.
Do not judge the site by opening the file directly — `file://` and static preview snapshots
drop relative asset paths, so the stylesheet silently doesn't load and you end up debugging a
styling bug that does not exist. This wasted a cycle the first time this skill was run.

Then check, at minimum:

- **One mobile width and one desktop width.** Confirm the layout actually changes at the
  breakpoint rather than merely not breaking.
- **The primary conversion path, clicked.** Submit the form. If it has no endpoint yet, confirm
  it says so visibly instead of appearing to succeed.
- **Every nav link.** A link to a page you have not written yet is the most common break, and
  the one users find first.
- **Placeholders still visibly placeholder** at real widths.

A site that has never been rendered is a plausible-looking directory of files. The gap between
"the markup looks right" and "it works" is where this actually gets finished.

## Failure modes

- **Tokens drift back into pages.** Someone hardcodes one colour under time pressure and the
  system quietly stops being the source of truth. Grep for raw hex before shipping.
- **Scope changes after the system is built.** Usually survivable — that's the point of the
  layering — but if the site's *purpose* changed, redo Step 1 rather than bending components.
- **The brand research returns four options that all look the same.** The constraint was too
  tight. Loosen the "not too adventurous" half and ask again.
- **User has an existing brand and you invented a new one.** Always check Step 1 for existing
  assets first. Extracting tokens from a live site is faster than inventing and then reconciling.
- **`[hidden]` stops working.** Any component class that sets `display` (e.g. `.field { display: grid }`)
  outranks the `hidden` attribute's user-agent rule, so hidden elements render anyway. Error
  states and status messages are the usual casualties — they appear on first paint, which looks
  broken. Add `[hidden] { display: none !important; }` once, globally, when you write the
  component layer. Found by rendering, not by reading.
