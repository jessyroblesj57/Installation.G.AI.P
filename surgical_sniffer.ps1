# [SURGICAL SNIFFER - V2]
$SharkRoot = "C:\shark"
$Buffer = "$SharkRoot\live_stream.txt"

# 1. SETUP
Write-Host "--- NETWORK INTERFACE CHECK ---" -F Cyan
& "C:\Program Files\Wireshark\tshark.exe" -D
Write-Host "---------------------------------" -F Cyan
Write-Host "The script is set to use Interface #8." -F Yellow
Write-Host "If that is NOT your active internet (Wi-Fi/Ethernet), edit this script." -F Gray
Start-Sleep -Seconds 3

Stop-Process -Name chrome,tshark -Force -ErrorAction SilentlyContinue
$env:SSLKEYLOGFILE = "$SharkRoot\ssl_keys.log"
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" "https://skillmachine.net"

# 2. THE CAPTURE
Write-Host "[*] SURGICAL SNIFFER ACTIVE. DO NOT CLOSE." -F Red
# We pipe to file to prevent crashes.
# Filter matches: "client_seed" OR "multiplier"
& "C:\Program Files\Wireshark\tshark.exe" -i 8 -o "tls.keylog_file:$SharkRoot\ssl_keys.log" -Y "frame contains 63:6c:69:65:6e:74:5f:73:65:65:64 or frame contains 6d:75:6c:74:69:70:6c:69:65:72" -x -l > $Buffer
