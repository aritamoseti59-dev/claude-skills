# Token layer scaffold

The token file is the contract. Everything else in the site reads from it and nothing writes
around it. Keep it in one place — `styles/tokens.css` for plain CSS, the theme block for
Tailwind, `tokens.ts` for CSS-in-JS. One file, one source of truth.

## Naming

Two tiers, and the distinction matters more than the names:

- **Primitive** — the raw value. `--slate-900: #1B2B3A`. Names a colour.
- **Semantic** — the role. `--color-surface: var(--slate-900)`. Names a *job*.

Components reference semantic tokens only. Primitives exist so semantics have something to point
at. This is what lets you re-theme by editing five lines instead of auditing every component:
`--color-danger` can start life as red and become orange without a single component knowing.

## Scaffold

```css
:root {
  /* ---- primitives: colour ---- */
  --brand-900: #1B2B3A;
  --brand-700: #2E4A60;
  --accent-500: #B84C2B;
  --neutral-050: #F2EFE9;
  --neutral-000: #FFFFFF;

  /* ---- semantic: colour ---- */
  --color-bg:            var(--neutral-050);
  --color-surface:       var(--neutral-000);
  --color-text:          var(--brand-900);
  --color-text-muted:    color-mix(in srgb, var(--brand-900) 65%, transparent);
  --color-accent:        var(--accent-500);
  --color-on-accent:     var(--neutral-000);
  --color-border:        color-mix(in srgb, var(--brand-900) 12%, transparent);

  /* semantic status — define these even if unused today.
     They are what stops a seventh red being invented later. */
  --color-success: #2E7D5B;
  --color-warning: #B4830F;
  --color-danger:  #A03427;

  /* ---- type ---- */
  --font-heading: "Instrument Sans", system-ui, sans-serif;
  --font-body:    "Plus Jakarta Sans", system-ui, sans-serif;

  /* one scale, ~1.25 ratio. Add steps, don't add one-offs. */
  --text-xs:   0.79rem;
  --text-sm:   0.889rem;
  --text-base: 1rem;
  --text-lg:   1.125rem;
  --text-xl:   1.406rem;
  --text-2xl:  1.758rem;
  --text-3xl:  2.197rem;
  --text-4xl:  2.747rem;

  --leading-tight: 1.15;
  --leading-body:  1.6;

  /* ---- spacing: one scale, used everywhere ---- */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;
  --space-16: 4rem;
  --space-24: 6rem;

  /* ---- radius / elevation ---- */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --shadow-1: 0 1px 2px rgb(0 0 0 / 0.06);
  --shadow-2: 0 4px 12px rgb(0 0 0 / 0.08);
  --shadow-3: 0 12px 32px rgb(0 0 0 / 0.12);

  /* ---- motion ---- */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --dur-fast: 120ms;
  --dur-base: 220ms;
  --dur-slow: 420ms;
}

/* Dark mode, if the brand has one, redefines SEMANTIC tokens only —
   never primitives, or the ramp stops meaning anything. */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg:      var(--brand-900);
    --color-surface: var(--brand-700);
    --color-text:    var(--neutral-050);
  }
}

/* Respect the OS setting. One block, covers the whole site. */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Component inventory

Build these against the tokens *before* any page exists, and render them all on one page so
they can be seen together. Inconsistency is obvious on a component sheet and invisible when
the parts are scattered across five pages.

Minimum set for a marketing site:

- Button — primary, secondary, and a disabled state
- Link — inline, and standalone with affordance
- Card — the base, plus whatever variants the content actually needs
- Form field — label, input, help text, **and the error state**
- Nav — desktop and mobile, including the open mobile state
- Section header — eyebrow, heading, subheading
- Footer

The error state is the one that gets skipped and the one that gets seen at the worst moment.

## Contrast

Check text against its background as you define semantic tokens, not afterwards. WCAG AA is
4.5:1 for body text and 3:1 for large text. Accent colours chosen for brand feel are the usual
offender — a rust or amber that looks right on a swatch often fails against white, and the fix
is a darker variant of the same hue rather than a different colour.
