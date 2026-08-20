---
name: poster-studio
description: Design and render advertisement posters and flyers — club nights, events, product promos, any advert meant to be shared. Composes typography in HTML against a locked design system and renders exact-pixel images with Playwright, sourcing photography from uploads, background removal, or Higgsfield generation. Use this whenever the user asks for a poster, flyer, advert, promo graphic, event graphic, or artwork for a night, show, launch or offer — including when they only describe an event and want something to post, say "make me something for Saturday", ask for a solo variant of an existing poster for one artist, want a story-sized cut, or hand over a lineup and a date. Prefer it over generating a poster image directly: an image model cannot hold exact brand colour, tracking, or verbatim legal copy, and holding those is the entire point of the system.
---

# Poster Studio

A working poster system, derived from 15 real posters produced for The Echo
Lounge (Kisii) and four out-of-town venues. Read
`references/design-system.md` before composing — it carries the tokens,
zone stack, roster rule and copy tokens that the rest of this file assumes.

## Why the work is shaped this way

Posters get composed in **HTML and rendered with a headless browser**, not
generated as images. That looks like the long way round until you notice what
the poster has to hold:

- an alcohol disclaimer that is a licensing requirement and must be
  letter-perfect
- performers' names, spelled right, every time
- exact brand hex values and exact letter-spacing
- a phone number people will dial

Image models cannot hold any of that reliably. They will eventually misspell
the disclaimer, drop a letter from a DJ's name, or shift the gold. The reference
set already carries two spelling errors that propagated across eight posters
simply from being retyped — the failure mode is real and it is expensive.

So: **image models make the pictures, the browser sets the type.** Photography
comes from uploads or generation; every glyph is composed in HTML where it can
be pasted from a token and verified.

## Workflow

### 1 · Take the brief

Fill this out before opening the template. Fields marked **required** cannot be
guessed, because guessing produces an advert that misinforms people.

| Field | Zone | Notes |
|---|---|---|
| Event or offer name | 3 | The title. Two or three words if possible. |
| Date **with year** | 1 | required |
| Start time / doors | 8 | **required** |
| Entry price | 8 | **required for ticketed shows**, not for regular nights — see below |
| Venue name + address | 6 | required |
| Contact number | 8 | required |
| Lineup / roster | 5 | Names in billing order |
| Presenter line | 2 | optional |
| Script subtitle | 3 | optional — *Pre Valentine Party*, *Fridays* |
| Dress code, sponsor | 6 | optional, as an extra lockup cell |
| Socials | 9 | house events only |

**Ask for everything missing in one message, not one question at a time.**

**Price behaves differently from time, and the distinction is the client's, not
yours.** A regular club night — a weekly, a residency, a themed evening — does
not normally carry a gate price in this market, and putting one on is wrong, not
merely unnecessary. A *ticketed show* — a headline act, a tour date, a
gated concert — does, with tiers and a paybill or till number, as the Rirongo
Show poster does. So don't demand a price for a weekly. Establish which kind of
event this is, then require the price only for the ticketed kind.

Door time is different: it is useful on both, and it costs nothing to state.

Never invent either. No poster in the reference set carries a start time — that
gap is what this skill exists to close, and filling it with a plausible-looking
guess is worse than leaving it out, because a wrong time sends people to a
locked door. If the user cannot supply a field, omit it and say plainly what the
poster is going out without.

**Check the weekday against the calendar.** "Friday 13th February 2026" must
actually be a Friday. All 15 reference posters got this right; it is a cheap
check and an embarrassing miss.

### 2 · Choose the treatment

Three decisions, made once:

- **Composition variant** — A split / B stacked / C centred. B is the house
  default. See `design-system.md` §3.
- **T1 display voice** — premium / hype / funk / blunt / tech. Match the event,
  not your preference: a headline tour is hype, a brand weekly is premium, a
  throwback night is funk. `references/fonts.md` gives the verified face per
  voice.
- **Background direction** — house TV-and-radio wall for a regular night, or a
  deliberate break for a special.

Everything below the credits line stays constant regardless. That is what makes
varied posters still read as one studio.

### 3 · Get the images

Read `references/assets.md`. In short: supplied photos first, background
removal via Higgsfield `remove_background`, generation only for backgrounds,
textures and anonymous figures.

**A named real person requires a supplied photograph.** Generating a face for a
named performer fabricates a real person's likeness on material that will
circulate publicly under their name. If there is no usable photo, say so and
offer a type-led cut instead — the system carries a poster on zones 3 and 5
alone.

### 4 · Compose

Copy `assets/poster.html` into the project and edit it. Everything meant to
change is either a custom property in `:root` or a block marked `FILL`.

```bash
cp ~/.claude/skills/poster-studio/assets/poster.html ./poster.html
```

Set the body class to the chosen variant (`var-a` / `var-b` / `var-c`), point
`--t1-family` at the chosen voice, swap the fallback background for a real
image, and drop cutouts into the `.talent` layer.

Paste the legal and social strings from `design-system.md` §7. Do not retype
them.

### 5 · Render

```bash
python ~/.claude/skills/poster-studio/scripts/render.py poster.html out/poster.jpg
```

Options: `--width` / `--height` for other sizes, `--scale 2` for print,
`--quality` for JPEG.

**Exit codes carry meaning. Read them.**

- `0` — rendered, dimensions verified, all fonts resolved
- `1` — render failed, or the output is the wrong size
- `2` — **a font silently fell back.** The poster rendered in the wrong
  typeface and still looks finished. Fix the font spec and render again; do not
  ship a `2`.

Exit 2 exists because the system font list and the browser's font namespace are
different namespaces, and a face can enumerate as installed while resolving to
Times. `references/fonts.md` explains it. The "roughly a fifth fail" rate was
measured on Windows/DirectWrite; the mechanism holds identically on
macOS/CoreText, but the rate here is unmeasured — and the verified font map in
`references/fonts.md` is Windows-only. Read its warning before composing.

The renderer also warns on content overflow — a poster that scrolls has
overflowed its canvas and the export is cropped.

### 6 · Look at it — beside the reference, not alone

Open the rendered image and inspect it. A clean exit code means the render
mechanism worked, not that the poster is right.

**Build a side-by-side against a reference poster at matched height and look at
that, every time.** A poster judged on its own passes easily: every element is
present, correctly spelled and neatly aligned, and none of that tells you it
reads as a template. Composition errors are invisible in isolation and obvious
in comparison — the gap between an object-in-a-slot layout and a full-bleed one
does not show up in any checklist item, only in the pair.

```bash
python -c "from PIL import Image; a=Image.open('ref.jpg'); b=Image.open('out.jpg'); H=1500; a=a.resize((int(a.width*H/a.height),H)); b=b.resize((int(b.width*H/b.height),H)); c=Image.new('RGB',(a.width+b.width+30,H),'white'); c.paste(a,(0,0)); c.paste(b,(a.width+30,0)); c.save('_compare.png')"
```

Then compare, in this order — structure first, because a structural miss makes
the detail checks moot:

- **Does the talent bleed off the bottom and both sides, with the text over it?**
  See `design-system.md` §2. This is the one that most changes how the poster
  feels, and the one an element-by-element check will never catch.
- How much of the height do the figures occupy, against the reference?
- Does the title span a comparable share of the width?
- Is the bottom block as dense as theirs?

Then the details:

- **Roster alternation is visible.** Names should alternate white/gold,
  separators gold/cyan. If they are all one colour the rule has collapsed —
  crop that band and look, because a uniform roster looks deliberate.
- **The title is readable at thumbnail size.** View at ~15%. If it disappears
  into the background, the scrim is too weak.
- **No cutout eats a letterform.**
- **The margins agree.** Credits, lockup and footer share one inset.
- **Names, date, time, price, phone** all match the brief exactly.

Then run the checklist in `design-system.md` and fix what fails.

### 7 · Variants and delivery

If the lineup has several billed acts, produce solo cuts — this is the
commercial core of the system, not a nicety. Each artist gets a flyer that is
visibly theirs to post to their own following.

Swap only the hero cutout and the variant tag. Everything below the credits
line stays pixel-identical. A lineup change edits the master and **all** cuts
re-export; never patch one.

Name every export with event, date and version:

```
out/sat31jan_v1_ensemble.jpg
out/sat31jan_v1_amanda.jpg
```

Two undated cuts of one event in circulation is how the wrong lineup keeps
getting shared — the reference set has exactly this problem.

Offer a story cut (`--width 1080 --height 1920`) when the poster is for social.
It is **rebuilt, not cropped**: zones 6–9 are too dense to survive a crop, so
the story carries zones 1–5 plus the venue lockup.

Send finished posters with `SendUserFile`. If this is for The Echo, Moseti sends
every finished piece to Telegram — offer it.

## Adverts that are not events

The zone stack is an advert stack. For a product, service or offer, map it:
title becomes the headline, talent becomes the product shot, credits become key
benefits (the alternation still works), venue lockup becomes the brand lockup,
reservation becomes the call to action. Drop the alcohol legal — it is a venue
requirement, not a house style. `design-system.md` §2 has the full mapping.

The tokens, the type tiers and the render loop are unchanged.

## When the client is not The Echo

The Echo's colours, address, socials and legal text are the reference
implementation, not the system. For another client, replace the tokens in
`:root`, the lockup contents and the copy tokens — and keep the structure: the
zone order, the three type tiers, the roster alternation, the safe margin, the
scrim rule.

If the client has existing artwork, look at it before designing. Match their
palette and their display voice rather than importing The Echo's.

## Files

- `references/design-system.md` — tokens, zones, components, copy tokens,
  checklist. **Read before composing.**
- `references/fonts.md` — verified faces per voice, and the silent-fallback
  trap.
- `references/assets.md` — sourcing, background removal, the likeness rule.
- `assets/poster.html` — the template. Renders standalone.
- `assets/fontmap.json` — machine-verified resolving font specs.
- `scripts/render.py` — HTML → exact-pixel image, with verification.
- `scripts/fontcheck.py` — rebuild the font map on a different machine.
