# [SURGICAL SNIFFER - FACT BASED]
$SharkRoot = "C:\shark"
$Buffer = "$SharkRoot\live_stream.txt"

# 1. SETUP
Stop-Process -Name chrome,tshark -Force -ErrorAction SilentlyContinue
$env:SSLKEYLOGFILE = "$SharkRoot\ssl_keys.log"
Start-Process chrome "https://skillmachine.net"

# 2. THE FILTER (Based on your HAR Analysis)
# client_seed hex: 63:6c:69:65:6e:74:5f:73:65:65:64
# multiplier hex:  6d:75:6c:74:69:70:6c:69:65:72

Write-Host "[*] SURGICAL SNIFFER ACTIVE." -F Red
Write-Host "    Targeting confirmed signatures from HAR file." -F Gray

# We pipe to a file to decouple the process and prevent pipe crashes
& "C:\Program Files\Wireshark\tshark.exe" -i 8 -o "tls.keylog_file:$SharkRoot\ssl_keys.log" -Y "frame contains 63:6c:69:65:6e:74:5f:73:65:65:64 or frame contains 6d:75:6c:74:69:70:6c:69:65:72" -x -l > $Buffer
