# Play a pre-rendered clip from the OmniVoice phrase library. Instant —
# playback costs nothing, only generation is expensive. This is what
# notifications and hooks should call, never the OmniVoice model directly.
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$Name,
    [string]$CacheDir = "C:\Users\roman\Downloads\OmniVoice\voice_cache",
    [switch]$List
)

if ($List) {
    Get-ChildItem $CacheDir -Filter *.wav -ErrorAction SilentlyContinue |
        ForEach-Object { $_.BaseName }
    return
}

# Accept either a bare clip id ("task_complete") or a full path to a WAV.
$path = if (Test-Path -LiteralPath $Name) { $Name } else { Join-Path $CacheDir "$Name.wav" }

if (-not (Test-Path -LiteralPath $path)) {
    $have = (Get-ChildItem $CacheDir -Filter *.wav -ErrorAction SilentlyContinue |
             ForEach-Object { $_.BaseName }) -join ', '
    Write-Error "No clip '$Name'. Available: $have"
    exit 1
}

(New-Object System.Media.SoundPlayer $path).PlaySync()
