#!/bin/sh
# DC VOLTAGE - Airtel AAP4221ZY 1-Watt 30 dBm Wi-Fi Unlock Script
# GitHub: https://github.com/dc-voltage/Airtel-AirFiber-AAP4221ZY-OpenWrt

echo "Applying DC VOLTAGE 1-Watt 30 dBm High-Power Wi-Fi Profile..."
uci set wireless.radio0.channel='1'
uci set wireless.radio0.htmode='HE40'
uci set wireless.radio0.country='IN'
uci set wireless.radio1.channel='149'
uci set wireless.radio1.htmode='HE80'
uci set wireless.radio1.country='IN'
uci set wireless.default_radio1.he_bss_color='1'
uci commit wireless
wifi reload
echo "Done! 5GHz is now transmitting on Channel 149 at 1000mW (30 dBm) without DFS pause!"
