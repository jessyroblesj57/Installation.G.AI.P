# [SURGICAL HUD]
$Buffer = "C:\shark\live_stream.txt"
[Console]::Title = "SNIPER HUD: READY"
Write-Host "--- WAITING FOR CONFIRMED PACKETS ---" -F Cyan

# Wait for sniffer to initialize
while (-not (Test-Path $Buffer)) { Start-Sleep -m 500 }

Get-Content $Buffer -Wait | ForEach-Object {
    $Line = "$_"

    # 1. DETECT SEED (Round Start)
    if ($Line -match "63 6c 69 65 6e 74 5f 73 65 65 64") {
        Write-Host "`n[>>>] SEED SENT (ROUND START)" -F Yellow
    }

    # 2. DETECT MULTIPLIER (Round Result)
    if ($Line -match "6d 75 6c 74 69 70 6c 69 65 72") {
        # Convert Hex line to Text to extract the number
        try {
            $Text = -join ($Line -split ' ' | ForEach-Object { [char][byte]"0x$_" })

            # Regex to find "multiplier": 12.34
            if ($Text -match 'multiplier..:\s*([\d.]+)') {
                $Val = $matches[1]

                Clear-Host
                Write-Host "`n*********************************" -F Green
                Write-Host "   MULTIPLIER: $Val   " -F Black -B Green
                Write-Host "*********************************`n" -F Green
                [Console]::Title = "LOCKED: $Val"
                [System.Console]::Beep(1500, 150)
            }
        } catch {
            # Ignore conversion errors from partial lines
        }
    }
}