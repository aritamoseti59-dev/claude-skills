#!/usr/bin/env python3
"""Probe which font specs actually resolve in Chromium on this machine.

Why this exists: the OS font enumeration (PowerShell's InstalledFontCollection
on Windows, Font Book / `system_profiler SPFontsDataType` on macOS) is NOT the
same namespace Chromium uses. Chromium resolves through the platform text stack
-- DirectWrite on Windows, CoreText on macOS -- where style-linked faces live
under a base typographic family plus weight/stretch rather than as standalone
family names. So "Gill Sans Ultra Bold Condensed" appears installed, is requested in
CSS, and silently renders as Times — with no error anywhere.

A poster that renders in the wrong face looks finished. That is the failure
this script exists to prevent: it measures, rather than trusting the name.

Method: canvas text measurement. Render a test string in `"Candidate", generic`
and compare its width against `generic` alone, for three generics. If the width
is identical in all three, the candidate never resolved.

Usage:
    python3 fontcheck.py                      # probe the built-in candidate list
    python3 fontcheck.py --json map.json      # also write results to JSON
    python3 fontcheck.py --add "Some Font"    # probe extra families
"""

import argparse
import json
import sys

from playwright.sync_api import sync_playwright

# (label, css font-family, css font-weight, css font-stretch)
#
# Font availability is per-machine, so the candidate list is per-platform.
# Probing a Windows list on macOS just prints 60 FAILs -- it does not tell
# you what to use instead.

CANDIDATES_WIN32 = [
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

CANDIDATES_DARWIN = [
    # --- T1 premium: high-contrast serif ---
    ("premium",  "Didot",                      "normal", "normal"),
    ("premium",  "Didot",                      "bold",   "normal"),
    ("premium",  "Bodoni 72",                  "normal", "normal"),
    ("premium",  "Bodoni 72",                  "bold",   "normal"),
    ("premium",  "Bodoni 72 Oldstyle",         "normal", "normal"),
    ("premium",  "Bodoni 72 Smallcaps",        "normal", "normal"),
    ("premium",  "Baskerville",                "normal", "normal"),
    ("premium",  "Baskerville",                "bold",   "normal"),
    ("premium",  "Hoefler Text",               "normal", "normal"),
    ("premium",  "Hoefler Text",               "bold",   "normal"),
    ("premium",  "Georgia",                    "bold",   "normal"),
    ("premium",  "Palatino",                   "bold",   "normal"),
    ("premium",  "Charter",                    "bold",   "normal"),

    # --- T1 hype: heavy condensed sans ---
    ("hype",     "Impact",                     "normal", "normal"),
    ("hype",     "Arial Narrow",               "bold",   "normal"),
    ("hype",     "Avenir Next Condensed",      "bold",   "normal"),
    ("hype",     "Avenir Next Condensed",      "800",    "normal"),
    ("hype",     "DIN Condensed",              "bold",   "normal"),
    ("hype",     "Helvetica Neue",             "bold",   "condensed"),
    ("hype",     "Futura",                     "normal", "condensed"),
    ("hype",     "Futura",                     "bold",   "condensed"),
    ("hype",     "Phosphate",                  "normal", "normal"),

    # --- T1 funk: retro / hand / display ---
    ("funk",     "SignPainter",                "normal", "normal"),
    ("funk",     "Marker Felt",                "bold",   "normal"),
    ("funk",     "Chalkduster",                "normal", "normal"),
    ("funk",     "Bradley Hand",               "bold",   "normal"),
    ("funk",     "Noteworthy",                 "bold",   "normal"),
    ("funk",     "Trattatello",                "normal", "normal"),
    ("funk",     "Luminari",                   "normal", "normal"),

    # --- T1 blunt: geometric heavy sans ---
    ("blunt",    "Futura",                     "bold",   "normal"),
    ("blunt",    "Avenir Next",                "800",    "normal"),
    ("blunt",    "Avenir Next",                "bold",   "normal"),
    ("blunt",    "Arial Black",                "normal", "normal"),
    ("blunt",    "Gill Sans",                  "bold",   "normal"),
    ("blunt",    "Optima",                     "bold",   "normal"),
    ("blunt",    "Helvetica Neue",             "bold",   "normal"),

    # --- T1 tech: cut / stencil / DIN ---
    ("tech",     "DIN Alternate",              "normal", "normal"),
    ("tech",     "DIN Condensed",              "normal", "normal"),
    ("tech",     "Menlo",                      "bold",   "normal"),
    ("tech",     "Courier New",                "bold",   "normal"),
    ("tech",     "Silom",                      "normal", "normal"),
    ("tech",     "Krungthep",                  "normal", "normal"),

    # --- T2 script connector ---
    ("script",   "Snell Roundhand",            "normal", "normal"),
    ("script",   "Snell Roundhand",            "bold",   "normal"),
    ("script",   "Zapfino",                    "normal", "normal"),
    ("script",   "Apple Chancery",             "normal", "normal"),
    ("script",   "Savoye LET",                 "normal", "normal"),
    ("script",   "Brush Script MT",            "normal", "normal"),
    ("script",   "Bradley Hand",               "normal", "normal"),

    # --- T3 utility: locked, all-caps bold grotesque ---
    ("utility",  "Helvetica Neue",             "bold",   "normal"),
    ("utility",  "Helvetica",                  "bold",   "normal"),
    ("utility",  "Arial",                      "bold",   "normal"),
    ("utility",  "Avenir Next",                "600",    "normal"),
    ("utility",  "Verdana",                    "bold",   "normal"),
    ("utility",  "Tahoma",                     "bold",   "normal"),
    ("utility",  "Trebuchet MS",               "bold",   "normal"),

    # --- controls: prove the probe itself is working ---
    # A present face must resolve; a nonsense name must not. If either
    # control misbehaves, every other row is untrustworthy.
    ("control",  "Helvetica",                  "normal", "normal"),
    ("control",  "ZZZZNoSuchFontZZZZ",         "normal", "normal"),
]

CANDIDATES_BY_PLATFORM = {
    "darwin": CANDIDATES_DARWIN,
    "win32":  CANDIDATES_WIN32,
}

PROBE_JS = """(specs) => {
  const ctx = document.createElement('canvas').getContext('2d');
  const test = 'MMMMWWWWmmmmlli1234ABCDEFGHIJ';
  const generics = ['monospace', 'serif', 'sans-serif'];
  return specs.map(s => {
    let resolved = false, applied = true, widths = [];
    // font-stretch must actually be emitted into the CSS font shorthand.
    // A previous version had `s.stretch !== 'normal' ? '' : ''` -- both
    // branches empty -- so stretch was silently dropped and every
    // condensed spec was measured as if it were normal width.
    const sp = s.stretch === 'normal' ? '' : s.stretch + ' ';
    for (const g of generics) {
      const baseFont = `${s.weight} ${sp}72px ${g}`;
      ctx.font = baseFont;
      // If the shorthand is invalid, ctx.font silently keeps its old value
      // and every measurement below is against the wrong face.
      if (ctx.font.indexOf(g) === -1) applied = false;
      const base = ctx.measureText(test).width;
      ctx.font = `${s.weight} ${sp}72px "${s.family}", ${g}`;
      const got = ctx.measureText(test).width;
      widths.push(Math.round(got * 10) / 10);
      if (Math.abs(got - base) > 0.5) resolved = true;
    }
    return { ...s, resolved, applied, widths };
  });
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="write the resolved font map here")
    ap.add_argument("--add", nargs="*", default=[],
                    help="extra family names to probe")
    ap.add_argument("--platform", choices=sorted(CANDIDATES_BY_PLATFORM),
                    default=None,
                    help="candidate list to probe (default: this platform)")
    args = ap.parse_args()

    plat = args.platform or sys.platform
    if plat not in CANDIDATES_BY_PLATFORM:
        print(f"No candidate list for platform {plat!r}. "
              f"Known: {', '.join(sorted(CANDIDATES_BY_PLATFORM))}.", file=sys.stderr)
        return 1
    candidates = CANDIDATES_BY_PLATFORM[plat]
    print(f"Probing the {plat} candidate list ({len(candidates)} specs).")

    specs = [{"role": r, "family": f, "weight": w, "stretch": s}
             for r, f, w, s in candidates]
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
            warn = "" if i.get("applied", True) else "   <-- CSS font shorthand REJECTED"
            print(f"  [{mark}] {i['family']}{wt}{st}{warn}")
            ok_total += i["resolved"]

    # --- Validate the instrument before trusting any row above. -----------
    ctrl = {i["family"]: i for i in results if i["role"] == "control"}
    present = ctrl.get("Helvetica")
    absent = ctrl.get("ZZZZNoSuchFontZZZZ")
    if present is not None and absent is not None:
        if not present["resolved"] or absent["resolved"]:
            print("\nCONTROL FAILURE: a known-present face did not resolve, or a "
                  "nonsense name did. The probe is not measuring what it claims "
                  "-- discard these results.", file=sys.stderr)
            return 1
        print("\nControls passed: present face resolved, nonsense name did not.")

    # --- A spec that measures identically to a sibling is not a distinct
    # --- face. Requesting it renders the sibling, silently.
    seen: dict[tuple, dict] = {}
    for i in results:
        if i["resolved"] and i["role"] != "control":
            # Dedupe by the spec itself first: the same (family, weight,
            # stretch) legitimately appears under more than one role, and
            # that is not a collision with itself.
            bucket = seen.setdefault((i["family"], tuple(i["widths"])), {})
            bucket[(i["weight"], i["stretch"])] = i
    collisions = {k: list(v.values()) for k, v in seen.items() if len(v) > 1}
    if collisions:
        print("\n=== NOT DISTINCT FACES (identical advance metrics) ===")
        print("  Requesting these renders the same face as its sibling. Do not")
        print("  list one under a role that depends on the axis it ignores.")
        for (fam, _), items in sorted(collisions.items()):
            variants = ", ".join(
                f"{i['weight']}/{i['stretch']}" for i in items)
            print(f"  {fam}: {variants}")

    print(f"\n{ok_total}/{len(results)} specs resolved.")

    if args.json:
        keep = {}
        for role, items in by_role.items():
            if role == "control":
                continue
            keep[role] = [
                {"family": i["family"], "weight": i["weight"],
                 "stretch": i["stretch"], "widths": i["widths"]}
                for i in items if i["resolved"]
            ]
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"platform": plat, "roles": keep}, fh, indent=2)
        print(f"Wrote {args.json}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
