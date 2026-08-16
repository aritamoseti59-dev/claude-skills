---
name: frontend-verification-loop
description: Verification discipline for browser/frontend debugging and browser automation — before trusting what a tool reports about a page, tab, or interactive component, verify the tool's own view of that surface is accurate first. Covers recovering a page the user has open that a browser-automation tool can't see (its tab tracking is narrower than "the browser" as the user experiences it), proving a preview/render surface actually renders before debugging app code as broken, and instrumenting a UI pipeline stage-by-stage instead of guessing and rewriting the last stage repeatedly when interactive state won't visibly update. Use this whenever debugging a blank or wrong-looking page in a preview pane, an interactive component that won't update, or when a browser-automation tool can't find a tab or page the user says is already open — even when the obvious diagnosis seems to be "the code is broken" or "the user is wrong about what's open."
license: MIT
---

# Frontend Verification Loop

Your tools' view of a browser or frontend surface can be narrower, staler, or
flatly wrong compared to what's actually there. A narrow or broken
observation instrument doesn't fail loudly — it produces confident, precise,
entirely false readings, and every measurement taken through it afterward is
worthless no matter how careful the analysis looks. Before diagnosing "the
page doesn't exist," "the app is broken," or "the state is wrong," verify the
instrument you're looking through.

## Step 1: Check the tool's blind spots before asking the user

A browser-automation tool's model of "the browser" is usually narrower than
the user's: it sees the tabs it created or is tracking, not necessarily every
tab the user has open. When a user references a page they already have open
and the tool comes up empty, that's evidence about the tool's visibility, not
evidence the page doesn't exist.

Work a recovery ladder, cheapest first, before involving the user:

1. **Check the tracked scope.** Confirm whether the target is already inside
   the tool's own tracked scope.
2. **Use the app's own recency surface.** If not, use the application's own
   memory of recent activity rather than the browser's. Most authenticated
   apps expose a richer, better-scoped "recent" surface than browser history
   does — a site's own recents list, in-app search history, a
   recently-viewed panel — and it's often reachable even when raw browser
   history isn't (browser-internal history pages are frequently blocked from
   automated navigation entirely).
3. **Confirm the match.** Check the recovered target actually matches what
   the user described before building anything on it. A same-shaped guess is
   not a confirmed one.
4. **Ask last.** Only after those fail, ask the user directly for the URL.

Real case: asked to act on "the page I have open" in a social app, the
automation tool's own tracked tabs were empty and browser history was
unreachable. The app's own in-product "recent" surface — richer and already
authenticated — recovered the right target with no round trip needed.

## Step 2: Prove the tool can render anything before debugging code

A blank or wrong-looking page has two possible causes that look identical
from the symptom alone: the app is broken, or the viewer is broken. Assuming
the first without ruling out the second means every measurement taken
afterward is worthless, because it was taken through a broken instrument —
and the cost isn't just wasted effort, it's real edits made to innocent code.

Before touching app code:

- **Establish a known-good control.** Confirm the render surface shows
  *something* correctly (the document has plausible height, an element you
  know should be visible actually is).
- **Cross-check a second surface.** If a second render surface is
  available — the user's own browser, a different preview — confirm the
  symptom actually reproduces there before trusting it's a code problem.
- **Escalate only after clearing the environment.** Only move to code-level
  isolation once the environment itself has been ruled out.

Real case: a page appeared blank in an agent-controlled preview pane. A long
sequence of component isolation, cache clearing, and animation-code rewrites
followed — all wasted, because the pane itself had never rendered the app at
all, while the user's actual browser rendered it correctly the whole time.

## Step 3: When interactive state won't update, instrument the pipeline before rewriting it

A UI that silently fails to update has a chain behind it: event → state →
computed value → rendered output. Seeing only that the end result is wrong
doesn't tell you which link broke — and guessing at the last link, usually
the part you can see (the animation or rendering code), turns every rewrite
into a shot in the dark against a component that might be entirely innocent.

Emit each intermediate value in that chain as a plain, non-animated attribute
or text node, and read them back. Plain attributes are the control: if they
update correctly while the derived or animated output doesn't, the logic is
fine and the rendering layer is at fault — no further rewrites needed there.
If the plain attributes are wrong too, the fault sits upstream of rendering
entirely, and rewriting rendering code again won't touch it.

Real case: an interactive component "just didn't update." Three successive
rewrites of its animation wiring — different library call shapes, then a full
structural remount — changed nothing. One instrumentation pass, rendering the
intermediate values as plain DOM attributes, took a single edit and showed
state and the computed target were both already correct. The failure was
entirely downstream, which meant none of the three prior rewrites had ever
had a chance of fixing it.

## Closing check

Before spending effort on the target itself, confirm the observation channel
is trustworthy: a missing tab, a blank page, or state that "just won't
update" might be proof about the thing being observed — or it might just be a
fact about the observer. One cheap check settles which.
