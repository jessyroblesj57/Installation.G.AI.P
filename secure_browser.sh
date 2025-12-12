#!/bin/bash

# ==============================================================================
# SECURE BROWSER LAUNCHER (VPN + Docker Isolation + Randomization)
# ==============================================================================
#
# Purpose: Launches a Firefox instance inside a Docker container that is
#          strictly routed through a VPN container (Gluetun).
#          Randomizes container identity on every launch.
#
# Usage:   sudo ./secure_browser.sh <path_to_vpn_config.ovpn>
# ==============================================================================

# --- 1. Checks & Setup ---


if [[ -z "$1" ]]; then
    echo "Usage: sudo ./secure_browser.sh <path_to_vpn_config.ovpn>"
    exit 1
fi

# Get the absolute path and the specific filename
VPN_FILE=$(realpath "$1")
VPN_FILENAME=$(basename "$VPN_FILE")
VPN_DIR=$(dirname "$VPN_FILE")

# Debug output for troubleshooting
echo "[DEBUG] VPN_FILE: $VPN_FILE"
echo "[DEBUG] VPN_FILENAME: $VPN_FILENAME"
echo "[DEBUG] VPN_DIR: $VPN_DIR"

BROWSER_PORT=3000
CONTAINER_VPN="secure_vpn_gateway"
CONTAINER_BROWSER="secure_firefox_vm"

if [[ ! -f "$VPN_FILE" ]]; then
    echo "[!] Error: VPN file not found at $VPN_FILE"
    exit 1
fi

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "[*] Docker not found. Installing Docker..."
    apt-get update
    apt-get install -y docker.io docker-compose-v2
    systemctl start docker
    systemctl enable docker
fi

# --- 2. Randomization Engine ---

# Generate a random MAC address for the container
generate_mac() {
    printf '02:42:%02X:%02X:%02X:%02X\n' $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256))
}

# Generate a random hostname
generate_hostname() {
    tr -dc 'a-z0-9' < /dev/urandom | head -c 12
}

# Select a random common screen resolution (Blending in is better than true random)
RESOLUTIONS=("1920x1080" "1366x768" "1440x900" "1536x864" "2560x1440")
RAND_INDEX=$(($RANDOM % ${#RESOLUTIONS[@]}))
RAND_RES=${RESOLUTIONS[$RAND_INDEX]}
WIDTH=$(echo $RAND_RES | cut -d'x' -f1)
HEIGHT=$(echo $RAND_RES | cut -d'x' -f2)

RAND_MAC=$(generate_mac)
RAND_HOST=$(generate_hostname)

echo "[*] Generating Random Machine Identity:"
echo "    - Hostname: $RAND_HOST"
echo "    - MAC:      $RAND_MAC"
echo "    - Display:  $WIDTH x $HEIGHT"

# --- 3. Clean Up Old Sessions ---
echo "[*] Cleaning up previous sessions..."
docker rm -f $CONTAINER_BROWSER $CONTAINER_VPN 2>/dev/null || true

# --- 4. Launch VPN Gateway (Gluetun) ---
# We map port 3000 here because the browser will share this network stack.

echo "[*] Starting VPN Gateway (Gluetun)..."


# This is one long line to avoid line-ending issues
docker run -d \
  --name "$CONTAINER_VPN" \
  --mac-address="$RAND_MAC" \
  --hostname="$RAND_HOST" \
  --cap-add=NET_ADMIN \
  --device /dev/net/tun:/dev/net/tun \
  -v "$VPN_DIR:/gluetun" \
  -e VPN_TYPE=openvpn \
  -e VPN_SERVICE_PROVIDER=custom \
  -e OPENVPN_CUSTOM_CONFIG="/gluetun/$VPN_FILENAME" \
  -e OPENVPN_USER="dCSrVNthO4GJ3B4D" \
  -e OPENVPN_PASSWORD="oo2cqeqeqfptT9s3jtMh254FQgPtVWl6" \
  -p "$BROWSER_PORT":3000 \
  qmcgaw/gluetun

echo "[*] Waiting for VPN handshake..."

# --- 5. Verify VPN Connection (Improved) ---

# This loop checks the container logs every 2 seconds for the success message.
# It will time out after 30 seconds to prevent an infinite loop.
for i in {1..15}; do
    LOGS=$(docker logs "$CONTAINER_VPN" 2>&1)
    if echo "$LOGS" | grep -q "You are connected"; then
        echo "[+] VPN Connection Established!"
        break
    fi
    if [[ $i -eq 15 ]]; then
        echo "[!] VPN connection timed out after 30 seconds."
        echo "--- Container Logs ---"
        echo "$LOGS"
        echo "----------------------"
        docker rm -f "$CONTAINER_VPN"
        exit 1
    fi
    sleep 2
done

# If container IS running, check for the external IP
VPN_IP=$(docker exec "$CONTAINER_VPN" wget -qO- https://ipinfo.io/ip)

if [[ -z "$VPN_IP" ]]; then
    echo "[!] VPN IP check failed. Aborting."
    echo "--- Container Logs ---"
    docker logs "$CONTAINER_VPN"
    echo "----------------------"
    docker rm -f "$CONTAINER_VPN"
    exit 1
fi
echo "[+] VPN Connected! Tunnel IP: $VPN_IP"

# --- 6. Launch Browser VM ---
# We route this container's network through the VPN container.

echo "[*] Launching Firefox VM..."

docker run -d \
  --name $CONTAINER_BROWSER \
  --network=container:$CONTAINER_VPN \
  -e PUID=$(id -u) \
  -e PGID=$(id -g) \
  -e CUSTOM_RES_W=$WIDTH \
  -e CUSTOM_RES_H=$HEIGHT \
  --shm-size="2gb" \
  lscr.io/linuxserver/firefox:latest

# --- 7. Instructions ---
echo "========================================================"
echo " [SUCCESS] VM Browser is Running"
echo "========================================================"
echo " 1. Open your physical browser to: http://localhost:$BROWSER_PORT"
echo " 2. You will see a Firefox desktop running inside the VM."
echo " 3. Verify your IP inside that browser; it should match: $VPN_IP"
echo " 4. To stop: docker rm -f $CONTAINER_VPN $CONTAINER_BROWSER"
echo "========================================================"