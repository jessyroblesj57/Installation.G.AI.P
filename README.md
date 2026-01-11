# Installation.G.AI.P
A Windows installation program for simple Google AI Programs. Built by Gem for Gem.

## Surgical Sniffer Tools
This repository contains PowerShell scripts for analyzing `skillmachine.net` traffic on Windows.

### Prerequisites
1.  **Windows OS** (PowerShell 5.1 or Core)
2.  **Wireshark** installed at `C:\Program Files\Wireshark\`
3.  **Google Chrome** installed
4.  Create the directory `C:\shark` before running the scripts.

### Usage
1.  Run **`surgical_sniffer.ps1`** as Administrator to start capturing traffic. This will launch Chrome and begin logging to `C:\shark\live_stream.txt`.
2.  Run **`surgical_hud.ps1`** in a separate PowerShell window to monitor the feed and display round results (Seed/Multiplier).
