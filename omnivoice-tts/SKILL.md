---
name: omnivoice-tts
description: Text-to-speech on this machine. Instant Windows system voices for anything spoken live, and the local OmniVoice model for voice-cloned, voice-designed, or non-English audio assets. Use when asked to speak, say something aloud, read text out, narrate, generate a voiceover or audio notification, clone a voice, or produce speech in another language. Routes by latency: OmniVoice runs ~150x slower than real-time on this CPU and must never be used for live speech.
---

# Text-to-speech on this machine

Internal skill — machine-specific paths and measured timings for this laptop.

## Pick the engine first

Choosing wrong is the main failure mode here: OmniVoice sounds better, so it
is tempting, but using it for live speech means the user waits minutes for a
sentence.

| Need | Engine | Latency |
|---|---|---|
| Speak something now; notifications; progress; confirmations | `scripts/speak.ps1` (Windows SAPI) | instant |
| Replay a phrase already rendered by OmniVoice | `scripts/play.ps1` | instant |
| Voice cloning, voice design, non-English, best quality | `scripts/render.ps1` (OmniVoice) | ~2.5 min compute per second of audio |

**Rule: nothing the user is waiting on may call OmniVoice.** If speech is
needed inside a live interaction, use `speak.ps1`. OmniVoice is only for
assets generated ahead of time and reused.

## Instant speech

```powershell
powershell -ExecutionPolicy Bypass -File <skill>/scripts/speak.ps1 "Your text here"
powershell -ExecutionPolicy Bypass -File <skill>/scripts/speak.ps1 -Text "Slower and male" -Voice "Microsoft David Desktop" -Rate -2
powershell -ExecutionPolicy Bypass -File <skill>/scripts/speak.ps1 -Text "Save it" -Out "C:\path\out.wav"
```

Voices installed: `Microsoft Hazel Desktop` (en-GB female, default),
`Microsoft David Desktop` (en-US male), `Microsoft Zira Desktop` (en-US
female). An unknown `-Voice` warns and falls back rather than failing.
`-Rate` is -10..10, `-Volume` is 0..100.

## Play a cached clip

```powershell
powershell -ExecutionPolicy Bypass -File <skill>/scripts/play.ps1 task_complete
powershell -ExecutionPolicy Bypass -File <skill>/scripts/play.ps1 -Name x -List     # list clip ids
```

Cache lives at `C:\Users\roman\Downloads\OmniVoice\voice_cache`. Accepts a
bare clip id or a full path to a WAV. Playback is free — only generation
costs anything, which is the whole reason the cache exists.

## Render assets with OmniVoice

Always batch. The 3.1 GB model loads once per run (~25 s), so one run of ten
clips beats ten runs of one.

```powershell
powershell -ExecutionPolicy Bypass -File <skill>/scripts/render.ps1 -TestList phrases.jsonl -NumStep 8 -EstimateOnly
powershell -ExecutionPolicy Bypass -File <skill>/scripts/render.ps1 -TestList phrases.jsonl -NumStep 8
```

Manifest is JSONL, one clip per line. Only `id` and `text` are required:

```json
{"id": "greeting", "text": "Good morning.", "language_id": "en"}
{"id": "cloned",   "text": "In my own voice.", "ref_audio": "C:\\path\\me.wav", "ref_text": "exact transcript of me.wav"}
{"id": "designed", "text": "Calm and slow.", "instruct": "calm British narrator, low energy"}
```

`ref_audio` (5–15 s of clean speech) + `ref_text` clones a voice. `instruct`
designs one when no reference audio exists. Also accepted: `duration`,
`speed`.

Script guards, both verified: refuses jobs estimated over `-MaxMinutes`
(default 15) unless `-Force`, and refuses to start when another render is
running unless `-AllowConcurrent` — two models on 4 cores makes both crawl.

### Speed levers — measured, not assumed

Defaults are `num_step=32`, `guidance_scale=2.0`, `t_shift=0.1`.

**`num_step` does not reduce runtime on this machine.** Measured twice:
`num_step=32` gave 148x real-time, `num_step=8` gave 159x — slightly slower,
not 4x faster. Runtime is dominated by autoregressive token generation in the
Qwen3 backbone, which `num_step` does not touch; it only controls iterative
decoding of the audio codebooks. Lower it for quality experiments if you
like, but do not expect it to buy time, and never promise a user it will.

Untested on this machine, so do not quote numbers for these:

- `--guidance_scale 1.0` removes the CFG pass. Plausibly helps, unverified,
  and costs prompt adherence.
- Weights are float32; bfloat16 would halve memory traffic. Needs a code
  change, not a flag.

If a job is too slow, the only reliable lever is **less text**.

## Before starting any render

1. Run with `-EstimateOnly` first and state the estimate to the user.
2. Over ~10 min, get explicit confirmation before starting — the cost is
   invisible up front; a paragraph looks small and renders for hours.
3. Start it in the background, never foreground — these outlive tool
   timeouts and get orphaned.
4. Poll progress by checking the output WAVs directly, not a directory
   listing (see gotchas).

## Measured facts and gotchas

- **~150-160x slower than real-time**, regardless of `num_step`. Two measured
  runs: 3.64 s of audio in 9 min 18 s (148x, `num_step=32`); 11.79 s of audio
  in 31 min 38 s (159x, `num_step=8`). Budget ~3 min of compute per second of
  speech.
- **A finished WAV does not mean a finished job.** In batch mode all the
  output files appeared roughly 3 minutes in, while the process ran another
  ~28 minutes before exiting. Judge completion by process exit or the
  script's own `Finished` line — never by the output files existing. Reporting
  "done" off the file listing understated one run by 10x.
- **`huggingface_hub` downloads are broken on this machine** — they hang at
  zero bytes on HuggingFace's xet-bridge CDN, in both directions of
  `HF_HUB_DISABLE_XET`. Never let anything auto-download from HF. Weights
  are already local at `C:\Users\roman\Downloads\OmniVoice\model`; fetch new
  ones with curl instead.
- **PowerShell execution policy is Restricted** on every scope, so
  `powershell -File script.ps1` fails with "running scripts is disabled on
  this system". Always pass `-ExecutionPolicy Bypass`, as every example above
  does. Note that an agent's own PowerShell session may run with `Process`
  scope set to `Bypass`, which child processes inherit — so a script can work
  when tested from there and still fail from a plain terminal. Verify from a
  clean shell.
- **ffmpeg is not installed**, so every run prints a pydub warning. Harmless
  — output is WAV via soundfile. It only matters for mp3/m4a.
- **Directory listings report stale sizes for files being written** on NTFS.
  When checking render progress, stat the WAV directly; a recursive folder
  total can sit frozen while the file is actively growing.
- Renders survive session teardown as orphaned processes. Check with
  `Get-Process omnivoice-infer-batch` before assuming nothing is running.
