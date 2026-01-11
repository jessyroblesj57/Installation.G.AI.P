# [SURGICAL HUD - V2]
$Buffer = "C:\shark\live_stream.txt"
[Console]::Title = "SNIPER HUD: READY"
Write-Host "--- WAITING FOR CONFIRMED PACKETS ---" -F Cyan

while (-not (Test-Path $Buffer)) { Start-Sleep -m 500 }

Get-Content $Buffer -Wait | ForEach-Object {
    $Line = "$_"

    # 1. DETECT SEED
    if ($Line -match "63 6c 69 65 6e 74 5f 73 65 65 64") {
        Write-Host "`n[>>>] SEED SENT (ROUND START)" -F Yellow
    }

    # 2. DETECT MULTIPLIER
    if ($Line -match "6d 75 6c 74 69 70 6c 69 65 72") {
        try {
            # Robust Hex Parsing:
            # 1. Split by space
            # 2. Select only valid 2-digit hex values (ignore offsets/spaces)
            # 3. Convert to characters
            $HexParts = $Line -split ' ' | Where-Object { $_ -match '^[0-9a-fA-F]{2}$' }
            $Text = -join ($HexParts | ForEach-Object { [char][byte]"0x$_" })

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
            # Silent fail on bad lines
        }
    }
}
