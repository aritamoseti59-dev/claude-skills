#!/usr/bin/env python3
"""Render a poster HTML file to an exact-pixel image.

The poster system depends on typography landing where the spec says it lands,
so the render must be deterministic: a fixed viewport, no scrollbars, fonts
fully loaded before the shutter, images fully decoded before the shutter.

Usage:
    python render.py poster.html out.jpg
    python render.py poster.html out.png --width 1080 --height 1920
    python render.py poster.html out_print.jpg --scale 2

Exit codes:
    0  rendered, dimensions verified
    1  render failed
    2  rendered but a font in the page fell back to a substitute
"""

import argparse
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=2000)
    ap.add_argument("--scale", type=int, default=1,
                    help="device pixel ratio; 2 doubles output resolution")
    ap.add_argument("--quality", type=int, default=92,
                    help="JPEG quality, ignored for PNG")
    ap.add_argument("--timeout", type=int, default=30000)
    args = ap.parse_args()

    src = pathlib.Path(args.html).resolve()
    if not src.exists():
        print(f"ERROR: {src} does not exist", file=sys.stderr)
        return 1

    out = pathlib.Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    is_jpg = out.suffix.lower() in (".jpg", ".jpeg")

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--force-color-profile=srgb",
                                          "--font-render-hinting=none"])
        page = browser.new_page(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale,
        )
        page.goto(src.as_uri(), wait_until="load", timeout=args.timeout)

        # Fonts and images must be settled or the shutter catches a reflow.
        page.wait_for_function("document.fonts.ready.then(() => true)",
                               timeout=args.timeout)
        page.wait_for_function(
            "Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)",
            timeout=args.timeout,
        )
        page.wait_for_timeout(250)

        # A poster that scrolls has overflowed its canvas — the render would
        # silently crop rather than fail, so surface it.
        overflow = page.evaluate(
            "() => ({h: document.documentElement.scrollHeight,"
            " w: document.documentElement.scrollWidth})"
        )

        # Detect silent font substitution.
        #
        # document.fonts.check() is NOT usable here: it answers "can this text
        # be painted", which is true whenever any fallback exists, so a page
        # rendering entirely in Times reports zero problems. Measure instead —
        # paint the same string in `"Candidate", generic` and in `generic`
        # alone; identical widths across every generic means the named face
        # never resolved and the poster is in the wrong typeface.
        font_report = page.evaluate("""() => {
            const wanted = new Map();
            document.querySelectorAll('*').forEach(el => {
                if (!el.textContent || !el.textContent.trim()) return;
                const cs = getComputedStyle(el);
                const first = cs.fontFamily.split(',')[0].trim()
                                .replace(/^['"]|['"]$/g, '');
                if (first) wanted.set(first + '|' + cs.fontWeight,
                                      {family: first, weight: cs.fontWeight});
            });
            const generic = new Set(['serif','sans-serif','monospace','cursive',
                                     'fantasy','system-ui','ui-monospace',
                                     'ui-serif','ui-sans-serif','']);
            const ctx = document.createElement('canvas').getContext('2d');
            const probe = 'MMMMWWWWmmmmlli1234ABCDEFGHIJ';
            const missing = [];
            for (const {family, weight} of wanted.values()) {
                if (generic.has(family.toLowerCase())) continue;
                let resolved = false;
                for (const g of ['monospace','serif','sans-serif']) {
                    ctx.font = `${weight} 72px ${g}`;
                    const base = ctx.measureText(probe).width;
                    ctx.font = `${weight} 72px "${family}", ${g}`;
                    if (Math.abs(ctx.measureText(probe).width - base) > 0.5) {
                        resolved = true; break;
                    }
                }
                if (!resolved) missing.push(`${family} (weight ${weight})`);
            }
            return missing;
        }""")

        page.screenshot(
            path=str(out),
            type="jpeg" if is_jpg else "png",
            **({"quality": args.quality} if is_jpg else {}),
        )
        browser.close()

    expect_w, expect_h = args.width * args.scale, args.height * args.scale
    try:
        from PIL import Image
        with Image.open(out) as im:
            actual = im.size
    except Exception:
        actual = None

    result = {
        "output": str(out),
        "expected": [expect_w, expect_h],
        "actual": list(actual) if actual else None,
        "bytes": out.stat().st_size,
        "overflow": overflow,
        "missing_fonts": font_report,
    }
    print(json.dumps(result, indent=2))

    if actual and actual != (expect_w, expect_h):
        print(f"ERROR: expected {expect_w}x{expect_h}, got {actual[0]}x{actual[1]}",
              file=sys.stderr)
        return 1
    if overflow["h"] > args.height + 1 or overflow["w"] > args.width + 1:
        print(f"WARNING: content overflows canvas "
              f"({overflow['w']}x{overflow['h']} vs {args.width}x{args.height}) "
              f"— the render is cropped", file=sys.stderr)
    if font_report:
        print(f"FONT FALLBACK: {', '.join(font_report)} did not resolve. "
              f"The page rendered in a substitute face.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
