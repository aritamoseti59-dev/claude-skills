#!/usr/bin/env bash
# macOS counterpart of render.ps1. Render audio assets with the local
# OmniVoice model (voice cloning, voice design, 600+ languages). Always batch
# — the 3.1 GB model loads once per run.
#
# Refuses jobs estimated over --max-minutes unless --force is passed. That
# gate exists because the cost is invisible up front: a page of text looks
# small and renders for half a day.
#
#   render.sh jobs.jsonl
#   render.sh jobs.jsonl --estimate-only
#   render.sh jobs.jsonl --num-step 8 --max-minutes 30 --force
set -euo pipefail

ROOT="${OMNIVOICE_ROOT:-$HOME/Downloads/OmniVoice}"
EXE="$ROOT/.venv/bin/omnivoice-infer-batch"

test_list="${1:?usage: render.sh <manifest.jsonl> [options]}"
shift

res_dir="${OMNIVOICE_CACHE_DIR:-$ROOT/voice_cache}"
num_step=8
max_minutes=15
force=0
estimate_only=0
allow_concurrent=0

while [ $# -gt 0 ]; do
    case "$1" in
        --res-dir)          res_dir="$2"; shift 2 ;;
        --num-step)         num_step="$2"; shift 2 ;;
        --max-minutes)      max_minutes="$2"; shift 2 ;;
        --force)            force=1; shift ;;
        --estimate-only)    estimate_only=1; shift ;;
        --allow-concurrent) allow_concurrent=1; shift ;;
        *) echo "unknown option: $1" >&2; exit 1 ;;
    esac
done

[ -x "$EXE" ]        || { echo "OmniVoice venv missing at $EXE" >&2; exit 1; }
[ -f "$test_list" ]  || { echo "Manifest not found: $test_list" >&2; exit 1; }

# --- Cost estimate -------------------------------------------------------
# SECONDS_PER_AUDIO_SECOND is the wall-clock cost of one second of output.
#
# The default below (175) is the WINDOWS figure, calibrated on the old 4-core
# laptop against two measured runs:
#   num_step=32:  3.64s audio -> 558s wall  (148x real-time)
#   num_step=8:  11.79s audio -> 1898s wall (159x real-time)
# num_step did NOT change the ratio, so there is deliberately no num_step
# term here — runtime is dominated by autoregressive token generation in the
# LLM backbone, which num_step does not affect.
#
# It has NOT been re-measured on Apple silicon and is almost certainly far
# too pessimistic there. That is the safe direction: over-estimating makes
# the gate fire early, under-estimating causes the surprise the gate exists
# to prevent. Re-measure one real run, then set OMNIVOICE_SEC_PER_SEC to the
# observed ratio (round UP) and delete this paragraph.
RATIO="${OMNIVOICE_SEC_PER_SEC:-175}"
[ "$RATIO" = "175" ] && echo "note: using the un-recalibrated Windows cost ratio (175x). Set OMNIVOICE_SEC_PER_SEC after one measured run." >&2

chars=$(python3 -c '
import json, sys
total = 0
for i, line in enumerate(open(sys.argv[1], encoding="utf-8"), 1):
    line = line.strip()
    if not line:
        continue
    try:
        total += len(json.loads(line)["text"])
    except Exception:
        sys.exit(f"Line {i} is not valid JSON with a text field: {line}")
print(total)
' "$test_list")

clips=$(grep -c '[^[:space:]]' "$test_list" || true)

read -r audio_sec est_min <<EOF
$(python3 -c "
a = $chars / 14.0
print(round(a, 1), round((a * $RATIO + 30) / 60.0, 1))
")
EOF

echo "Clips:      $clips"
echo "Audio:      ~${audio_sec}s"
echo "num_step:   $num_step  (does not affect runtime)"
echo "Estimated:  ~${est_min} min"

[ "$estimate_only" = "1" ] && exit 0

if [ "$force" != "1" ] && python3 -c "import sys; sys.exit(0 if $est_min > $max_minutes else 1)"; then
    echo "Estimated $est_min min exceeds --max-minutes $max_minutes. Re-run with --force, or shorten the text." >&2
    exit 1
fi

# Two renders at once means two 3.1 GB models competing for memory bandwidth.
if [ "$allow_concurrent" != "1" ] && pgrep -f omnivoice-infer-batch >/dev/null 2>&1; then
    echo "An OmniVoice render is already running (PID $(pgrep -f omnivoice-infer-batch | head -1)). Wait for it, or pass --allow-concurrent." >&2
    exit 1
fi

mkdir -p "$res_dir"
echo "Starting $(date +%H:%M:%S) ..."

"$EXE" --model "$ROOT/model" --test_list "$test_list" --res_dir "$res_dir" --num_step "$num_step"

echo "Finished $(date +%H:%M:%S)"
find "$res_dir" -maxdepth 1 -name '*.wav' -exec sh -c 'printf "  %s  %s KB\n" "$(basename "$1" .wav)" "$(( $(wc -c < "$1") / 1024 ))"' _ {} \;
