# Fonts

## The trap

The system font list and the browser's font namespace are **not the same thing**.
A face can appear in the OS font enumeration, be requested by that exact name in
CSS, and silently render as Times. Chromium resolves through the platform text
stack — DirectWrite on Windows, **CoreText on macOS** — where style-linked faces
live under a base typographic family plus weight/stretch rather than as
standalone family names. The trap is identical on both; only the resolver
differs.

`document.fonts.check()` cannot detect this. It answers *"can this text be
painted"*, which is true whenever any fallback exists — so a poster rendering
entirely in Times reports zero missing fonts.

A poster in the wrong typeface still looks like a finished poster. That is why
this is verified by measurement rather than trusted by name.

`scripts/render.py` runs the measurement check on every render and **exits 2**
if any face fell back. Treat exit 2 as a failed render, not a warning.

## Verified map — macOS (this machine)

Measured 2026-08-20 on macOS 26.2, Apple Silicon, by canvas advance-width
comparison in Chromium. 61 of 65 probed specs resolved. The two controls
behaved correctly — a known-present face resolved, a nonsense family name did
not — so the instrument was working when these rows were taken.

Use this map on this machine. The Windows map further down is the record for
the other machine and **will render entirely in Times here**.

### T1 display — varies per event, one voice per poster

| Voice | Use it for | CSS |
|---|---|---|
| **premium** | Upmarket weeklies, brand nights | `font-family:"Didot"` |
| | heavier alternative | `font-family:"Didot"; font-weight:700` |
| | tighter alternative | `font-family:"Bodoni 72"` |
| | small-caps alternative | `font-family:"Bodoni 72 Smallcaps"` |
| | softer alternative | `font-family:"Baskerville"; font-weight:700` |
| | most contrast | `font-family:"Hoefler Text"; font-weight:700` |
| **hype** | Headline acts, tours, big-name shows | `font-family:"Impact"` |
| | narrowest | `font-family:"DIN Condensed"; font-weight:700` |
| | geometric alternative | `font-family:"Futura"; font-weight:700; font-stretch:condensed` |
| | grotesque alternative | `font-family:"Helvetica Neue"; font-weight:700; font-stretch:condensed` |
| | humanist alternative | `font-family:"Avenir Next Condensed"; font-weight:800` |
| | inline/deco alternative | `font-family:"Phosphate"` |
| | lighter alternative | `font-family:"Arial Narrow"; font-weight:700` |
| **funk** | Retro, throwback, old-skool, party | `font-family:"SignPainter"` |
| | brush alternative | `font-family:"Marker Felt"; font-weight:700` |
| | chalk alternative | `font-family:"Chalkduster"` |
| | blackletter-ish alternative | `font-family:"Trattatello"` |
| | roman-display alternative | `font-family:"Luminari"` |
| **blunt** | Plain, loud, no styling | `font-family:"Futura"; font-weight:700` |
| | heaviest | `font-family:"Arial Black"` |
| | humanist alternative | `font-family:"Avenir Next"; font-weight:800` |
| | grotesque alternative | `font-family:"Helvetica Neue"; font-weight:700` |
| | calligraphic alternative | `font-family:"Optima"; font-weight:700` |
| **tech** | Industrial, minimal, techno | `font-family:"DIN Alternate"` |
| | condensed alternative | `font-family:"DIN Condensed"` |
| | monospace alternative | `font-family:"Menlo"; font-weight:700` |
| | squared alternative | `font-family:"Silom"` |

**funk is the weak role on macOS.** There is no stock equivalent of Cooper
Black, Bauhaus 93 or Showcard Gothic — the groovy/bubble register simply is
not in the system library. The entries above are the nearest available
registers (hand-painted, brush, chalk), not equivalents. For a genuine retro
poster, install a display face and re-probe rather than accepting the nearest
miss.

### T2 script — connector only

| Use | CSS |
|---|---|
| default connector | `font-family:"Snell Roundhand"` |
| heavier | `font-family:"Snell Roundhand"; font-weight:700` |
| most ornate | `font-family:"Zapfino"` |
| calligraphic | `font-family:"Apple Chancery"` |
| tighter | `font-family:"Savoye LET"` |
| brush | `font-family:"Brush Script MT"` |

`Zapfino` measures ~1.7x the advance width of every other script face. It will
overrun a lockup sized for the others — set it and re-measure, never swap it in
as a drop-in.

### T3 utility — locked, never varies

| Use | CSS |
|---|---|
| default | `font-family:"Helvetica Neue"; font-weight:700` |
| alternative | `font-family:"Avenir Next"; font-weight:600` |
| widest | `font-family:"Verdana"; font-weight:700` |
| narrower | `font-family:"Trebuchet MS"; font-weight:700` |

### Resolves, but not a distinct face — do not rely on the axis

These strings resolve, so `render.py` exits 0 and the poster looks finished.
But the weight or stretch axis produced **no measurable change**: you get the
sibling face, silently.

| Spec | Renders as |
|---|---|
| `Gill Sans` + `font-stretch:condensed` | plain `Gill Sans` bold — no condensed cut exists |
| `Futura` + `font-weight:900` | `Futura` bold — no black cut |
| `Helvetica Neue` + `font-weight:900` | `Helvetica Neue` bold — no black cut |
| `DIN Alternate` + `font-weight:700` | `DIN Alternate` regular — no bold cut |
| `DIN Condensed` + `font-weight:700` | `DIN Condensed` regular — no bold cut |
| `Bradley Hand` + `font-weight:700` | `Bradley Hand` regular — no bold cut |

`Arial` and `Helvetica` measure identically at every weight — Arial was drawn
metric-compatible with Helvetica. Both resolve to real, visually different
faces; the probe simply cannot separate them by width. Pick by eye, not by
this map.

### Does not resolve on macOS

`Playfair Display` · `Haettenschweiler` · `Cooper Black` — and every other
face in the Windows map below.

## Verified map — Windows (the other machine)

Measured on the Windows machine, 2026-08-17. Each entry below resolved there;
entries under "Does not resolve" enumerate as installed but fall back.
**None of these resolve on macOS** (checked 2026-08-20).

### T1 display — varies per event, one voice per poster

| Voice | Use it for | CSS |
|---|---|---|
| **premium** | Upmarket weeklies, brand nights | `font-family:"Bodoni MT Condensed"` |
| | heavier alternative | `font-family:"Bodoni MT Black"` |
| | softer alternative | `font-family:"Baskerville Old Face"` |
| **hype** | Headline acts, tours, big-name shows | `font-family:"Haettenschweiler"` |
| | wider alternative | `font-family:"Impact"` |
| | serif-flavoured alternative | `font-family:"Bernard MT Condensed"` |
| | lighter alternative | `font-family:"Arial Narrow"; font-weight:700` |
| **funk** | Retro, throwback, old-skool, party | `font-family:"Cooper Black"` |
| | geometric alternative | `font-family:"Bauhaus 93"` |
| | deco alternative | `font-family:"Broadway"` |
| | slab alternative | `font-family:"Showcard Gothic"` |
| **blunt** | Direct, loud, no-frills | `font-family:"Berlin Sans FB"; font-weight:700` |
| | heavier alternative | `font-family:"Franklin Gothic Heavy"` |
| **tech** | Late-night, electronic, industrial | `font-family:"Bahnschrift"; font-weight:700; font-stretch:condensed` |
| | narrower alternative | `font-family:"Agency FB"; font-weight:700` |

Also verified: `Gill Sans MT` at `font-weight:700; font-stretch:condensed`,
`Tw Cen MT Condensed` at `font-weight:700`, `Rockwell Condensed` at
`font-weight:700`, `Bodoni MT` at `font-weight:700` or `font-stretch:condensed`.

### T2 script — connector only

All of these resolve. Ranked by closeness to the reference posters' signature:

1. `Freestyle Script` — closest to the house *Featuring*
2. `Brush Script MT` — heavier, better for a bold connector like *Fridays*
3. `Pristina` — lighter, more formal
4. `Palace Script MT` — very fine; needs large sizes
5. `Mistral`, `Segoe Script`/bold, `Monotype Corsiva`, `French Script MT`,
   `Edwardian Script ITC`, `Kunstler Script`, `Vladimir Script`, `Lucida Handwriting`

Keep cap height at or above **42 px at master size**. Below that the script
degrades into an illegible squiggle — this happened on two reference posters,
where *Pre Valentine Party* misreads entirely.

### T3 utility — locked, never varies

```css
font-family: "Segoe UI", Arial, sans-serif;
/* two weights only: 700 for most, 900 for the venue name */
```

Alternatives that resolve if you ever need them: `Arial Black`,
`Segoe UI Black`, `Franklin Gothic Heavy`, `Franklin Gothic Medium`/bold,
`Arial`/bold, `Tahoma`/bold, `Verdana`/bold.

T3 carries the roster, venue, address, legal, reservations and footer. It is the
constant that makes five different display faces still read as one studio, so
changing it changes every poster or none.

### Does not resolve — do not use these strings

`Gill Sans Ultra Bold Condensed` · `Gill Sans Ultra Bold` ·
`Bodoni MT Poster Compressed` · `Tw Cen MT Condensed Extra Bold` ·
`Franklin Gothic Demi Cond` · `Franklin Gothic Demi` · `Berlin Sans FB Demi` ·
`Britannic Bold` · `Eras Bold ITC` · `Bahnschrift SemiBold Condensed` ·
`Didot` · `Playfair Display`

Several of these are reachable another way — `Berlin Sans FB` at weight 700
gives you the Demi cut, `Bahnschrift` at weight 700 + `font-stretch:condensed`
gives you SemiBold Condensed. Reach for the base family plus properties before
concluding a face is unavailable.

## Re-verifying on another machine

The map above is specific to this machine's font install. On any other machine,
rebuild it:

```bash
python3 scripts/fontcheck.py --json assets/fontmap.darwin.json
```

Requires Playwright (`python3 -m pip install playwright && playwright install
chromium`). The script picks the candidate list for the platform it is running
on; override with `--platform darwin|win32`, and add candidates with
`--add "Some Family" "Another Family"`.

It prints OK/FAIL per spec and writes the resolving ones to JSON. Read three
things in its output before trusting the map:

1. **Controls passed.** A known-present face must resolve and a nonsense name
   must not. If that line is missing or failed, the probe was not measuring
   what it claims and every row is worthless.
2. **CSS font shorthand REJECTED** on any row — the browser refused the font
   string, so `ctx.font` kept its previous value and that row measured the
   wrong face entirely.
3. **NOT DISTINCT FACES** — those specs resolve but ignore the weight or
   stretch you asked for. Never list one under a role that depends on the
   axis it ignores.
