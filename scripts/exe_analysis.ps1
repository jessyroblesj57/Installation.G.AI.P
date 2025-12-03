<#
.SYNOPSIS
    Analyzes Windows Executable (EXE) files.

.DESCRIPTION
    This script performs basic analysis on a target executable file,
    including calculating file hash, retrieving version information,
    and checking digital signatures.

.PARAMETER FilePath
    The path to the executable file to analyze.

.EXAMPLE
    .\exe_analysis.ps1 -FilePath "C:\Windows\System32\notepad.exe"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

if (-not (Test-Path $FilePath)) {
    Write-Error "File not found: $FilePath"
    exit 1
}

$fileItem = Get-Item $FilePath

Write-Host "--- Executable Analysis ---"
Write-Host "File: $($fileItem.FullName)"
Write-Host "Size: $($fileItem.Length) bytes"
Write-Host "Created: $($fileItem.CreationTime)"

# Calculate Hash
Write-Host "`n[Calculating SHA256 Hash...]"
try {
    $hash = Get-FileHash -Path $FilePath -Algorithm SHA256
    Write-Host "SHA256: $($hash.Hash)"
} catch {
    Write-Warning "Could not calculate hash."
}

# Version Info
Write-Host "`n[Version Information]"
try {
    $versionInfo = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($FilePath)
    Write-Host "File Version: $($versionInfo.FileVersion)"
    Write-Host "Product Version: $($versionInfo.ProductVersion)"
    Write-Host "Company Name: $($versionInfo.CompanyName)"
    Write-Host "Description: $($versionInfo.FileDescription)"
} catch {
    Write-Warning "Could not retrieve version info."
}

# Digital Signature (Basic Check)
Write-Host "`n[Digital Signature]"
try {
    $sig = Get-AuthenticodeSignature -FilePath $FilePath
    Write-Host "Status: $($sig.Status)"
    if ($sig.SignerCertificate) {
        Write-Host "Signer: $($sig.SignerCertificate.Subject)"
    }
} catch {
    Write-Warning "Could not check signature (cmdlet might not be available)."
}

Write-Host "`nAnalysis Complete."
