#!/usr/bin/env bash
# macOS counterpart of speak.ps1. Instant text-to-speech via the built-in
# macOS `say` voices. Latency is effectively zero — this is the engine for
# anything spoken live. For voice cloning / non-English / high quality, use
# render.sh instead.
#
#   speak.sh "Save it"
#   speak.sh "Save it" --voice Daniel --rate 200 --out /tmp/out.aiff
#
# Voice note: the Windows default was "Microsoft Hazel Desktop" (en-GB
# female). The closest macOS equivalents, "Serena" and "Kate", are NOT
# installed on this machine and need a one-time download under System
# Settings > Accessibility > Spoken Content > System Voice. Until then the
# default below is "Daniel" — the only en-GB voice actually present. For a
# female register instead of the accent, pass --voice Moira (en-IE) or
# --voice Samantha (en-US). `say -v '?'` lists what is really installed.
#
# Rate note: SAPI took -10..10; `say -r` takes words per minute (default
# ~175). They are not the same scale, so the flag is WPM here.
set -euo pipefail

text="${1:?usage: speak.sh <text> [--voice NAME] [--rate WPM] [--out FILE]}"
shift

voice="Daniel"
rate=175
out=""

while [ $# -gt 0 ]; do
    case "$1" in
        --voice) voice="$2"; shift 2 ;;
        --rate)  rate="$2";  shift 2 ;;
        --out)   out="$2";   shift 2 ;;
        *) echo "unknown option: $1" >&2; exit 1 ;;
    esac
done

if ! say -v '?' | awk '{print $1}' | grep -qx "$voice"; then
    echo "Voice '$voice' not installed. Using system default. Available: $(say -v '?' | awk '{print $1}' | paste -sd, -)" >&2
    voice=""
fi

args=(-r "$rate")
[ -n "$voice" ] && args+=(-v "$voice")
[ -n "$out" ]   && args+=(-o "$out")

say "${args[@]}" "$text"
[ -n "$out" ] && echo "Wrote $out"
exit 0
