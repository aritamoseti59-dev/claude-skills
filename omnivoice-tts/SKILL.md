---
name: omnivoice-tts
description: Text-to-speech on this machine. Instant macOS system voices for anything spoken live, and the local OmniVoice model for voice-cloned, voice-designed, or non-English audio assets. Use when asked to speak, say something aloud, read text out, narrate, generate a voiceover or audio notification, clone a voice, or produce speech in another language. Routes by latency: OmniVoice is orders of magnitude slower than real-time and must never be used for live speech.
---

# Text-to-speech on this machine

Internal skill — machine-specific paths and timings for this laptop
(macOS 26, Apple Silicon). The `.ps1` scripts alongside each `.sh` are the
Windows counterparts, kept for the other machine; on this one always use the
`.sh` scripts.

## Pick the engine first

Choosing wrong is the main failure mode here: OmniVoice sounds better, so it
is tempting, but using it for live speech means the user waits minutes for a
sentence.

| Need | Engine | Latency |
|---|---|---|
| Speak something now; notifications; progress; confirmations | `scripts/speak.sh` (macOS `say`) | instant |
| Replay a phrase already rendered by OmniVoice | `scripts/play.sh` | instant |
| Voice cloning, voice design, non-English, best quality | `scripts/render.sh` (OmniVoice) | minutes of compute per second of audio |

**Rule: nothing the user is waiting on may call OmniVoice.** If speech is
needed inside a live interaction, use `speak.sh`. OmniVoice is only for
assets generated ahead of time and reused.

## Instant speech

```bash
<skill>/scripts/speak.sh "Your text here"
<skill>/scripts/speak.sh "Slower and American" --voice Samantha --rate 150
<skill>/scripts/speak.sh "Save it" --out ~/Downloads/out.aiff
```

`--rate` is **words per minute** (default 175), not the -10..10 SAPI scale the
Windows script used. The two are not interchangeable — a `--rate 2` here is
two words per minute, not slightly-fast.

Voices actually installed on this machine (checked 2026-08-20): `Daniel`
(en-GB male, the default), `Moira` (en-IE female), `Karen` (en-AU female),
`Tessa` (en-ZA female), `Samantha` (en-US female), `Fred`/`Albert` (en-US
male), plus the novelty set (`Zarvox`, `Bubbles`, `Whisper`, …).

**There is no en-GB female voice installed.** The Windows default was
`Microsoft Hazel Desktop` (en-GB female); its closest macOS equivalents,
`Serena` and `Kate`, both need a one-time download under System Settings →
Accessibility → Spoken Content → System Voice. Until then `Daniel` keeps the
accent and `Moira` keeps the register — pick whichever matters more for the
line. An unknown `--voice` warns and falls back to the system default rather
than failing. `say -v '?'` lists what is really there.

Output is AIFF, not WAV — that is what `say` writes natively.

## Play a cached clip

```bash
<skill>/scripts/play.sh task_complete
<skill>/scripts/play.sh --list      # list clip ids
```

Cache defaults to `~/Downloads/OmniVoice/voice_cache`, overridable with
`$OMNIVOICE_CACHE_DIR`. Accepts a bare clip id or a full path to a WAV.
Playback is free — only generation costs anything, which is the whole reason
the cache exists.

## Render assets with OmniVoice

> **OmniVoice is not installed on this machine.** `render.sh` expects a venv at
> `$OMNIVOICE_ROOT/.venv/bin/omnivoice-infer-batch` (default
> `~/Downloads/OmniVoice`), and that path does not exist here — checked
> 2026-08-20. The script exits 1 with `OmniVoice venv missing` rather than
> failing obscurely. Install it, or point `$OMNIVOICE_ROOT` at an existing
> install, before promising anyone a cloned voice.

Always batch. The 3.1 GB model loads once per run, so one run of ten clips
beats ten runs of one.

```bash
<skill>/scripts/render.sh phrases.jsonl --num-step 8 --estimate-only
<skill>/scripts/render.sh phrases.jsonl --num-step 8
```

Manifest is JSONL, one clip per line. Only `id` and `text` are required:

```json
{"id": "greeting", "text": "Good morning.", "language_id": "en"}
{"id": "cloned",   "text": "In my own voice.", "ref_audio": "/Users/you/me.wav", "ref_text": "exact transcript of me.wav"}
{"id": "designed", "text": "Calm and slow.", "instruct": "calm British narrator, low energy"}
```

`ref_audio` (5–15 s of clean speech) + `ref_text` clones a voice. `instruct`
designs one when no reference audio exists. Also accepted: `duration`,
`speed`.

Script guards: refuses jobs estimated over `--max-minutes` (default 15) unless
`--force`, and refuses to start when another render is running unless
`--allow-concurrent`.

### Speed levers

Defaults are `num_step=32`, `guidance_scale=2.0`, `t_shift=0.1`.

**`num_step` did not reduce runtime on the Windows machine.** Measured twice
there: `num_step=32` gave 148x real-time, `num_step=8` gave 159x — slightly
slower, not 4x faster. The cause is architectural rather than machine-specific:
runtime is dominated by autoregressive token generation in the Qwen3 backbone,
which `num_step` does not touch; it only controls iterative decoding of the
audio codebooks. Expect that to hold here too, but do not promise a user it
will until it is measured on this machine.

Untested anywhere, so do not quote numbers for these:

- `--guidance_scale 1.0` removes the CFG pass. Plausibly helps, unverified,
  and costs prompt adherence.
- Weights are float32; bfloat16 would halve memory traffic. Needs a code
  change, not a flag.

If a job is too slow, the only reliable lever is **less text**.

## Before starting any render

1. Run with `--estimate-only` first and state the estimate to the user.
2. Over ~10 min, get explicit confirmation before starting — the cost is
   invisible up front; a paragraph looks small and renders for hours.
3. Start it in the background, never foreground — these outlive tool
   timeouts and get orphaned.
4. Poll progress by stat-ing the output WAVs directly, not a directory
   listing (see gotchas).

## Measured facts and gotchas

- **The ~150-160x-slower-than-real-time figure is a Windows measurement, on
  4 CPU cores.** Two runs there: 3.64 s of audio in 9 min 18 s (148x,
  `num_step=32`); 11.79 s of audio in 31 min 38 s (159x, `num_step=8`).
  `render.sh` carries that ratio as its estimator default
  (`$OMNIVOICE_SEC_PER_SEC`, 175). Apple Silicon will almost certainly differ.
  **Benchmark one short clip and reset `$OMNIVOICE_SEC_PER_SEC` before quoting
  any estimate to the user on this machine.**
- **A finished WAV does not mean a finished job.** In batch mode on the
  Windows runs, all output files appeared roughly 3 minutes in while the
  process ran another ~28 minutes before exiting. Judge completion by process
  exit or the script's own `Finished` line — never by the output files
  existing. Reporting "done" off the file listing understated one run by 10x.
  This is a property of the batch writer, not of the OS.
- **Check for orphans before assuming nothing is running:**
  `pgrep -f omnivoice-infer-batch`. Renders survive session teardown.
- **`huggingface_hub` downloads stalled at zero bytes on the Windows
  machine**, in both directions of `HF_HUB_DISABLE_XET`. That was a property
  of that machine's network and is **untested here**. If a fetch hangs at zero
  bytes, recognise the symptom and pull with curl instead of retrying.
- **Directory listings can report stale sizes for files being written.**
  Observed on NTFS; the safe habit is platform-independent — `stat` the WAV
  directly rather than reading a recursive folder total, which can sit frozen
  while the file is actively growing.
- **`ffmpeg` is not installed** (checked 2026-08-20), so OmniVoice runs print
  a pydub warning. Harmless — output is WAV via soundfile. It only matters for
  mp3/m4a.
- The PowerShell execution-policy gotcha from the Windows notes does not apply
  here. The macOS equivalent is the executable bit: if a script fails with
  "permission denied", `chmod +x scripts/*.sh` (already done at install).
