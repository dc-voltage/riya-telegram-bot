#!/bin/bash
# ================================================================
# DC VOLTAGE - Jio AirFiber 6J11 Failsafe Flasher (Linux / macOS)
# Official GitHub: https://github.com/dc-voltage
# Telegram: https://t.me/JIo_Airtel_Unlock
# ================================================================

ROUTER_IP=${1:-"192.168.31.1"}
echo "=== DC VOLTAGE Jio 6111 Linux Flasher ==="
echo "[*] Target Router IP: $ROUTER_IP"

if ! ping -c 1 "$ROUTER_IP" >/dev/null 2>&1; then
    echo "[-] Cannot reach router at $ROUTER_IP. Check Ethernet cable!"
    exit 1
fi
echo "[+] Connection to $ROUTER_IP verified!"

echo "Enabling LuCI web interface & killing TR-069..."
ssh -o StrictHostKeyChecking=no root@"$ROUTER_IP" "
    /etc/init.d/uhttpd enable && /etc/init.d/uhttpd start
    /etc/init.d/tr069 stop && /etc/init.d/tr069 disable
    uci set tr069.state.enable=0 2>/dev/null
    uci commit 2>/dev/null
"

echo "[+] Success! Native LuCI is now active on http://$ROUTER_IP"
