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

## Verified map

> **⚠ This map was measured on a Windows machine and is not valid on the
> current macOS machine.** Every display face below — Bodoni MT, Bodoni MT
> Condensed, Haettenschweiler, Impact, Cooper Black, Bauhaus 93, Broadway,
> Showcard Gothic, Baskerville Old Face, Bernard MT Condensed, Arial Narrow,
> Didot, Playfair Display — is a Windows/Office font, and **none of them are
> installed here** (checked 2026-08-20). Composing against this map on macOS
> yields a poster set entirely in fallback, which `render.py` catches as exit 2.
> Regenerate before using poster-studio on this machine:
> `python3 scripts/fontcheck.py --json map.json` (requires Playwright), then
> replace the tables below with the result. Keep this Windows map only as the
> record for that machine.

Measured on the Windows machine, 2026-08-17. Each entry below resolved there;
entries under "Does not resolve" enumerate as installed but fall back.

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
python scripts/fontcheck.py --json assets/fontmap.json
```

Add candidates with `--add "Some Family" "Another Family"`. The script prints
OK/FAIL per spec and writes the resolving ones to JSON.
