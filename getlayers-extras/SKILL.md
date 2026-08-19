---
name: getlayers-extras
description: Additions to the getlayers plugin skill, which is third-party and should not be edited locally. Load alongside getlayers whenever building a site, landing page, or pitch mockup for a third party, and whenever visually verifying a page with scroll-triggered or staggered motion. Covers checking for an incumbent site before designing, and why screenshots of animated pages need a settling wait before anything is diagnosed as a bug.
---

# getlayers-extras

`getlayers` ships as a third-party plugin, so editing it locally would be
overwritten on update and would diverge from upstream. These two additions
live here instead. **Load both**; this file is only the delta.

Pairing: supplements the `getlayers` plugin skill. Both items below generalise
beyond getlayers — they apply to any client-pitch or site-building skill, and
to any visual verification of an animated page.

## Before designing what they should have, establish what they already have

Applies to **any "build X for this third party" brief** — a pitch mockup, a
redesign, a landing page for a prospect.

Add this to the pre-build interview, **before template selection**:

**Follow every link in the prospect's profile and check whether a site already
exists.**

A brief framed as "make a mockup to give him visibility" implies no web
presence. That framing is often just the requester's assumption. In the case
that surfaced this, the bio link led to an already-live site the brief had
never mentioned.

An incumbent site changes the work in two ways at once:

- **It changes the deliverable.** The pitch is now a *redesign*, not a
  greenfield build — and a redesign must explicitly name what the new one does
  better. A mockup that ignores the incumbent is a weaker sales argument,
  because you have to beat what exists rather than fill a void.
- **It is the cheapest source of accurate content.** Brand copy, palette,
  nav and service taxonomy, contact details — all already written, all free.
  Capture them as source material rather than inventing substitutes.

The general form: for any brief about a third party, spend one step on what
they already have. The incumbent artefact is simultaneously the competitive
benchmark and the best content source, and its existence often reshapes the
deliverable in a way the requester did not flag.

## On an animated surface, a single screenshot is a sample, not a state

Applies to any page with **scroll-triggered or staggered motion** — which is
most pages getlayers produces.

**Never screenshot immediately after scrolling.** A staggered reveal means a
heading is *legitimately* half-clipped for several hundred milliseconds after
entering the viewport. A frame captured at that instant is indistinguishable
from a genuine clipping defect, and the natural next move — inspecting
`line-height` and `overflow` — yields a plausible-sounding diagnosis for a bug
that does not exist. Real time has been lost "fixing" a descender-clipping
issue that was never visible in the settled state.

The procedure:

1. Scroll.
2. **Wait past the longest reveal duration plus its stagger.** For line
   reveals this is typically **1.5–2.5s**.
3. Capture.

**If something still looks clipped or half-drawn, do not diagnose yet.**
Capture a second frame after a further wait and compare:

- **Two identical frames** → a real defect. Now investigate.
- **Two different frames** → it was still animating. Wait longer.

Before treating what a screenshot shows as a defect, establish that the
surface has settled — otherwise the design's own motion gets debugged as a bug.
