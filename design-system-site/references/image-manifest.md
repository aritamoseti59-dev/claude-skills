# Image manifest

The point: page generation and image generation are different jobs with different tools and
different latencies. Blocking one on the other wastes both. Emit every image slot as a
placeholder plus a complete generation brief, then fill them in a batch.

Write it to `assets/images/manifest.json` next to where the images will land.

## Format

```json
{
  "images": [
    {
      "id": "image-01",
      "slot": "hero-bg",
      "aspect": "16:9",
      "dimensions": "1920x1080",
      "alt": "Roofing crew installing shingles on a two-storey home at dusk",
      "prompt": "Wide cinematic photo of a roofing crew installing dark charcoal architectural asphalt shingles on a two-storey midwestern home. Warm late-afternoon light, slightly desaturated. Clean roof ridge line, shallow depth of field.",
      "status": "pending"
    },
    {
      "id": "image-02",
      "slot": "service-card-repair",
      "aspect": "3:2",
      "dimensions": "1200x800",
      "alt": "Close-up of a roofer replacing flashing around a chimney",
      "prompt": "Close-up of a roofer's gloved hands replacing damaged flashing around a brick chimney. Warm late-afternoon light, crisp texture, editorial documentary photography, shallow depth of field.",
      "status": "pending"
    }
  ]
}
```

`alt` is filled in now, while the intent is fresh. Written later, from looking at a delivered
image, it describes the picture instead of its purpose — and purpose is what a screen reader
user needs.

## Placeholder rendering

Render each pending slot as a visible box at the correct aspect ratio, labelled with its `id`
and dimensions. Correct aspect ratio matters: a placeholder at the wrong shape means the layout
shifts when real images arrive, and you discover the hero was never going to work at 16:9.

```html
<div class="img-placeholder" style="aspect-ratio: 16/9" data-image-id="image-01">
  image-01 · hero-bg · 16:9 · 1920×1080
</div>
```

Style it as an obvious placeholder — pinstripes, a flat token colour, anything that cannot be
mistaken for a design decision. If a placeholder can be mistaken for finished work, one will
eventually ship.

## Writing the prompts

**Describe the photograph, not the layout.** "Leave space at the bottom for a call to action"
makes the generator render text in the image. Composition notes are fine and useful
("framing leaves darker open space on the left third") — instructions about *page* elements
are not.

Useful things to specify: subject and action, time of day and light quality, mood, lens
character (shallow depth of field, wide), colour treatment. Keep the same light and treatment
across the set or the page will read as a collage.

## Filling the slots

The number binds everything. The user generates, downloads, and names files `image-01.webp`,
`image-02.webp`, matching the `id`. Then:

1. Drop files into `assets/images/`
2. Match by `id` → `slot`, replace the placeholder, set `status` to `done`
3. Carry `alt` from the manifest into the markup
4. Any slot still `pending` keeps its placeholder — visibly, so it doesn't ship unnoticed

If a delivered file's aspect ratio doesn't match the manifest, say so rather than cropping
silently. The layout was built to the declared ratio, and a silent crop is how faces lose
their heads on mobile.

## File size

Generated images are routinely far larger than the web needs. Convert to WebP or AVIF, and
size to roughly twice the largest CSS display width — no more. A 4K hero on a 1200px container
is several megabytes buying nothing.
