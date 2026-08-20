---
name: youtube-to-agent
description: Turn a YouTube tutorial into a working Claude Code skill or agent. Watches the video with /watch, gets an independent second read from Gemini's native video understanding, reconciles the two into one build spec, then hands that spec to skill-creator. Use when the user pastes a YouTube tutorial link and says "build this", "turn this into a skill", or "make an agent out of this".
argument-hint: "<youtube-url> [what you want out of it]"
allowed-tools: Bash, Read, Write, Skill, AskUserQuestion
license: MIT
user-invocable: true
---

# youtube-to-agent

Two independent readers watch the same video. /watch gives you frames plus a
timestamped transcript inside your own context. Gemini reads the video natively
on Google's side and returns a written spec. They are wrong in different ways,
and the disagreement is the useful part.

## Platform note (this machine is macOS, Apple Silicon)

- Use `python3`. Both `python` and `python3` resolve to the same miniforge
  Python 3.13 here, so either runs, but `python3` stays correct if the
  miniforge shim ever leaves PATH.
- The Gemini pass script lives beside this file at
  `~/.claude/skills/youtube-to-agent/scripts/gemini_review.py`. Call it by
  that absolute path so it works from any working directory.
- Multi-line commands continue with `\`, not `^`.
- The key lives in the environment variable `GEMINI_API_KEY`. If a run reports
  no key, it was exported into a shell profile after this shell started — read
  it back with `grep GEMINI_API_KEY ~/.zshrc ~/.zprofile ~/.zshenv` and pass it
  through `--key` rather than telling the user to set it again.
- **Dependencies are not installed on this machine yet.** The Gemini pass needs
  `google-genai` (`python3 -m pip install google-genai`); /watch needs `ffmpeg`,
  which needs Homebrew first. Check both before Step 1 rather than discovering
  it at Step 3.

## Step 1: Scope before spending anything

Ask what the user actually wants if they did not say. Then **check for captions
before checking the duration** — captions decide which path you are on, and
duration only matters on one of them.

Frames are the expensive channel. The transcript is the cheap one, and its limit
is completely different. Do not generalise the frame budget to the whole task.

- **Captions exist:** length is not a scoping problem. A full-length
  `--detail transcript` pass over a four-hour video costs a few tens of thousands
  of tokens for 100% coverage. Take the whole thing. Scope the *frames*, not the
  video.
- **No captions:** frames are the only evidence, so the old rule holds — anything
  over about 20 minutes gets scoped to a section unless the user insists.

Never split a captioned video into equal frame-bearing chunks. That is the most
expensive and least accurate option available: hundreds of arbitrarily-placed
frames, a huge image-token bill, and repeated compaction that discards the
earliest chunks' visual evidence before the spec is ever written.

## Step 2: The Claude pass

**Long captioned video — do it in this order:**

1. Full-length `--detail transcript` pass. No truncation, no windowing.
2. Strip caption overlap (below) before reading a single line.
3. Pick cue moments *from the transcript* — the places where something is
   actually demonstrated.
4. Spend the frame budget on those moments via `--timestamps`. Reserve
   `--resolution 1024` for frames where on-screen text must be read; it costs
   roughly 4x per frame.
5. Checkpoint findings to disk after each pass, so compaction cannot erase them.

**Short video or no captions:** run /watch directly. Pick the detail mode on
purpose: `transcript` for talking heads, `efficient` for a first look at a long
screen recording, `balanced` when you need to read the screen, `--resolution 1024`
for terminal and code work. Use --start and --end whenever a section was named.

Always pass --no-whisper: transcription runs locally in this pipeline, never
through a paid API.

### Strip the caption overlap first

YouTube auto-captions are emitted as a rolling two-line window, so consecutive
segments repeat the previous segment's tail before adding new words. Read as-is,
a transcript costs almost exactly twice what its information content warrants —
one measured case went from 115,553 words to 57,824, a 50% reduction with no
loss at all.

Nothing upstream flags this. The raw report just looks like a long transcript.

For each line, find the longest suffix of the previous line that matches a prefix
of the current one, keep only the remainder, and carry the timestamp of the line
that introduced the new words. Report the before/after word count so the saving
is visible.

Two encoding gotchas that will bite:

- The report may contain bytes that are not valid UTF-8. Open with an explicit
  errors fallback.
- Timestamps in these reports run as cumulative MM:SS past the hour — `243:15`
  means 4h03m15s, not 243 hours. Convert to HH:MM:SS before passing anything
  back as `--start`, `--end` or `--timestamps`.

Read every frame path. Then write the six section spec to notes/claude-pass.md
BEFORE looking at Gemini's answer, or you will anchor to it.

## Step 3: The Gemini pass

    python3 ~/.claude/skills/youtube-to-agent/scripts/gemini_review.py "<url>" \
      --samples 2 --start <seconds> --end <seconds> \
      --focus "<what the user asked for>" > notes/gemini-pass.md

Two samples on purpose. A claim in both samples is worth something. A claim in
one is the model guessing.

**This pass has a coverage ceiling, and it does not tell you when it hits one.**
Run it per window with explicit `--start`/`--end` on anything long, rather than
once against the whole URL.

## Step 3.5: Assert coverage before you reconcile

A truncated Gemini read exits 0 and produces a well-formed, confident spec. It is
shaped exactly like a complete one. In one measured case the pass ingested roughly
the opening few minutes of a 4h03m video and returned six polished sections; every
mechanical signal said success.

Before reconciling anything, prove the second reader reached the end of each
requested window:

- Require it to quote something from the final minutes of the window.
- Compare its reported input-token count against the expected tokens-per-second
  for the duration. ~55k input tokens is minutes of footage, not hours.
- Watch for the semantic tell: phrases like "not reached in this clip", or a
  spec that describes nothing past initial setup.

Treat any shortfall as partial coverage and rerun that window. Then constrain
what the labels are allowed to say:

- CONFIRMED may only be applied inside the range **both** readers actually
  covered.
- The "what the video does not show" section must be **discarded entirely** for
  any range one reader never reached. A partial reader's silence about unread
  material is indistinguishable from a finding of absence, and marking it as
  absence fabricates a conclusion.

## Step 4: Reconcile into SPEC.md

Three labels on every line. CONFIRMED means both agree, build on it. SINGLE
SOURCE means one reader only, keep it and mark it. CONFLICT means go look at the
frames yourself and settle it, never average two guesses.

Throw away every timestamp, duration and count. Keep exact strings. Watch for the
archetype trap: a step that reads like documentation rather than like this video
probably came from training data.

### Reconcile coverage against scope

For each scope area the user asked for, record **where in the source it was
actually found and how substantial it was**. Mark explicitly any area the source
does not cover.

Chapter titles, section headings and tables of contents are not evidence that
content exists. Verify each against the transcript body. A real case: a chapter
titled "Monetizing Your Skills" turned out to be ninety seconds of advertising
for the presenter's paid community, containing no monetisation methodology at
all — while the only genuinely useful monetisation content in four hours was an
unscripted aside two and a half hours in.

In the emitted spec, put a visible boundary between SOURCED material and
SUPPLIED material. A section filled from your own general knowledge looks exactly
like an extracted one, and the user will reasonably read it as coming from the
video.

When the source does not cover something the user asked for, **report the gap as
a finding before building anything on top of it**. The gap changes what the
deliverable can honestly claim, and that is the user's decision to make, not a
hole to quietly fill.

## Step 5: Build and verify

Hand SPEC.md to skill-creator. Say plainly that it came from a video, that
SINGLE SOURCE lines are unverified, and which scope areas the source did not
actually cover. Then run the new skill once on a real input and fix what breaks.
A skill built from a tutorial and never executed is a summary of a video, not a
tool.

## Failure modes

- No captions: /watch returns frames only. Gemini still hears the audio, so the
  spoken content is covered. Say so in the spec, and run faster-whisper locally
  if you need the transcript on disk.
- Gemini 429s on every model: free tier quota is spent. Run the Claude pass alone
  and mark the whole spec SINGLE SOURCE.
- The two readers disagree about almost everything: the window was too wide.
  Narrow to a section and rerun both.
- Gemini agrees with everything and adds nothing: suspect truncation, not
  consensus. Go back to Step 3.5.
