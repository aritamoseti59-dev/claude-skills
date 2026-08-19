# Sourcing images

Three routes in, in order of preference. Work down the list — the further down
you go, the more you are inventing rather than depicting.

---

## 1 · Supplied photographs — always first

If the client sent photos, use them. Save into `<project>/assets/src/`, keep the
originals untouched, and work on copies.

**A named real person must come from a supplied photograph.** If the poster says
`FEATURING DJ NKID`, the face on it has to be DJ Nkid. Generating a plausible
face for a named performer fabricates a real person's likeness on promotional
material that will circulate publicly under their name — that is not a style
choice, and no amount of "it looks close enough" makes it acceptable.

When a named act has no usable photo, do not paper over it. Say so and offer the
alternatives: a type-led cut with no portrait (the system supports this — zones
3 and 5 carry the poster on their own), the venue's logo in the hero slot, or
hold the poster until a photo arrives.

Generation is fine for: backgrounds, textures, atmosphere, crowd scenes with no
identifiable individual, and anonymous stock-style figures where no name is
attached.

---

## 1b · Logos — a different job from cutouts

**Do not run a background remover on a logo lockup.** Matting models are
trained to find a subject, and they read a logo's wordmark as background. Tested
twice on real client logos: both times the model returned a clean mark and
silently discarded the company name underneath it. The output looks like a
successful cutout, which is what makes it dangerous.

What works instead, in order:

1. **Ask for the original.** A vector or transparent PNG from the client beats
   every extraction. Always request it — a logo lifted from a JPEG of a poster
   is a reconstruction, and the client usually has the real file.
2. **Colour-key it**, when the logo sits on a contrasting ground. Key on
   *brightness and saturation together*, not brightness alone: a white logo is
   bright **and** desaturated, so `alpha = f(V) · g(1−S)` keeps the mark while
   rejecting the coloured light streaks and lens flare that a pure luminance
   threshold lets through. For a gold-on-pastel-sky logo, invert it — key on
   high saturation, since the lettering is saturated and the sky is not.
3. **Split the lockup** when the two halves need different treatment. A matte
   model may nail a complex 3D mark while failing on its wordmark; key the
   wordmark separately and combine the two alpha channels with `max()`. Do this
   at full frame before cropping to bounding box, or the two layers lose
   registration with each other.
4. **Upscale before matting, not after.** Alpha rarely survives an upscaler.
   Higgsfield `upscale_image` on the opaque crop first gives the matte more
   detail to work with and produces a far cleaner edge.
5. **Re-set the type** when a sub-line is too small to recover. Text that is
   6 px tall in the source is gone — no filter brings it back. Extract the mark
   as artwork and set the wordmark in real type. Say that you have done it, so
   the client can supply the original if the match matters.

Beware component filters that discard "thin" blobs to remove streaks: fine
letterforms are also thin, and an aspect-ratio filter will eat a sub-line
before it eats a diagonal light streak.

## 2 · Background removal

The cutout look is the system's foundation. Use Higgsfield `remove_background`
on each **portrait** — see §1b for why logos need a different route — then
composite as a PNG in the `.talent` layer.

```
mcp__f80ce0a6-…__remove_background   # cutout from a supplied photo
mcp__f80ce0a6-…__upscale_image       # if the source is small or soft
```

Check the result before compositing — background removers leave halos on hair
and fail on low-contrast edges. Both are visible at poster scale, and the
reference set has examples of each. If the cutout is rough, an upscale first
usually fixes it.

Never leave a hard unshadowed edge. The template applies a drop shadow; keep it.

---

## 3 · Generated imagery

For backgrounds, textures and anonymous figures. Default to **GPT Image 2** for
anything with graphic structure, **Nano Banana** for photographic figures.

```
mcp__f80ce0a6-…__generate_image
```

Prompt for the *background plate*, not the poster. The typography is composed in
HTML, so asking an image model for a finished poster with text throws away every
guarantee this system provides — exact hex, exact tracking, verbatim legal copy,
correctly spelled names. Image models cannot set a legal disclaimer without
eventually misspelling it, and that disclaimer is a licensing requirement.

Good background prompts describe the plate and leave room for type:

> Wall of stacked vintage CRT televisions and radio receivers glowing amber in a
> dark room, warm bokeh, deep shadows in the upper third, cinematic, no text,
> no people

Include `no text` — generated lettering in the background will fight the real
typography and is usually misspelled.

---

## 4 · Web images

Only with a clear licence, and only for reference or client-supplied material
you are re-hosting on their behalf. Do not pull a stranger's photograph off a
search result onto a commercial poster. If the client wants a specific image
they saw, ask them to supply it.

---

## Working layout

```
<project>/
├── assets/
│   ├── src/        originals, never edited
│   ├── cut/        background-removed PNGs
│   └── bg/         background plates
├── poster.html
└── out/
    ├── sat31jan_v1_ensemble.jpg
    └── sat31jan_v1_amanda.jpg
```

Reference images from the HTML with **relative paths**. The renderer loads the
page from disk, so relative paths resolve, and the project stays portable.

`render.py` fails the render if an image does not load, so a broken path cannot
reach an export as a blank space.
