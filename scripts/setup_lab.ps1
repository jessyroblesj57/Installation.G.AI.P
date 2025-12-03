# ==========================================
# Gemini Lab Environment Setup Script
# ==========================================

$ProjectRoot = "C:\Gemini"
$RepoDir = Join-Path $ProjectRoot "data\repos"

# 1. Prepare Directory Structure
Write-Host "[*] Checking directory structure..." -ForegroundColor Cyan
if (!(Test-Path $RepoDir)) {
    New-Item -ItemType Directory -Force -Path $RepoDir | Out-Null
    Write-Host "    Created $RepoDir" -ForegroundColor Green
} else {
    Write-Host "    Repo directory exists." -ForegroundColor Gray
}

# 2. Clone Repositories
# We use a hashtable to map folder names to URLs
$Repos = @{
    "awesome-canbus" = "https://github.com/iDoka/awesome-canbus.git";
    "python-can"     = "https://github.com/hardbyte/python-can.git";
    "ICSim"          = "https://github.com/zombieCraig/ICSim.git";
    "arp-scan"       = "https://github.com/royhills/arp-scan.git";
    "lazygit"        = "https://github.com/jesseduffield/lazygit.git";
}

Write-Host "`n[*] Cloning Repositories into $RepoDir..." -ForegroundColor Cyan
foreach ($name in $Repos.Keys) {
    $path = Join-Path $RepoDir $name
    if (!(Test-Path $path)) {
        Write-Host "    Cloning $name..." -ForegroundColor Yellow
        git clone $Repos[$name] $path
    } else {
        Write-Host "    $name already exists. Skipping." -ForegroundColor DarkGray
    }
}

# 3. Install Gemini Extensions
# These must be installed via the Gemini CLI command
Write-Host "`n[*] Installing Gemini Extensions..." -ForegroundColor Cyan

# List of extensions to install
$Extensions = @(
    "https://github.com/gemini-cli-extensions/jules",
    "https://github.com/gemini-cli-extensions/packet-buddy"
)

foreach ($ext in $Extensions) {
    Write-Host "    Installing $ext..." -ForegroundColor Yellow
    # We use --auto-update to ensure you stay current
    gemini extensions install $ext --auto-update
}

# 4. Install Utility Tools (Optional but Recommended)
Write-Host "`n[*] Checking for Utility Tools (Winget)..." -ForegroundColor Cyan

function Install-Tool ($toolId) {
    if (winget list -q $toolId) {
        Write-Host "    $toolId is already installed." -ForegroundColor DarkGray
    } else {
        Write-Host "    Installing $toolId..." -ForegroundColor Magenta
        winget install --id $toolId -e --source winget
    }
}

# You can comment these out if you don't want them automatically installed
Install-Tool "JesseDuffield.Lazygit"
Install-Tool "junegunn.fzf"
Install-Tool "DylanAraps.Neofetch"

Write-Host "`n[✓] Setup Complete! Your lab is ready at $RepoDir" -ForegroundColor Green
Write-Host "    To use Jules, type: /jules in your Gemini CLI."
