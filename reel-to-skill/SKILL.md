---
name: reel-to-skill
description: Turn an Instagram reel (or TikTok, or any short yt-dlp-supported clip) into a working Claude Code skill or agent. Fetches the caption and video with yt-dlp, transcribes the audio locally with Whisper, reads the on-screen content as frames, then hands the reconciled spec to skill-creator. Use when the user pastes an instagram.com/reel or instagram.com/p link and asks to turn it into a skill, agent, or lesson. Also triggers on "reel this", "skill this reel", "learn this reel".
argument-hint: "<reel-url> [what you want out of it]"
allowed-tools: Bash, Read, Write, Skill, AskUserQuestion
license: MIT
user-invocable: true
---

# reel-to-skill

A reel teaching a workflow has two channels, and they carry different things.
The audio is the narration; the screen is where the actual commands, settings
and file paths live. Transcribing only the audio throws away the half that is
usually harder to reconstruct — so this skill reads both, then reconciles.

## Platform note (this machine is macOS, Apple Silicon)

- `mlx-whisper` is Apple Silicon only, and this **is** an arm64 Mac — so it is
  the right engine here and runs on the GPU. `openai-whisper` is the CPU
  fallback, not the default.
- The two take different flag styles. **mlx-whisper takes hyphenated** flags
  (`--output-format`, `--output-dir`); **openai-whisper takes underscored**
  ones (`--output_format`, `--output_dir`). Do not mix them.
- Use `python3`.
- Multi-line commands continue with `\`, not `^`.
- **The pipeline is installed directly, not through `uvx`.** `yt-dlp`,
  `mlx_whisper`, `ffmpeg` and `ffprobe` are all on PATH in the miniforge env
  (installed 2026-08-20). Call them by name — there is no `uv`/`uvx` on this
  machine, so any `uvx ...` command copied from the source guide will fail
  with "command not found".
- `ffmpeg` is the static build bundled by `imageio-ffmpeg`, symlinked into
  `~/miniforge3/bin/ffmpeg`. It is a real ffmpeg 7.1 and handles everything
  this pipeline needs; it is not a Homebrew install, so `brew upgrade` will
  not touch it.

## Step 1: Fetch metadata (no download yet)

```
yt-dlp --skip-download --dump-json "<REEL_URL>"
```

From the JSON keep: `description` (this is the caption), `uploader`, `channel`,
`like_count`, `comment_count`. Save them to a working folder at
`~/reel-to-skill-runs/<shortcode>/`.

The caption is not a footnote. Creators routinely put the steps in the caption
that they gloss over in the audio, and on a music-only reel it is the entire
payload. Read it before deciding the reel is worthless.

## Step 2: Download the video

```
yt-dlp -f "best[ext=mp4]/best" -o "<workdir>/reel.%(ext)s" "<REEL_URL>"
```

## Step 3: Transcribe the audio locally

```
mlx_whisper "<workdir>/reel.mp4" \
  --model mlx-community/whisper-large-v3-turbo \
  --output-format txt --output-dir "<workdir>" --language en
```

Nothing leaves the machine — transcription is local on either engine. The model
*source* differs though: `mlx-whisper` pulls weights from HuggingFace
(`mlx-community/...`) on first run, while `openai-whisper` pulls from
`openaipublic.azureedge.net`. The hf_hub zero-byte stall recorded in the old
Windows notes was a property of that machine's network, not of this pipeline,
and is untested here. If a first mlx run hangs at zero bytes, that is the
symptom to recognise — fall back to `openai-whisper` rather than retrying.

**Model choice on this machine is unmeasured — do not quote the numbers below
as if they described it.** They were measured on the Windows box this skill was
first written for, where torch fell back to CPU FP32 with no usable GPU:

| Model | Wall time (Windows, CPU FP32, 29s sample) | Output |
|-------|-------------------------------------------|--------|
| `turbo` | 228s | lowercase, no punctuation |
| `base` | 79s | correct capitalisation and sentence breaks |

That constraint does not exist here. On Apple Silicon `mlx-whisper` runs on the
GPU, which is exactly the configuration the original source guide assumed when
it specified `turbo`. So the guide's choice is most likely right on this
machine, and the `base` workaround above is most likely obsolete.

**Most likely is not measured.** Benchmark once on a real clip before writing
any timing claim into a spec or telling the user how long to wait, then replace
this section with the measured numbers. Until that happens, quote no figures.

Step back to `--model mlx-community/whisper-base-mlx` if `turbo` disappoints on
speed or the clip is trivially short. Fall back to `openai-whisper` (underscored
flags, `--model base`) only if mlx cannot fetch or run its weights at all.

Drop `--language en` for a non-English reel, or set it to that language. Leaving
it off entirely lets Whisper autodetect, which is usually right but occasionally
transcribes accented English as another language.

Tell the user transcription is running and roughly how long it will take. A
silent multi-minute wait is indistinguishable from a hang.

## Step 4: Read the screen

The reel is still on disk at this point — this is the only chance to read it.

```
python3 ~/.claude/plugins/cache/claude-video/watch/<version>/skills/watch/scripts/watch.py \
  "<workdir>/reel.mp4" --detail balanced --max-frames 20 --resolution 1024 --no-whisper
```

The `claude-video` plugin is **not installed on this machine** — `~/.claude/plugins`
does not exist yet. Install it before relying on this step, and glob the real
version directory rather than hardcoding one; the `0.2.0` in the original note
was pinned to a different machine's install.

- `--no-whisper` is mandatory: audio is already transcribed locally in Step 3,
  and this flag stops the clip being uploaded to a paid transcription API.
- `--resolution 1024` because the point of this pass is reading terminal text,
  menu labels and file paths. 512px will not resolve them.
- Frames are deduplicated by default, so a static screen recording costs far
  fewer than 20.

Then `Read` every frame path the script prints, in one message.

Skip this step only for a pure talking-head reel with nothing on screen — and
decide that from the frames, not from the transcript.

## Step 5: Sanity-check before building

Two guards, in order:

1. **Music-only.** If the transcript is empty, or one short phrase repeats for
   most of the file, the audio is a music bed. Say so and continue from the
   caption and frames instead of failing.
2. **Nothing to teach.** If transcript, caption and frames together describe no
   actual procedure — a motivational clip, a results screenshot, an ad — say so
   and stop. Do not synthesise a skill out of a slogan. A reel that teaches
   nothing should produce no skill, and reporting that is a valid outcome.

## Step 6: Reconcile the two readers

Write `<workdir>/SPEC.md` labelling every claim by where it came from:

- **CONFIRMED** — said in the audio *and* visible on screen. Build on it.
- **SINGLE SOURCE** — one channel only. Keep it, mark it, do not present it as
  verified. Exact commands read off a frame but never spoken belong here.
- **CONFLICT** — the narration and the screen disagree. The screen usually wins
  for anything literal (a flag, a path, a version), because presenters misspeak
  constants. Settle it by looking again, never by averaging.

Keep exact strings — commands, filenames, flags. Throw away timestamps and
counts. Watch for the archetype trap: a step that reads like generic
documentation rather than like this specific reel probably came from your own
training data, not the source. Mark supplied material as supplied, visibly.

## Step 7: Hand off to skill-creator

Ask one question first: **skill or agent?** A skill teaches a method applied
inside a conversation; an agent is a worker dispatched to go do the thing. When
in doubt, skill — it can be promoted later.

Then invoke `skill-creator` with `SPEC.md`, the caption, the author handle and
the link. Tell it plainly that the source was a reel, that SINGLE SOURCE lines
are unverified, and which parts came from frames rather than narration.

Record provenance in the generated skill: the reel URL, the author, and the run
date. A skill whose source cannot be traced cannot be re-derived when it breaks.

## Step 8: Clean up, then actually run it

Delete `reel.mp4` once the transcript and frames are secured. Keep the
transcript, metadata, `SPEC.md` and frames as the archive.

Then run the new skill once, on a real input, while the reel is fresh. A skill
built from a tutorial and never executed is a summary of a video, not a tool.

## Error handling

- **yt-dlp login or rate-limit error** — retry once with
  `--cookies-from-browser chrome` (read-only use of the existing browser
  session). If it still fails, wait an hour; Instagram rate-limits bursts and
  single links recover quickly. Process reels one at a time, never in batches —
  anonymous fetching is the one fragile dependency in this pipeline.
- **Photo post or carousel** — no audio track. Say so and offer to build from
  the caption and images alone.
- **Transcript in the wrong language** — set `--language` explicitly and rerun
  Step 3; the video is still on disk if Step 8 has not run.
- **Nonsense transcript, repeated words** — music-only reel, see Step 5.
- **Never crash the session.** Report the failing step and stop cleanly.

## Provenance

Built from "The Reel to Skill Engine" by Jens Heitmann (@jens.heitmann),
extracted 2026-08-16. Deviations from the source, all deliberate:

- **Platform.** First adapted for Windows: `openai-whisper` in place of
  `mlx-whisper`, underscored flags, and `base` in place of `turbo` — both
  benchmarked on that machine, which had no usable GPU. Re-adapted for macOS on
  Apple Silicon, 2026-08-20: `mlx-whisper` and `turbo` revert to the guide's
  original choices, but are **unbenchmarked here**. See Step 3.
- **Step 4 frames pass and Step 6 reconciliation** are additions. The source
  transcribes audio only and deletes the video, which discards everything shown
  on screen — usually where a workflow reel's actual commands live.
- **Step 5 guard 2** (reel teaches no procedure → build nothing) is an addition.

Unverified against a real reel at time of writing: the yt-dlp fetch and download
steps were never exercised end to end, only the transcription path. Steps 1, 2
and the `--cookies-from-browser` retry remain SINGLE SOURCE from the guide.
