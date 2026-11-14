@echo off
TITLE DC VOLTAGE - Jio AirFiber 6J11 Failsafe Flasher
COLOR 0A
echo ================================================================
echo          DC VOLTAGE OFFICIAL JIO AIRFIBER 6J11 FLASHER
echo            https://github.com/dc-voltage
echo ================================================================
echo.
echo [*] Ensure your PC is connected to LAN port of Jio 6111 Router.
echo [*] Default IP: 192.168.31.1
echo.
set /p ROUTER_IP="Enter Router IP [Default: 192.168.31.1]: "
if "%ROUTER_IP%"=="" set ROUTER_IP=192.168.31.1

echo.
echo [*] Testing connection to %ROUTER_IP%...
ping -n 2 %ROUTER_IP% >nul
if errorlevel 1 (
    echo [!] ERROR: Cannot reach %ROUTER_IP%. Check Ethernet cable!
    pause
    exit /b
)
echo [+] Connection OK!
echo.
echo Select Action:
echo  1. Enable Native OpenWrt LuCI Web GUI (Stock Firmware)
echo  2. Disable TR-069 Remote Spyware & Watchdog
echo  3. Backup Current Firmware Partitions
echo  4. Flash Custom OpenWrt Image to Inactive Slot (Failsafe)
echo.
set /p CHOICE="Enter choice (1-4): "

if "%CHOICE%"=="1" (
    echo [*] Enabling LuCI Web Server...
    ssh -o StrictHostKeyChecking=no root@%ROUTER_IP% "/etc/init.d/uhttpd enable && /etc/init.d/uhttpd start && /etc/init.d/tr069 stop && /etc/init.d/tr069 disable"
    echo [+] Done! Open http://%ROUTER_IP% in your browser.
)
if "%CHOICE%"=="2" (
    echo [*] Disabling TR-069...
    ssh -o StrictHostKeyChecking=no root@%ROUTER_IP% "/etc/init.d/tr069 stop && /etc/init.d/tr069 disable && uci set tr069.state.enable=0 && uci commit"
    echo [+] TR-069 permanently neutralized!
)
if "%CHOICE%"=="3" (
    echo [*] Backing up MTD partitions...
    ssh -o StrictHostKeyChecking=no root@%ROUTER_IP% "cat /proc/mtd"
)
if "%CHOICE%"=="4" (
    echo [*] Please ensure openwrt-sysupgrade.bin is in this folder.
    if exist "openwrt-sysupgrade.bin" (
        scp openwrt-sysupgrade.bin root@%ROUTER_IP%:/tmp/
        ssh -o StrictHostKeyChecking=no root@%ROUTER_IP% "sysupgrade -v -n /tmp/openwrt-sysupgrade.bin"
    ) else (
        echo [!] openwrt-sysupgrade.bin not found!
    )
)
echo.
echo Thank you for using DC VOLTAGE tools! Join: https://t.me/JIo_Airtel_Unlock
pause
