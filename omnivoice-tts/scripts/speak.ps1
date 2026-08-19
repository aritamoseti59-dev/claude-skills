# Instant text-to-speech via the built-in Windows SAPI voices.
# Latency is effectively zero — this is the engine for anything spoken live.
# For voice cloning / non-English / high quality, use render.ps1 instead.
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$Text,
    [string]$Voice = "Microsoft Hazel Desktop",
    [int]$Rate = 0,       # -10 (slowest) .. 10 (fastest)
    [int]$Volume = 100,   # 0 .. 100
    [string]$Out = ""     # optional: write a WAV instead of playing
)

Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer

$available = $synth.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name }
if ($available -contains $Voice) {
    $synth.SelectVoice($Voice)
} else {
    Write-Warning "Voice '$Voice' not installed. Using system default. Available: $($available -join ', ')"
}

$synth.Rate = $Rate
$synth.Volume = $Volume

if ($Out) {
    $synth.SetOutputToWaveFile($Out)
    $synth.Speak($Text)
    $synth.SetOutputToDefaultAudioDevice()   # releases the file handle
    Write-Output "Wrote $Out"
} else {
    $synth.Speak($Text)
}

$synth.Dispose()
