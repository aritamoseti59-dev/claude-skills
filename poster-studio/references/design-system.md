# The poster system

Derived from 15 posters produced Jan–Jun 2026 for The Echo Lounge (Kisii) and
four out-of-town venues. This is a record of a system that already works, not an
invention. The Echo is the reference implementation; the system generalises.

---

## 1 · Format

Canvas is **4:5 portrait**, `1600 × 2000` master. Safe margin **6% of width** on
all four edges — nothing in zones 6–9 crosses it. That single measurement fixes
the margin drift that otherwise creeps in between the credits block, the venue
lockup and the footer.

**Story cut** (`1080 × 1920`) is *rebuilt, not cropped*. Zones 6–9 are too dense
to survive a crop; the story carries zones 1–5 plus the venue lockup only.

---

## 2 · The zone stack

Every poster uses the same vertical order. The order is the system. Zones may be
omitted; they may not be resequenced.

| # | Zone | Content |
|---|---|---|
| 1 | Date chip | Day, date, month, **year** |
| 2 | Presenter line | Tracked micro-caps |
| 3 | Title block | Display — largest element on the page |
| 4 | Talent | Cutout photography, **full bleed** — see below |
| 5 | Credits | Script connector + roster line |
| 6 | Venue lockup | Mark │ name │ address |
| 7 | Legal | Fixed string, §7 |
| 8 | Reservation | Hairline rule; doors, price, phone |
| 9 | Social footer | House events only |

Zones 3 and 4 **interleave** — the title sits behind or beside the cutouts rather
than stacked above them.

### The talent is full bleed. This is the single most important rule here.

Get this wrong and the poster is recognisably not theirs, however correct
everything else is.

The talent runs **past both side edges and off the bottom of the canvas**, and
zones 5–9 are laid *on top of it*. The reference posters are photographs with
type over them. The failure mode — and it looks fine until you set the two side
by side — is a photo sitting in a slot in the middle with a dead panel beneath
it holding the text. That reads as a template. Theirs does not.

Concretely, in the reference set:

- Figures occupy roughly **70% of the height**, from just under the title to the
  bottom edge. Not 40–55%, and never floating clear of the bottom.
- The outer subjects are **cut by the left and right edges**. There is no side
  margin around the group.
- Heads begin **at the title's baseline and overlap it** — the title wins on
  z-order, the hair passes behind it.
- The credits, the venue lockup, the legal line and the socials all sit **over
  the bodies**, legible because of a gradient, not because of a black panel.

That needs a **second scrim above the talent layer**, not just the one behind
it. Behind-talent scrim seats the title; above-talent scrim darkens the lower
body so the text block reads. Roughly: transparent to 55%, 0.3 at 68%, 0.6 at
78%, 0.9 at 85%, solid by 92%.

Never fade the bottom of the cutout to hide its crop edge. Scale it so the crop
edge falls **below the canvas** instead — a faded-out body is the slot look
again.

### Adapting to non-event adverts

The stack is an advert stack, not just an event stack. For a product or service:

| Zone | Event | Generic advert |
|---|---|---|
| 1 | Date | Offer window, or omit |
| 2 | Presenter | Brand line |
| 3 | Title | Headline / the offer |
| 4 | Talent | Product shot or subject |
| 5 | Credits | Key benefits, same alternation |
| 6 | Venue lockup | Brand lockup |
| 8 | Reservation | Call to action + contact |

---

## 3 · Composition variants

Pick one per poster. Do not blend.

- **A — Split.** Title left column, talent right, roughly 45/55. For a single
  dominant hero.
- **B — Stacked.** Full-width centred title in the top third, talent centred
  below. **House default.**
- **C — Centred.** Title holds the centre mass, talent flanks. Reads at smaller
  sizes — best for shares rather than printed flyers.

---

## 4 · Type: three tiers

**T1 display — varies.** One voice per poster: premium, hype, funk, blunt, tech.
See `fonts.md` for the verified face per voice.

**T2 script — fixed role.** Only the soft connector: *Featuring*, *Fridays*,
*Pre Valentine Party*. Never carries information the reader must act on. Minimum
cap height 42 px at master size.

**T3 utility — locked.** All-caps bold sans, one face, everywhere. Roster, venue,
address, legal, reservations, footer.

T3 being locked is why five display faces still read as one studio. If a change
to T3 is ever proposed, it changes all posters or none.

**Tracked micro-caps** are a studio signature — they travel to non-house venues.
Two uses: the presenter line, and the vertical right-edge rail carrying the venue
name bottom-to-top. Tracking `0.35em`, regular weight, 70% opacity.

---

## 5 · Colour

Four roles on a dark ground.

| Token | Value | Use |
|---|---|---|
| Ground | `#0C0C0E` | Base. Never a mid-grey. |
| Primary | `#FFFFFF` | Title, roster, venue name |
| Gold | `#E8B84B` | Second half of title; alternating roster names; address |
| Cyan | `#4FC3F7` | Separators. At most one title half per poster. |
| Red | `#E53935` | **Containers only** — badges, tag boxes, date disc |

Red is a container colour, never a type colour. Every correct use in the
reference set is a filled shape with text knocked out of it. That constraint is
what stops the palette going to three competing accents.

Values are eyeballed from rendered artwork. Sample from a source file and correct
them if you get the chance.

---

## 6 · The roster rule

The strongest mechanic in the system. **Names alternate white/gold; separators
alternate gold/cyan, independently.**

```
ATHING ✕ CHLOE ✕ CYRIL ✕ ELSY
white  gold gold cyan white gold gold
```

It breaks a long unpunctuated list into scannable units with no bullets, commas
or line breaks. It holds seven names on one line and still reads.

- Always begin on white. The first name is the highest-billed.
- Separator colour alternates **independently** of name colour — do not lock them
  in step.
- Maximum seven names per line; then break and restart on white.
- The glyph is `✕` (`&#10005;`), not the letter X, at 80% of name size.

`assets/poster.html` encodes this with `nth-child(4n+…)`. It must not be
"simplified" to `nth-of-type` — names and separators are both spans and
interleave, so nth-of-type makes every name odd and every separator even, and the
alternation silently collapses to one colour each while still looking deliberate.

---

## 7 · Copy tokens

Paste these. Do not retype them — two spelling errors propagated across roughly
eight reference posters by being retyped each time.

**Legal — the only approved version:**

```
EXCESSIVE ALCOHOL CONSUMPTION IS HARMFUL TO YOUR HEALTH. DO NOT DRINK AND DRIVE.
ALCOHOL IS NOT FOR SALE TO PERSONS UNDER THE AGE OF 18 YEARS. DO NOT FORWARD THIS TO PERSONS UNDER THE AGE OF 18 YEARS.
```

*(The errors to watch for: `YEQRS` for YEARS, `FOWARD` for FORWARD.)*

Drop the alcohol legal entirely for non-alcohol adverts — it is a venue
requirement, not a house style.

**Presenter line:** `THE ECHO LOUNGE PRESENTS` — with the definite article, matching
the venue name everywhere else.

**Address:** `MKO PLAZA, DARAJA MBILI, KISII`

**Social footer:** Facebook `@theechokenya` · TikTok `@theecho` · Instagram
`@theechokenya` · Web `www.primemoseti.co.ke`. The web line takes a **globe**
icon, not an envelope. Handles cannot contain spaces.

---

## 8 · Components

**Venue lockup** — mark, vertical rule, venue name in T3 black, address beneath
in tracked caps. The most rigid element in the system. It is **extensible by
adding a cell to the right** using the same divider rule (the RNB Brunch adds
`│ DRESS CODE / A TOUCH OF DENIM`). Any other addition to the lockup is a defect.

**Date chip** — standard is a white rounded rectangle, black T3 caps,
`SAT 31ST JAN, 2026`. Specials alternate to a red disc, white caps, two lines.
The wrapped-ring treatment is retired.

**Star divider** — `* * * * * * * * *`, tracking `0.5em`, primary at 60%. Sits
between credits and venue lockup.

**Reservation rule** — hairline with content centred in the break. Carries doors,
price and phone.

**Variant tag** — script *Featuring* above a dark box; the name inside splits
white + gold across its two words (`DJ` + `NKID`). Sits in the lower third of the
talent zone, on the side with more negative space.

---

## 9 · Image treatment

- Cutout, background removed, separated from ground by drop shadow or rim glow —
  never a hard unshadowed edge.
- Warm grade: orange push in skin, cool shadows. Applied consistently across all
  subjects in one poster, even when the sources differ.
- Heads land in the **upper-middle third**. Bodies crop at the credits line,
  never mid-face and never at a joint.
- Groups arrange on a staggered diagonal or a pyramid.

**Hierarchy through saturation.** Where a lineup has two tiers, the secondary
tier runs greyscale and the featured tier full colour. Used once in the reference
set and it is the most sophisticated move in the work — promote it to a rule: any
poster with a headline act plus a support roster uses it. (`.tier-2` in the
template.)

**Background is the event variable; foreground structure is the constant.** House
nights use the retro TV-and-radio wall — the strongest brand-to-motif link
available, since it literally depicts an echo. Specials break it deliberately.

**Scrim.** Any background sitting behind T1 requires a scrim — minimum **55%
opacity at the title's centre**. Without it the display face disappears into busy
imagery. This is the most common failure in the reference set: one title is
entirely unreadable and another has letterforms eaten by a cutout.

---

## 10 · Master and variants

A master carries the ensemble hero. Each solo variant swaps the hero cutout, adds
the variant tag, and **touches nothing below the credits line**. Zones 5–9 stay
pixel-identical across cuts.

This exists so each artist has a flyer that is visibly *theirs* to post to their
own following — distribution multiplied by the size of the lineup, at the cost of
one background swap. It is the commercial core of the whole output.

- Only zone 4 and the variant tag may change between cuts.
- A lineup change edits the master and **all** variants re-export. Never patch
  one cut.
- Every export carries a version in the filename:
  `sat31jan_v2_amanda.jpg`. Two undated cuts of one event in circulation is how
  the wrong lineup keeps getting shared.

---

## 11 · Known defects in the reference set

Kept as a record of what this spec exists to prevent.

| Severity | Defect |
|---|---|
| High | Legal string forked into two texts; one carries `YEQRS` and `FOWARD`, propagated to ~8 posters |
| High | Ungoverned title contrast — one title unreadable, one partly eaten by a cutout |
| High | Unversioned duplicate cuts of one event with different rosters |
| Medium | Zone order violated once (venue/legal/reservation above the title) |
| Medium | Date chip forked three ways |
| Medium | Margin drift between credits, lockup and footer |
| Medium | Script degradation below minimum cap height |
| Medium | `HOST BY` for HOSTED BY; `MILLENIALS`; wordmark rendering as `THE ECH0` with a zero; envelope icon for a web address |
| — | **No poster carries a start time.** |

That last line is why doors is a mandatory field in this skill.

Price is *not* the same gap. Only the Rirongo Show poster carries prices, and
that is correct: it is the only ticketed show in the set. Regular club nights in
this market do not carry a gate price on the flyer. Require price for ticketed
shows — with tiers and a till number — and leave it off weeklies.
