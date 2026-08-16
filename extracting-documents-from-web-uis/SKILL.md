---
name: extracting-documents-from-web-uis
description: Guidance for pulling a source document — a tutorial, a build guide, install instructions, a prompt library — out of a web UI (a wiki page, Notion, a docs site) without losing content to invisible truncation, and for correctly relaying anything sourced from it back to the user. Covers treating any extraction with a size cap as lossy by default (collapsed toggles that read as a complete page, evaluation tools that silently truncate long text) via an expand-then-inventory-then-window pass, and covers matching the formatting of a relayed command to where it will actually execute — a slash command placed inside a shell-tagged code fence gets run by the user's shell, not interpreted as chat input. Use this whenever pulling a script, prompt, or setup steps out of a hosted doc/wiki/Notion page with collapsible sections, or whenever relaying a command sourced from a tutorial back to the user for them to run — even if the page looks fully loaded and the command looks like ordinary chat text.
license: MIT
---

# Extracting Documents from Web UIs

When a setup document or tutorial lives in a web UI rather than a plain file,
two independent things can go wrong invisibly — once on the way from the
page into your context, and again on the way from you back out to the user.
A truncated read looks exactly like a complete one, and a command relayed in
the wrong wrapper looks exactly like one in the right wrapper. Both failures
pass every glance-level check and only surface later, as someone else's
problem.

## Step 1: Treat any extraction with a size cap as lossy by default

Web UIs commonly present a document behind interactive chrome — collapsed
sections, "load more" toggles, virtualized lists — and the tools available
to read them commonly have caps of their own. Both failure modes are silent:
the page "reads" complete because the surrounding prose flows normally
around a collapsed placeholder, and a truncated string returned by an
evaluation tool looks like a clean, syntactically plausible prefix.

Treat extracting a document out of a web UI as three explicit phases, not one
call:

1. **Expand.** Enumerate every collapse or toggle control programmatically
   and open all of them, then assert the state actually flipped — don't
   assume a click succeeded just because nothing errored.
2. **Inventory.** Before pulling content, list the extractable blocks with
   their lengths. This tells you how many blocks exist and which ones will
   exceed whatever cap the read tool imposes, before you've spent a call
   finding out the hard way.
3. **Window.** Pull any oversized block in explicitly overlapping slices
   sized under the cap, and verify continuity at the seams rather than
   assuming adjacency — don't trust that slice N+1 picks up exactly where
   slice N left off.

Prefer a DOM-level selector over a screenshot for anything that needs to be
reproduced character-exact — a script that's legible in a screenshot can
still be horizontally clipped in exactly the place that matters.

Real case: a build guide's payload — a multi-kilobyte script, several long
prompts, a skill file — lived inside collapsed toggles on a hosted wiki page.
The page-text tool returned "Loading…" placeholders for every collapsed
block while the surrounding prose read as complete, and a naive text-pull on
the script returned a clean-looking prefix ending in a silent truncation
marker. Concatenating that as-is would have produced a syntactically
plausible, silently incomplete script.

## Step 2: Match how you relay a command to where it will actually run

Once you're relaying an instruction sourced from that document back to the
user — a shell command, a slash command, a config snippet — the destination
is a property of how you format it, not a stylistic choice. Some rendering
layers turn a tagged code block into a button the user can click to execute
it directly in their shell. Choosing that tag is choosing an action on the
user's behalf, whether or not the text inside is actually shell syntax.

A Claude Code slash command is prompt-level input, not a shell command — it
means nothing to PowerShell or bash. Put it in inline code or an untagged
block, never inside a shell-tagged fence. The correctness bar for a
shell-tagged fence is "will this run correctly there," not "does this look
like a command."

Real case: relaying a tutorial's install step, a slash command was written
inside a shell-tagged code fence. The user pressed the fence's Run button,
the shell received the literal slash-command text, and returned a
command-not-found error. The user read that as the install itself failing,
and the actual problem — an unrelated registration step that had never
completed — was diagnosed a full round trip later than it needed to be.

## Closing check

Before treating a read from a web UI as complete, confirm every collapsed
section was actually expanded and every block came back under its cap — a
document that "reads fine" can still be missing exactly the part you need.
And before relaying anything sourced from that document back to the user,
check what a click on it would actually run.
