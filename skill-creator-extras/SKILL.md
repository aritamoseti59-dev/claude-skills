---
name: skill-creator-extras
description: Corrections and additions to the built-in skill-creator skill, which is read-only and cannot be edited directly. Load this alongside skill-creator whenever creating, benchmarking, or evaluating a skill — particularly when running eval test cases or aggregating benchmark results. Covers the eval directory layout that aggregate_benchmark.py actually requires and the silent zero-delta failure it produces when the layout is wrong.
---

# skill-creator-extras

`skill-creator` is a read-only system skill, so these corrections live here
instead of in its own file. **Load both.** This file contains only the delta;
everything else in skill-creator still applies as written.

Pairing: this skill supplements `skill-creator`. If skill-creator is ever
updated upstream to include the material below, delete the corresponding
section here rather than maintaining two copies.

## The eval directory layout in the prose does not match what the aggregator globs for

This is the correction that matters most, because getting it wrong produces a
**plausible wrong answer rather than an error**.

`skill-creator`'s prose tells you to save each test case's results to
`<eval-dir>/with_skill/outputs/` and to write `grading.json` into the run
directory. `aggregate_benchmark.py` does not look there. It globs for:

```
eval-*/<config>/run-*/grading.json
```

…and reads pass rates from a **`summary`** key inside each `grading.json`.

Following the documented prose layout produces neither the path shape nor the
key. The script then finds zero runs, emits `"runs": []`, prints
**`Delta: +0.00`**, and exits **0**.

### Why this is dangerous rather than merely annoying

A zero delta is a perfectly plausible experimental result. It reads as "the
skill made no difference" — a real, publishable finding. Nothing in the output
distinguishes it from a discovery failure. In the run that surfaced this, six
graded runs existed with correct `grading.json` files and the true delta was
**+0.49**; the reported delta was `+0.00`.

### What to do

**Before running the aggregator**, confirm your tree matches
`eval-N/<config>/run-N/grading.json` exactly, and that each `grading.json`
carries a `summary` block.

**Treat a `+0.00` delta as suspect until proven.** Check the `runs` array in
the aggregator's output is non-empty before reading the delta at all. An empty
`runs` array with a printed delta is a discovery failure, not a measurement.

**Fail loudly rather than reporting zero.** If you are modifying the
aggregator, make it error when it discovers no runs, and when it finds eval
directories whose config subdirectories contain a `grading.json` but no
`run-*` directory — that combination is the exact signature of the documented
prose layout having been followed.

The same silent-shape-mismatch risk applies to the `grading.json` field names.
skill-creator warns about this for the viewer but not for the aggregator; the
warning applies to both.

## The general rule this is an instance of

A pipeline stage that reports an aggregate must distinguish **"computed zero"**
from **"found nothing to compute"**. Where a discovery failure renders as a
plausible measurement, every downstream conclusion is drawn from an empty set
with no signal that anything went wrong.

Apply this to any eval or benchmark tooling you write: the empty-input case
should be an error, never a number.
