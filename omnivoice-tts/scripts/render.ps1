# Render audio assets with the local OmniVoice model (voice cloning, voice
# design, 600+ languages). SLOW: roughly 150x real-time on this CPU at the
# default num_step=32. Always batch — the 3.1 GB model loads once per run.
#
# Refuses jobs estimated over -MaxMinutes unless -Force is passed. That gate
# exists because the cost is invisible up front: a page of text looks small
# and renders for half a day.
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$TestList,
    [string]$ResDir = "C:\Users\roman\Downloads\OmniVoice\voice_cache",
    [int]$NumStep = 8,
    [int]$MaxMinutes = 15,
    [switch]$Force,
    [switch]$EstimateOnly,
    [switch]$AllowConcurrent
)

$root = "C:\Users\roman\Downloads\OmniVoice"
$exe = "$root\.venv\Scripts\omnivoice-infer-batch.exe"

if (-not (Test-Path $exe))      { Write-Error "OmniVoice venv missing at $exe"; exit 1 }
if (-not (Test-Path $TestList)) { Write-Error "Manifest not found: $TestList"; exit 1 }

# --- Cost estimate -------------------------------------------------------
# Calibrated against two measured runs on this machine:
#   num_step=32:  3.64s audio -> 558s wall  (148x real-time)
#   num_step=8:  11.79s audio -> 1898s wall (159x real-time)
# num_step did NOT change the ratio, so there is deliberately no num_step
# term here — runtime is dominated by autoregressive token generation in the
# LLM backbone, which num_step does not affect. The earlier version scaled by
# (NumStep/32) and under-predicted the second run by ~5x.
# 175 is above both measurements on purpose: under-estimating is the harmful
# direction, since the whole point of the gate is to prevent surprise.
$lines = Get-Content $TestList | Where-Object { $_.Trim() }
$chars = 0
foreach ($l in $lines) {
    try { $chars += ($l | ConvertFrom-Json).text.Length } catch {
        Write-Error "Line is not valid JSON: $l"; exit 1
    }
}
$audioSec = $chars / 14.0
$estMin = [math]::Round((($audioSec * 175) + 30) / 60.0, 1)   # +30s model load

Write-Output "Clips:      $($lines.Count)"
Write-Output "Audio:      ~$([math]::Round($audioSec,1))s"
Write-Output "num_step:   $NumStep  (does not affect runtime on this machine)"
Write-Output "Estimated:  ~$estMin min"

if ($EstimateOnly) { return }

if ($estMin -gt $MaxMinutes -and -not $Force) {
    Write-Error "Estimated $estMin min exceeds -MaxMinutes $MaxMinutes. Re-run with -Force to proceed, or lower -NumStep / shorten the text."
    exit 1
}

# Two renders at once means two 3.1 GB models thrashing 4 cores; both crawl.
$running = Get-Process omnivoice-infer-batch -ErrorAction SilentlyContinue
if ($running -and -not $AllowConcurrent) {
    Write-Error "An OmniVoice render is already running (PID $($running[0].Id), started $($running[0].StartTime.ToString('HH:mm:ss'))). Wait for it, or pass -AllowConcurrent."
    exit 1
}

New-Item -ItemType Directory -Force -Path $ResDir | Out-Null
Write-Output "Starting $(Get-Date -Format 'HH:mm:ss') ..."

& $exe --model "$root\model" --test_list $TestList --res_dir $ResDir --num_step $NumStep

Write-Output "Finished $(Get-Date -Format 'HH:mm:ss')"
Get-ChildItem $ResDir -Filter *.wav | ForEach-Object {
    "  {0}  {1} KB" -f $_.BaseName, [math]::Round($_.Length / 1KB)
}
