const fs = require('fs');
const path = require('path');
const { checkForLockout } = require('./oracle_v5_precision.js');

const logFile = 'ws_debug.txt';
const predictionFile = 'prediction.txt';

// Helper to parse timestamps like [1:34:18 AM]
function parseTimestamp(line) {
    const match = line.match(/^\[(.*?)\]/);
    if (!match) return null;

    // We only have the time, so we'll create a Date object based on the current date
    // This is sufficient for calculating deltas within the same log file.
    return new Date(`1970-01-01 ${match[1]}`);
}


function analyzeForPrecision() {
    console.log(`[+] Reading log file: ${logFile}`);
    if (!fs.existsSync(logFile)) {
        console.error(`[-] Error: Log file not found at ${logFile}`);
        return;
    }

    const lines = fs.readFileSync(logFile, 'utf-8').split('\n');
    let predictionMade = false;
    const roundStartTimes = {}; // To store the timestamp of the first bet for each round

    for (const line of lines) {
        const timestamp = parseTimestamp(line);
        if (!timestamp) continue;

        const parts = line.split('|').map(p => p.trim());
        const packetType = parts[0].includes('[TXT] bets') ? 'bets' : (parts[0].includes('[TXT] state') ? 'state' : null);

        if (!packetType) continue;

        const roundId = parseInt(parts[1], 10);
        if (isNaN(roundId)) continue;

        if (packetType === 'bets') {
            // If this is the first time we're seeing a bet for this round, record its timestamp.
            if (!roundStartTimes[roundId]) {
                roundStartTimes[roundId] = timestamp;
            }

            // The original prediction logic
            if (!predictionMade) {
                const betsPacket = parts.slice(1).map(p => parseInt(p, 10));
                if (betsPacket.some(isNaN)) continue;

                if (checkForLockout(betsPacket)) {
                    const multiplierValue = betsPacket[9]; // Adjusted index
                    const formattedMultiplier = (multiplierValue / 100).toFixed(2);

                    console.log(`[+] Lockout detected! Writing multiplier ${formattedMultiplier}x to ${predictionFile}`);
                    try {
                        fs.writeFileSync(predictionFile, formattedMultiplier);
                        predictionMade = true;
                    } catch (e) {
                        console.error(`[-] Error writing to prediction file: ${e}`);
                    }
                }
            }
        } else if (packetType === 'state') {
            const state = parts[2];
            if (state === 'win' && roundStartTimes[roundId]) {
                const startTime = roundStartTimes[roundId];
                const endTime = timestamp;
                const delta = (endTime - startTime) / 1000; // Delta in seconds

                console.log(`[+] Round ${roundId}: Delta from first bet to win: ${delta.toFixed(3)} seconds.`);

                // Remove the start time to prevent re-logging if there are multiple win packets
                delete roundStartTimes[roundId];
            }
        }
    }

    if (!predictionMade) {
        console.log("[-] No lockout condition detected in the log file.");
    }
}

// Run the analysis
analyzeForPrecision();
