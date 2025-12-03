<#
.SYNOPSIS
    Performs basic network analysis and diagnostics.

.DESCRIPTION
    This script gathers local network adapter information, checks connectivity
    to specific targets, and displays active TCP connections.

.PARAMETER Target
    A hostname or IP address to ping (default: google.com).

.EXAMPLE
    .\network_analysis.ps1 -Target "8.8.8.8"
#>

param(
    [string]$Target = "google.com"
)

Write-Host "--- Network Analysis Foundation ---"
Write-Host "Time: $(Get-Date)"

# 1. Local Interface Info
Write-Host "`n[Local Network Interfaces]"
try {
    # Using CIM/WMI if Get-NetAdapter is not available or for broader compatibility
    $adapters = Get-CimInstance -ClassName Win32_NetworkAdapterConfiguration | Where-Object { $_.IPEnabled -eq $true }
    foreach ($adapter in $adapters) {
        Write-Host "Adapter: $($adapter.Description)"
        Write-Host "  MAC: $($adapter.MACAddress)"
        Write-Host "  IP: $($adapter.IPAddress -join ', ')"
        Write-Host "  Gateway: $($adapter.DefaultIPGateway -join ', ')"
    }
} catch {
    Write-Warning "Could not retrieve adapter info via CIM. Trying standard ipconfig..."
    ipconfig
}

# 2. Connectivity Check
Write-Host "`n[Connectivity Check]"
Write-Host "Pinging $Target..."
try {
    $ping = Test-Connection -ComputerName $Target -Count 4 -ErrorAction Stop
    Write-Host "  Response Time: $($ping.ResponseTime) ms"
    Write-Host "  Status: Success"
} catch {
    Write-Warning "  Ping failed to $Target"
}

# 3. Active Connections (Netstat wrapper)
Write-Host "`n[Active TCP Connections (Top 5)]"
try {
    # Get-NetTCPConnection is modern, but 'netstat' is universal
    if (Get-Command Get-NetTCPConnection -ErrorAction SilentlyContinue) {
        Get-NetTCPConnection -State Established | Select-Object -First 5 | Format-Table -AutoSize
    } else {
        netstat -an | Select-Object -First 10
    }
} catch {
    Write-Error "Error retrieving connections: $_"
}

Write-Host "`nNetwork Analysis Complete."
