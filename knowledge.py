"""
Deep Technical Knowledge Base for Router, STB & Network Unlocking.
Official Sources:
- DC VOLTAGE: https://github.com/dc-voltage
- JFC-Group: https://github.com/JFC-Group
"""

GITHUB_BASE = "https://github.com/dc-voltage"
JFC_GITHUB_BASE = "https://github.com/JFC-Group"

REPOSITORIES_DATA = {
    # ==========================================
    # DC VOLTAGE REPOSITORIES
    # ==========================================

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
    },

    # ==========================================
    # JFC-GROUP METHODS & REPOSITORIES
    # (https://github.com/JFC-Group)
    # ==========================================

    # 13. Sercomm JioFiber JCOW414 OpenWrt Port
    "jiofiber_jcow414": {
        "title": "Sercomm JioFiber JCOW414 OpenWrt (Linux Kernel 6.18)",
        "hardware": "EcoNet / Airoha EN7528HU SoC, Dual-Bank Flash Protected",
        "repo_url": f"{JFC_GITHUB_BASE}/jiofiber-jcow414-openwrt",
        "summary": "Full community OpenWrt port (Linux 6.18) with LuCI web administration for Sercomm JioFiber JCOW414.",
        "details": [
            "EcoNet / Airoha EN7528HU platform support with complete Device Tree Source (.dts).",
            "Automated root patch tools and dual-bank failsafe flashing guide.",
            "Bypasses stock Jio restrictions and gives full OpenWrt 23.05+ capabilities."
        ]
    },

    # 14. Housekeeping-PoC (Jio STB 2-Stage Bootloader Unlock Exploit)
    "housekeeping_poc": {
        "title": "Housekeeping-PoC: 2-Stage Bootloader Unlock for Jio STBs",
        "hardware": "JMSC200Av2 on TeleOS 22.1.09, 24.1.39, 25.1.9 (Amlogic ARMv8)",
        "repo_url": f"{JFC_GITHUB_BASE}/Housekeeping-PoC",
        "summary": "Two-stage bootloader unlock and root exploit for Jio STBs.",
        "stages": [
            "Stage 1 (USB Debugging): Fake TR-069 server with GenieACS redirecting acs.oss.jio.com:8443 to set Device.JSTB.USB.USBDebugging=true and disable FOTA.",
            "Stage 2 (Bootloader Unlock): Exploits CVE-2024-31317 (Zygote command injection) to write U-Boot env lock bit (10100000) and set SELinux permissive.",
            "Extracts boot.img for Magisk patching (`pull_boot.sh`)."
        ]
    },

    # 15. JFxploit (JioFiber Router CLI Exploit Toolkit)
    "jfxploit": {
        "title": "JFxploit: JioFiber Router Web Interface Exploit Toolkit",
        "repo_url": f"{JFC_GITHUB_BASE}/JFxploit",
        "summary": "Python CLI toolkit for exploiting web interface vulnerabilities in JioFiber routers.",
        "features": [
            "Multiple RCE injection vectors (pre-auth and post-auth).",
            "Plug-in exploit architecture: auto-tries exploits in order.",
            "Post-exploitation actions: starts telnetd, opens firewall, sets root password, installs persistence.",
            "Custom command injection via `--action custom --cmd`."
        ]
    },

    # 16. JF-Customisation (JioFiber ONT Gateway Customisation & Key Guesser)
    "jf_customisation": {
        "title": "JF-Customisation: JioFiber ONT Gateway Firmwares, Tips & Key Guesser",
        "repo_url": f"{JFC_GITHUB_BASE}/JF-Customisation",
        "summary": "Files, instructions, and tools to customize JioFiber ONT Gateway.",
        "features": [
            "Key Guesser script (`keyguesser.py`) for encrypted router configuration files.",
            "ONT firmware links, recovery steps, and advanced gateway settings.",
            "Tips and tricks for JioFiber router configuration."
        ]
    },

    # 17. AF-Customisation (AirFiber IDU Root & Access)
    "af_customisation": {
        "title": "AF-Customisation: Jio AirFiber IDU Root, UART & UBOOT Access",
        "repo_url": f"{JFC_GITHUB_BASE}/AF-Customisation",
        "summary": "Step-by-step instructions for AirFiber IDU root access, UART serial pins, and UBOOT access.",
        "details": [
            "JAF IDU Root Access on stock and latest firmwares.",
            "Hardware UART access and pinouts.",
            "UBOOT access guides for failsafe recovery."
        ]
    },

    # 18. JioTV Go (Live TV on Web and IPTV)
    "jiotv_go": {
        "title": "JioTV Go: Live TV Channels on Web & IPTV",
        "repo_url": f"{JFC_GITHUB_BASE}/JF-JioTV-Go",
        "summary": "Stream Live TV channels on PC/Browser and IPTV without the JioTV mobile app.",
        "features": [
            "Lightweight web wrapper in Golang utilizing JioTV API.",
            "Generates M3U playlist and EPG XML/JSON for TiviMate, VLC, and IPTV players.",
            "Web interface to watch Live TV on any browser."
        ]
    },

    # 19. JFC-RusTone (JioJoin / Softphone for PC)
    "jfc_rustone": {
        "title": "JFC-RusTone: JioFiber / AirFiber Landline SIP Softphone for PC",
        "repo_url": f"{JFC_GITHUB_BASE}/JFC-RusTone",
        "summary": "Modern SIP softphone that auto-fetches landline credentials from JioFiber/AirFiber router.",
        "features": [
            "Makes your landline number ring and call directly from Windows, macOS, or Linux.",
            "Zero manual SIP configuration — auto-configures from the router.",
            "Replacement for JioJoin app on desktop."
        ]
    },

    # 20. JF-dropbear (Dropbear SSH for JioFiber MIPSEL)
    "jf_dropbear": {
        "title": "JF-dropbear: Lightweight SSH Server for JioFiber (MIPSEL)",
        "repo_url": f"{JFC_GITHUB_BASE}/JF-dropbear",
        "summary": "Precompiled dropbear SSH server and client tools for MIPSEL-based JioFiber routers."
    },

    # 21. Cloudflared for MIPSEL
    "cloudflared_mipsle": {
        "title": "Cloudflared for MIPSEL: Cloudflare Tunnel on JioFiber",
        "repo_url": f"{JFC_GITHUB_BASE}/cloudflared-mipsle",
        "summary": "Run Cloudflare Tunnel client on MIPSEL JioFiber devices for remote access without public IP."
    },

    # 22. JFC-Group Main Organization
    "jfc_group": {
        "title": "JFC-Group JioFiber & AirFiber Methods Hub",
        "repo_url": "https://github.com/JFC-Group",
        "summary": "Collection of JioFiber & AirFiber open-source unlocking, custom firmware, OpenWrt, and automation methods."
    },

    # 23. Jio AirFiber IDU-6401 (Sercomm JIDU6401 / Filogic 830)
    "jidu_6401": {
        "title": "Jio AirFiber IDU-6401 (Sercomm JIDU6401) Official OpenWrt & Superpower Setup",
        "hardware": "MediaTek MT7986A (Filogic 830) Quad-Core Cortex-A53 @ 2.0GHz, Wi-Fi 6 AX6000 4x4 MU-MIMO 160MHz, 512MB DDR4, 256MB SPI-NAND",
        "repo_url": f"{GITHUB_BASE}/Jio-AirFiber-IDU-6401-OpenWrt",
        "ip": "192.168.5.1 (Default OpenWrt: 192.168.1.1, Stock Jio: 192.168.31.1)",
        "credentials": "root / Call@8848 (Default OpenWrt had blank root password)",
        "uboot_bootpass": "!&X@oSCLY5tpz)=<",
        "summary": "Full OpenWrt 25.12.6 flash on Sercomm JIDU6401 with Dual-Zone VPN (LAN 4 + separate VPN Wi-Fi), AdGuard Home adblocker, and RGB LED Heartbeat.",
        "key_superpowers": [
            "MediaTek PPE Hardware Flow Offloading: Multi-gigabit routing at 0-1% CPU load.",
            "Dual-Zone Network Architecture: LAN Port 4 isolated into dedicated bridge `br-vpn` (192.168.40.1) with hardware Kill-Switch.",
            "Dedicated WireGuard VPN Wi-Fi: Separate SSIDs `JioAirFiber_VPN_2.4G` & `JioAirFiber_VPN_5G` routing exclusively through ProtonVPN USA.",
            "Network-Wide AdGuard Home: Running on port 3000, handling DNS on port 53 with encrypted DoH upstreams (Cloudflare, Google, Quad9) and 16MB optimistic RAM cache.",
            "RGB LED Customizer: Blue Heartbeat pulse reflecting CPU load, WAN traffic activity blink, or night stealth mode.",
            "Over 88 MB free writable /overlay flash storage (UBIFS)."
        ],
        "flashing_steps": [
            "Step 1: Backup critical MTD partitions (mtd4 Factory/EEPROM, mtd1 BL2, mtd5 FIP, mtd2 uboot-env, mtd3 MFG, mtd10 Jio-Reserved).",
            "Step 2: Enter U-Boot with bootpass `!&X@oSCLY5tpz)=<`.",
            "Step 3: Bypass U-Boot signature enforcement: `fdt addr $(fdtcontroladdr); fdt rm /signature; bootm 0x46000000`.",
            "Step 4: Format /dev/mtd6 (ubi2) and write initramfs factory UBI.",
            "Step 5: Boot OpenWrt RAM stage and flash permanent `sysupgrade.bin` via `sysupgrade -n /tmp/sysupgrade.bin`."
        ],
        "critical_troubleshooting": [
            "Android 'No Internet' on VPN Wi-Fi: Caused by table 100 missing the local subnet return route. Solved by adding `ip rule add to 192.168.40.0/24 lookup main priority 90` and DHCP option 6 pointing to 192.168.40.1.",
            "5GHz DFS Radar Freeze: Setting Channel 36 to HE160 overlaps DFS channels 52-64. Set to HE80 (UNII-1 36-48 non-DFS) for instantaneous broadcast.",
            "TCP Handshake / Webpage Hangs over WireGuard: Enable TCP MSS Clamping on zone vpn (`mtu_fix=1`) and set WireGuard MTU to 1360."
        ]
    }
}

# Aliases for quick lookup
REPOSITORIES_DATA["jio_stb"] = REPOSITORIES_DATA["jmsc200a"]
REPOSITORIES_DATA["genieacs"] = REPOSITORIES_DATA["genieacs_windows"]
REPOSITORIES_DATA["cwmp"] = REPOSITORIES_DATA["genieacs_windows"]
REPOSITORIES_DATA["tr069"] = REPOSITORIES_DATA["genieacs_windows"]

# JFC Aliases
REPOSITORIES_DATA["jcow414"] = REPOSITORIES_DATA["jiofiber_jcow414"]
REPOSITORIES_DATA["jcow"] = REPOSITORIES_DATA["jiofiber_jcow414"]
REPOSITORIES_DATA["jiofiber"] = REPOSITORIES_DATA["jiofiber_jcow414"]
REPOSITORIES_DATA["housekeeping"] = REPOSITORIES_DATA["housekeeping_poc"]
REPOSITORIES_DATA["bootloader_unlock"] = REPOSITORIES_DATA["housekeeping_poc"]
REPOSITORIES_DATA["jiotv"] = REPOSITORIES_DATA["jiotv_go"]
REPOSITORIES_DATA["jiotv_go"] = REPOSITORIES_DATA["jiotv_go"]
REPOSITORIES_DATA["rustone"] = REPOSITORIES_DATA["jfc_rustone"]
REPOSITORIES_DATA["jfc"] = REPOSITORIES_DATA["jfc_group"]
REPOSITORIES_DATA["jfc_group"] = REPOSITORIES_DATA["jfc_group"]

# Jio AirFiber IDU-6401 Aliases
REPOSITORIES_DATA["jidu6401"] = REPOSITORIES_DATA["jidu_6401"]
REPOSITORIES_DATA["idu6401"] = REPOSITORIES_DATA["jidu_6401"]
REPOSITORIES_DATA["6401"] = REPOSITORIES_DATA["jidu_6401"]
REPOSITORIES_DATA["jio_6401"] = REPOSITORIES_DATA["jidu_6401"]
REPOSITORIES_DATA["filogic830"] = REPOSITORIES_DATA["jidu_6401"]
REPOSITORIES_DATA["jidu6j01"] = REPOSITORIES_DATA["jidu_6401"]
REPOSITORIES_DATA["sercomm_6401"] = REPOSITORIES_DATA["jidu_6401"]

GUIDES = REPOSITORIES_DATA
REPOSITORIES = REPOSITORIES_DATA
