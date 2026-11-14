#!/usr/bin/env python3
"""
DC VOLTAGE - Jio STB (JMSD200A / JMSC200A) Automated Debloater
GitHub: https://github.com/dc-voltage
Telegram: https://t.me/JIo_Airtel_Unlock
"""
import sys
import subprocess

BLOATWARE_PACKAGES = [
    "com.jio.tr069client",
    "com.jio.teleos.watchdog",
    "com.jio.media.ondemand",
    "com.jio.jioplay.tv",
    "com.jio.teleos.analytics",
    "com.jio.fota",
]

def run_adb(device_ip, cmd):
    full_cmd = f"adb -s {device_ip}:5555 shell {cmd}"
    res = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    return res.stdout.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 auto_debloater.py <STB_IP>")
        sys.exit(1)

    ip = sys.argv[1]
    print(f"[*] Connecting to Jio STB at {ip}:5555...")
    subprocess.run(f"adb connect {ip}:5555", shell=True)

    print("[*] Neutralizing TR-069 & Watchdog auto-shutdown...")
    for pkg in BLOATWARE_PACKAGES:
        print(f"[-] Disabling: {pkg}")
        run_adb(ip, f"pm disable-user --user 0 {pkg}")

    print("[*] Speeding up UI (0.5x animations)...")
    run_adb(ip, "settings put global window_animation_scale 0.5")
    run_adb(ip, "settings put global transition_animation_scale 0.5")
    run_adb(ip, "settings put global animator_duration_scale 0.5")

    print("[+] STB Debloat & 20-min Shutdown Watchdog Neutralized Successfully!")
    print("[*] Unhide Android TV Settings: adb shell am start -n com.android.tv.settings/.MainSettings")

if __name__ == "__main__":
    main()
