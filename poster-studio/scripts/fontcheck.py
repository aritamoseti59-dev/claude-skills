#!/usr/bin/env python3
"""Probe which font specs actually resolve in Chromium on this machine.

Why this exists: the Windows font enumeration (what PowerShell's
InstalledFontCollection reports) is NOT the same namespace Chromium uses.
Chromium resolves through DirectWrite, where style-linked faces live under a
base typographic family plus weight/stretch rather than as standalone family
names. So "Gill Sans Ultra Bold Condensed" appears installed, is requested in
CSS, and silently renders as Times — with no error anywhere.

A poster that renders in the wrong face looks finished. That is the failure
this script exists to prevent: it measures, rather than trusting the name.

Method: canvas text measurement. Render a test string in `"Candidate", generic`
and compare its width against `generic` alone, for three generics. If the width
is identical in all three, the candidate never resolved.

Usage:
    python fontcheck.py                      # probe the built-in candidate list
    python fontcheck.py --json map.json      # also write results to JSON
    python fontcheck.py --add "Some Font"    # probe extra families
"""

import argparse
import json
import sys

from playwright.sync_api import sync_playwright

# (label, css font-family, css font-weight, css font-stretch)
CANDIDATES = [
    # --- T1 premium: high-contrast serif ---
    ("premium",  "Bodoni MT",                  "normal", "normal"),
    ("premium",  "Bodoni MT",                  "bold",   "normal"),
    ("premium",  "Bodoni MT Black",            "normal", "normal"),
    ("premium",  "Bodoni MT Condensed",        "normal", "normal"),
    ("premium",  "Bodoni MT",                  "normal", "condensed"),
    ("premium",  "Baskerville Old Face",       "normal", "normal"),
    ("premium",  "Didot",                      "normal", "normal"),
    ("premium",  "Playfair Display",           "normal", "normal"),

    # --- T1 hype: heavy condensed sans ---
    ("hype",     "Haettenschweiler",           "normal", "normal"),
    ("hype",     "Impact",                     "normal", "normal"),
    ("hype",     "Bernard MT Condensed",       "normal", "normal"),
    ("hype",     "Arial Narrow",               "bold",   "normal"),
    ("hype",     "Franklin Gothic Heavy",      "normal", "normal"),
    ("hype",     "Franklin Gothic Demi Cond",  "normal", "normal"),
    ("hype",     "Gill Sans MT",               "bold",   "condensed"),
    ("hype",     "Gill Sans Ultra Bold Condensed", "normal", "normal"),
    ("hype",     "Gill Sans Ultra Bold",       "normal", "normal"),
    ("hype",     "Bodoni MT Poster Compressed", "normal", "normal"),
    ("hype",     "Tw Cen MT Condensed Extra Bold", "normal", "normal"),
    ("hype",     "Tw Cen MT Condensed",        "bold",   "normal"),
    ("hype",     "Rockwell Condensed",         "bold",   "normal"),

    # --- T1 funk: retro bubble / groovy ---
    ("funk",     "Cooper Black",               "normal", "normal"),
    ("funk",     "Bauhaus 93",                 "normal", "normal"),
    ("funk",     "Broadway",                   "normal", "normal"),
    ("funk",     "Showcard Gothic",            "normal", "normal"),

    # --- T1 blunt: geometric heavy sans ---
    ("blunt",    "Berlin Sans FB Demi",        "normal", "normal"),
    ("blunt",    "Berlin Sans FB",             "bold",   "normal"),
    ("blunt",    "Eras Bold ITC",              "normal", "normal"),
    ("blunt",    "Britannic Bold",             "normal", "normal"),
    ("blunt",    "Franklin Gothic Heavy",      "normal", "normal"),

    # --- T1 tech: cut / stencil / DIN ---
    ("tech",     "Bahnschrift",                "600",    "condensed"),
    ("tech",     "Bahnschrift",                "bold",   "condensed"),
    ("tech",     "Bahnschrift Condensed",      "normal", "normal"),
    ("tech",     "Bahnschrift SemiBold Condensed", "normal", "normal"),
    ("tech",     "Agency FB",                  "bold",   "normal"),

    # --- T2 script connector ---
    ("script",   "Brush Script MT",            "normal", "normal"),
    ("script",   "Freestyle Script",           "normal", "normal"),
    ("script",   "Segoe Script",               "bold",   "normal"),
    ("script",   "Palace Script MT",           "normal", "normal"),
    ("script",   "French Script MT",           "normal", "normal"),
    ("script",   "Edwardian Script ITC",       "normal", "normal"),
    ("script",   "Monotype Corsiva",           "normal", "normal"),
    ("script",   "Pristina",                   "normal", "normal"),
    ("script",   "Mistral",                    "normal", "normal"),
    ("script",   "Kunstler Script",            "normal", "normal"),
    ("script",   "Vladimir Script",            "normal", "normal"),
    ("script",   "Lucida Handwriting",         "normal", "normal"),

    # --- T3 utility: locked, all-caps bold grotesque ---
    ("utility",  "Franklin Gothic Demi",       "normal", "normal"),
    ("utility",  "Franklin Gothic Heavy",      "normal", "normal"),
    ("utility",  "Franklin Gothic Medium",     "bold",   "normal"),
    ("utility",  "Arial",                      "bold",   "normal"),
    ("utility",  "Arial Black",                "normal", "normal"),
    ("utility",  "Segoe UI",                   "bold",   "normal"),
    ("utility",  "Segoe UI Black",             "normal", "normal"),
    ("utility",  "Tahoma",                     "bold",   "normal"),
    ("utility",  "Verdana",                    "bold",   "normal"),
]

PROBE_JS = """(specs) => {
  const ctx = document.createElement('canvas').getContext('2d');
  const test = 'MMMMWWWWmmmmlli1234ABCDEFGHIJ';
  const generics = ['monospace', 'serif', 'sans-serif'];
  return specs.map(s => {
    let resolved = false, widths = [];
    for (const g of generics) {
      ctx.font = `${s.weight} ${s.stretch !== 'normal' ? '' : ''}72px ${g}`;
      const base = ctx.measureText(test).width;
      ctx.font = `${s.weight} 72px "${s.family}", ${g}`;
      const got = ctx.measureText(test).width;
      widths.push(Math.round(got));
      if (Math.abs(got - base) > 0.5) resolved = true;
    }
    return { ...s, resolved, widths };
  });
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="write the resolved font map here")
    ap.add_argument("--add", nargs="*", default=[],
                    help="extra family names to probe")
    args = ap.parse_args()

    specs = [{"role": r, "family": f, "weight": w, "stretch": s}
             for r, f, w, s in CANDIDATES]
    specs += [{"role": "extra", "family": f, "weight": "normal",
               "stretch": "normal"} for f in args.add]

    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page()
        page.goto("about:blank")
        results = page.evaluate(PROBE_JS, specs)
        b.close()

    by_role: dict[str, list] = {}
    for r in results:
        by_role.setdefault(r["role"], []).append(r)

    ok_total = 0
    for role, items in by_role.items():
        print(f"\n=== {role.upper()} ===")
        for i in items:
            mark = "OK  " if i["resolved"] else "FAIL"
            wt = "" if i["weight"] == "normal" else f" / {i['weight']}"
            st = "" if i["stretch"] == "normal" else f" / {i['stretch']}"
            print(f"  [{mark}] {i['family']}{wt}{st}")
            ok_total += i["resolved"]

    print(f"\n{ok_total}/{len(results)} specs resolved.")

    if args.json:
        keep = {}
        for role, items in by_role.items():
            keep[role] = [
                {"family": i["family"], "weight": i["weight"],
                 "stretch": i["stretch"]}
                for i in items if i["resolved"]
            ]
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(keep, fh, indent=2)
        print(f"Wrote {args.json}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
