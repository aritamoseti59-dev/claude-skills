#!/usr/bin/env bash
# macOS counterpart of play.ps1. Play a pre-rendered clip from the OmniVoice
# phrase library. Instant — playback costs nothing, only generation is
# expensive. This is what notifications and hooks should call, never the
# OmniVoice model directly.
#
#   play.sh task_complete
#   play.sh /full/path/to/clip.wav
#   play.sh --list
set -euo pipefail

CACHE_DIR="${OMNIVOICE_CACHE_DIR:-$HOME/Downloads/OmniVoice/voice_cache}"

if [ "${1:-}" = "--list" ]; then
    find "$CACHE_DIR" -maxdepth 1 -name '*.wav' -exec basename {} .wav \; 2>/dev/null
    exit 0
fi

name="${1:?usage: play.sh <clip-id|path-to-wav> | --list}"

# Accept either a bare clip id ("task_complete") or a full path to a WAV.
if [ -f "$name" ]; then path="$name"; else path="$CACHE_DIR/$name.wav"; fi

if [ ! -f "$path" ]; then
    have=$(find "$CACHE_DIR" -maxdepth 1 -name '*.wav' -exec basename {} .wav \; 2>/dev/null | paste -sd, -)
    echo "No clip '$name'. Available: ${have:-<none>}" >&2
    exit 1
fi

exec afplay "$path"
