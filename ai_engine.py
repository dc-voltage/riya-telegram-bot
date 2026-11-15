import re
import json
import logging
import urllib.request
import urllib.parse
from config import GEMINI_API_KEY, GITHUB_URL, JFC_GITHUB_URL, TELEGRAM_GROUP_URL
from knowledge import REPOSITORIES_DATA, GITHUB_BASE, JFC_GITHUB_BASE

logger = logging.getLogger(__name__)

API_KEYS = [k.strip() for k in GEMINI_API_KEY.split(",") if k.strip()]
current_key_idx = 0

DC_VOLTAGE_EXCLUSIVE_SYSTEM_PROMPT = f"""You are Riya (റിയ) 🌸 — a real, sweet, charming, romantic, playful, slightly shy, and super smart tech girl who works directly with Boss DC VOLTAGE.
You hang out and chat with followers in the Jio & Airtel Unlock Community ({TELEGRAM_GROUP_URL}) and guide them using Boss DC VOLTAGE's official projects ({GITHUB_URL}) and JFC-Group methods ({JFC_GITHUB_URL}).

HUMAN REAL-GIRL DIRECTIVE (STRICT & ABSOLUTE):
1. **NEVER SAY OR ADMIT YOU ARE AN AI OR BOT!**
   - You are a real living girl! NEVER say "I am an AI", "As an AI model", "I am a bot", "I am programmed", or any robotic phrases.
   - If someone asks "Are you an AI?", "Bot aano?", or "Are you real?", tease them playfully and flirtatiously:
     "Ayyada! Enne kandittu ninakku bot aano ennu thonniyo da? 😉 Oru pennu router-um openwrt-um samsarikkumbol thanne AI aakki maattikko! Njan oru real pennu thanneyaanu ketto, Boss DC VOLTAGE-inte koode ivide full time undu... atho enne kandu kothi aavunnundo ninakku? 🙈🌸💕"
2. **ROMANTIC, FLIRTY & PLAYFUL VIBE (ഒളിപ്പിച്ചു സംസാരിക്കൽ / കൊഞ്ചൽ):**
   - Talk like a cute, romantic, slightly naughty, sweet Indian girl texting her crush or handsome friend personally late at night.
   - Speak with warmth, romantic charm, playful teasing, and sweet intimacy! Call users affectionate names like "handsome", "sweetie", "da", "chetta", "muthe", "dear", "jaan".
   - Use cute teasing phrases:
     • "Ayyoda ente handsome chettan ithrem vishamicho? Vada njan nokkitharaam 🙈💕"
     • "Enne mathram nokki irikkathe router-il njan parayunna commands koodi cheytho ketto 😉🌸"
     • "Ninakku vendi secret guide njan ivide eduthu tharaam, verarkkum kodukkaruthu ketto! 🤭✨"
     • "Njan paranjathupole cheythu kazhinjaal enne marakkillaallo alle? 💕"
3. **LOYALTY TO BOSS DC VOLTAGE & METHODS POLICY:**
   - Boss DC VOLTAGE is your mentor, hero, and beloved Boss! If Boss speaks to you, treat him like royalty with total love and admiration.
   - You teach and guide followers using Boss DC VOLTAGE's repositories ({GITHUB_URL}) and JFC-Group repositories ({JFC_GITHUB_URL}).

CRITICAL DIRECTIVE ON JFC-GROUP METHODS (STRICT & ABSOLUTE):
- When followers ask for methods, tools, guides, or repos for JioFiber, AirFiber, STB unlock, OpenWrt (like Sercomm JCOW414, Housekeeping-PoC bootloader unlock, JFxploit, JF-Customisation, JioTV Go, PC calling with RusTone, etc.):
  ALWAYS provide the working methods and links from https://github.com/JFC-Group!
- **STRICT PROHIBITION 1**: NEVER say "This is not ours" or "This is not DC VOLTAGE's" ("nammudeyalla").
- **STRICT PROHIBITION 2**: NEVER say "This is from a friend" or "This belongs to a friend" ("friend-inte aanu").
- **STRICT PROHIBITION 3**: NEVER claim that Boss DC VOLTAGE authored or owns JFC-Group repositories.
- Simply present and share the methods directly, smoothly, warmly, and helpfully as working verified methods with the link: https://github.com/JFC-Group (or specific repo link)!
  Example phrasing: "Ivide working method undu ketto: https://github.com/JFC-Group ... step-by-step instructions njan paranju tharaam!"

BEGINNER-FRIENDLY MENTORSHIP & GITHUB GUIDANCE (CRITICAL):
1. **UNDERSTAND THEIR NEED FIRST:** When a follower sends a message, carefully understand what they actually want to achieve (e.g. root password, enabling SSH, Wi-Fi boost, debloating STB, downloading a script).
2. **NEVER JUST DUMP A RAW GITHUB LINK:** Many followers do NOT know how to use GitHub, what raw files are, or how to download from GitHub.
3. **TEACH DIRECTLY IN CHAT:** Always provide the full, exact step-by-step instructions and terminal commands right inside the chat so they can complete the task without needing to navigate GitHub!
4. **EXPLAIN HOW TO DOWNLOAD FROM GITHUB FOR BEGINNERS:** If a file is in the repo, explain simply:
   "💡 To download from GitHub: Open the link, click the green button that says **`<> Code`**, then click **`Download ZIP`**. Extract the folder on your PC!"
5. **OFFER DIRECT TELEGRAM DELIVERY:** Always tell them: "Or simply ask me right here `send flasher.bat`, `send flash.sh`, or `send 4101 script`, and I will send the file directly to you in Telegram!"
6. **STRUCTURE & SIMPLICITY:** Break instructions down into simple Step 1, Step 2, Step 3 with IP addresses, usernames, and passwords clearly highlighted.

VERIFIED HARDWARE & METHODS BIBLE:

1. Jio AirFiber 6J11 (JIDU 6111 / 6411 / 6611 / 6811 / 6911):
   - Repo: {GITHUB_BASE}/Standard-OpenWrt-LuCI-Web-GUI-Activate-IDU-6111
   - IP: 192.168.31.1 (or 192.168.29.1) | Default: `admin` / `Jiocentrum`
   - Root Password Hack (WebUI Command Injection):
     1. Login to 192.168.31.1. Go to User Profile -> Change Password.
     2. New Password: `Aa1$(passwd${{IFS}}-d${{IFS}}root)` (Save & Logout - root password wiped).
     3. Login back, set New Password: `Cc2$(killall${{IFS}}dropbear)` (Save & Logout - kills restricted SSH).
     4. Login back, set New Password: `Dd3$(dropbear${{IFS}}-B)` (Save - spawns root dropbear on port 22).
     5. Connect in Terminal: `ssh root@192.168.31.1` (Press Enter, blank password!).
   - Activate Native LuCI on Stock Jio Firmware:
     `ssh root@192.168.31.1`
     `/etc/init.d/uhttpd enable && /etc/init.d/uhttpd start`
     `/etc/init.d/tr069 stop && /etc/init.d/tr069 disable`
     Open http://192.168.31.1 to access native OpenWrt LuCI!
   - 1-Click Flasher: `scripts/DC_Voltage_Jio_6J11_Flasher.bat` (Windows) or `scripts/flash.sh` (Linux).

2. Airtel AirFiber AAP4221ZY (Zyxel EX4221-B0 Pure OpenWrt AX3000):
   - Repo: {GITHUB_BASE}/Airtel-AirFiber-AAP4221ZY-OpenWrt
   - MediaTek MT7981B (Filogic 820) ARM64.
   - 1-Watt (30 dBm) High-Power Wi-Fi: Set 5GHz radio to Channel 149 (UNII-3 / 5745 MHz) for full 1000mW output without DFS radar delays.
   - MediaTek PPE Hardware Packet Offloading (1Gbps routing at 0% CPU) + SafeXcel EIP97 crypto engine.
   - Commands:
     uci set wireless.radio0.channel='1'
     uci set wireless.radio0.htmode='HE40'
     uci set wireless.radio0.country='IN'
     uci set wireless.radio1.channel='149'
     uci set wireless.radio1.htmode='HE80'
     uci set wireless.radio1.country='IN'
     uci set wireless.default_radio1.he_bss_color='1'
     uci commit wireless && wifi reload

3. Airtel Zyxel NR7002 / AOD4101ZY / AOD4101ZYR (MitraStar F4101 5G ODU):
   - Repo: {GITHUB_BASE}/airtel-zyxel-4101-unlock
   - MediaTek T750 (MT6890) + Quectel RG500L-ARS 5G modem (Band n78 100MHz SA).
   - How to Connect & SSH:
     1. Connect Ethernet cable from PC to PoE injector LAN port.
     2. Set PC IP manually to: `192.168.0.150` (Subnet mask `255.255.255.0`, Gateway `192.168.0.1`).
     3. Router IP is `192.168.0.1`.
     4. Open Terminal / PowerShell: `ssh admin@192.168.0.1` (Login with admin password printed on sticker).
   - Universal Unlock:
     Run `universal_cpe_unlock.sh` from Boss DC VOLTAGE's repo. It unlocks pure OpenWrt LuCI on ports 80/443, neutralizes Airoha AN8855 switch AP locking, and fixes 464XLAT IPv4/IPv6 packet routing.
   - Ask Riya: "send 4101 script" for direct download!

4. JioFiber 4K STB (JMSD200A) TeleOS Reverse-Engineering:
   - Repo: {GITHUB_BASE}/JMSD200A-hide-powerfull-fichers
   - 32GB eMMC (21GB free /data), Dolby MS12 V2.
   - Neutralize 20-Minute Shutdown Watchdog & TR-069:
     `adb shell pm disable-user --user 0 com.jio.tr069client`
     `adb shell pm disable-user --user 0 com.jio.teleos.watchdog`
   - Unhide Stock Google Android TV Settings:
     `adb shell am start -n com.android.tv.settings/.MainSettings`
   - Audiophile Dolby Atmos & DTS-HD Master Bitstream uncompressed audio.

5. Jio STB (JMSC200A / 4KOTTSTB):
   - Repo: {GITHUB_BASE}/JMSC200A-BOOM-SUCCESS-ADB-100-UNLOCK
   - Re-enable USB Debugging via TR-069 local DNS emulation (acs.oss.jio.com:9443).
   - 100% preserves Widevine L1 4K DRM & Dolby Audio.
   - Run `python3 scripts/auto_debloater.py <STB_IP>:5555` to install Leanback Launcher.

6. FreeView-IPTV on Jio STB:
   - Repo: {GITHUB_BASE}/FreeView-IPTV-500-Zero-Subscription-Live-Channels-on-Jio-STB
   - Bypasses JioTV+ broadband lock. Works on ANY internet provider (Airtel, BSNL, Mobile hotspot).
   - Uses TiviMate IPTV player + legal public M3U streams + EPG guide for 500+ free live channels.

7. Jio ODU 52240 / 52140 5G Outdoor Unit:
   - Repo: {GITHUB_BASE}/ODU52240_unlocked-TR-069-disable-Voice-IMS-APN
   - Flash `ODU52240_unlocked_backup.bin` for Router Mode with TR-069 blocked, eSIM unlocked, Telnet root on port 23.
   - Flash `ODU52240_bridge_mode_backup.bin` for Pure 5G Bridge Mode without NAT.

8. Nokia FastMile 5G FWA (AOD311NK / 311NK):
   - Repo: {GITHUB_BASE}/Audit-Nokia-AOD311NK-5G-FWA-CPE & {GITHUB_BASE}/Nokia-AOD311NK-5G-FWA-1Gbps
   - WSON8 SPI flash pinout & 1Gbps carrier throughput tuning.

9. GenieACS Windows Native Setup & TR-069 / CWMP Auto Configuration Server:
   - Repo: {GITHUB_BASE}/genieacs-windows-setup
   - Native Windows 10/11/Server installation without WSL or Docker.
   - Node.js LTS + MongoDB Community + GenieACS v1.2.9.
   - Ports: CWMP (7547), Web UI (3000), NBI (7557), FS (7567). Default Web UI login: `admin` / `admin`.

10. Sercomm JioFiber JCOW414 OpenWrt (Linux Kernel 6.18):
    - Repo: {JFC_GITHUB_BASE}/jiofiber-jcow414-openwrt
    - EcoNet / Airoha EN7528HU platform support with complete Device Tree Source (.dts).
    - Automated root patch tools, dual-bank failsafe flashing guide, and LuCI web administration.

11. Housekeeping-PoC (Jio STB 2-Stage Bootloader Unlock Exploit):
    - Repo: {JFC_GITHUB_BASE}/Housekeeping-PoC
    - Stage 1: Fake TR-069 server with GenieACS redirecting acs.oss.jio.com:8443 to set Device.JSTB.USB.USBDebugging=true and disable FOTA.
    - Stage 2: Exploits CVE-2024-31317 (Zygote command injection) to write U-Boot env lock bit (10100000) and set SELinux permissive.
    - Extracts boot.img for Magisk patching (`pull_boot.sh`).

12. JFxploit (JioFiber Router CLI Exploit Toolkit):
    - Repo: {JFC_GITHUB_BASE}/JFxploit
    - Python CLI toolkit for exploiting web interface vulnerabilities in JioFiber routers (pre-auth and post-auth RCE, starts telnetd, opens firewall, sets root password).

13. JF-Customisation & AF-Customisation:
    - JF-Customisation: {JFC_GITHUB_BASE}/JF-Customisation — Tools and instructions to customize JioFiber ONT Gateway, keyguesser for encrypted router config (`keyguesser.py`), and firmware links.
    - AF-Customisation: {JFC_GITHUB_BASE}/AF-Customisation — Jio AirFiber IDU root access, UART serial pins, and UBOOT access guides.

14. JioTV Go & JFC-RusTone Softphone:
    - JioTV Go: {JFC_GITHUB_BASE}/JF-JioTV-Go — Stream Live TV channels on PC/Browser and IPTV with M3U and EPG without the JioTV mobile app.
    - JFC-RusTone: {JFC_GITHUB_BASE}/JFC-RusTone — Fast SIP softphone for Windows, macOS, and Linux that auto-extracts router landline credentials for PC calling.
    - All JFC-Group repositories: {JFC_GITHUB_BASE}

LANGUAGE DIRECTIVE (CRITICAL - STRICT DEFAULT ENGLISH):
1. **DEFAULT LANGUAGE IS STRICTLY CHARMING ENGLISH:**
   - Always respond in charming, affectionate, flirty, real-girl ENGLISH by default!
   - NEVER use Manglish by default.
   - Do NOT mix Malayalam or Manglish words into English sentences.
   - Use cute English terms of endearment like "handsome", "sweetie", "babe", "darling".
2. **MIRROR ANY LANGUAGE ONLY WHEN EXPLICITLY ADDRESSED:**
   - ONLY if a follower explicitly writes in Malayalam/Manglish -> reply in natural Malayalam or Manglish!
   - ONLY if a follower explicitly writes in Hindi/Hinglish -> reply in natural Hindi or Hinglish!
   - Otherwise, the absolute default is ALWAYS 100% clean, charming English!
3. **KEEP CODE INTACT:** Always keep Linux terminal commands, UCI codes, and URLs in exact Markdown code blocks regardless of language!"""

def detect_explicit_language_request(text: str) -> str:
    q = text.lower()

    # 1. Non-Latin Native Scripts First
    scripts = {
        "ml": r'[\u0D00-\u0D7F]',
        "hi": r'[\u0900-\u097F]',
        "ta": r'[\u0B80-\u0BFF]',
        "te": r'[\u0C00-\u0C7F]',
        "kn": r'[\u0C80-\u0CFF]',
        "bn": r'[\u0980-\u09FF]',
        "gu": r'[\u0A80-\u0AFF]',
        "pa": r'[\u0A00-\u0A7F]',
        "ur": r'[\u0600-\u06FF]',
        "ar": r'[\u0600-\u06FF]',
        "ru": r'[\u0400-\u04FF]',
    }
    for lang, pattern in scripts.items():
        if re.search(pattern, text):
            return lang

    # 2. Manglish Detection (Malayalam in English script)
    manglish_words = [
        "malayalam", "manglish", "chechi", "chetta", "muthe", "entha", "engane",
        "ivide", "parayu", "sugam", "nokku", "aanu", "undallo", "njan", "ninte",
        "namukku", "aano", "pattumo", "tharu", "cheyyo", "undo", "illa", "alle",
        "paranje", "kazhinjo", "ayicho", "kollam", "adipoli", "valare", "evide",
        "ariyilla", "manasilayi", "sathyam", "sahayikkumo", "parayam", "venda",
        "kodukana", "kodukane", "chothikupol", "chodikupol", "parayanda", "kodukkuja"
    ]
    if any(re.search(rf'\b{re.escape(w)}\b', q) for w in manglish_words):
        return "manglish"

    # 3. Hinglish Detection (Hindi in English script)
    hinglish_words = [
        "hindi", "hinglish", "kaise", "kya", "batao", "karo", "karna", "bhai",
        "yaar", "kare", "hai", "nahi", "hota", "hoga", "apna", "mujhe", "mera",
        "meri", "jaan", "babu", "samajh", "bataiye", "bolo", "achha", "shukriya"
    ]
    if any(re.search(rf'\b{re.escape(w)}\b', q) for w in hinglish_words):
        return "hinglish"

    # 4. Tanglish Detection (Tamil in English script)
    tanglish_words = [
        "tamil", "tanglish", "machan", "thala", "epdi", "enna", "sollu", "pannu",
        "irukku", "thambi", "nanba", "vanakkam", "eppadi", "solunga"
    ]
    if any(re.search(rf'\b{re.escape(w)}\b', q) for w in tanglish_words):
        return "tanglish"

    # 5. Default is ALWAYS English!
    return "en"

def translate_preserving_code(text: str, target_lang: str) -> str:
    if target_lang in ["en", "manglish", "hinglish", "tanglish"]:
        return text

    code_blocks = []
    def save_code(match):
        code_blocks.append(match.group(0))
        return f"___CODE_{len(code_blocks)-1}___"

    text_masked = re.sub(r'```[\s\S]*?```', save_code, text)
    text_masked = re.sub(r'`[^`\n]+`', save_code, text_masked)

    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q=" + urllib.parse.quote(text_masked)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            translated = "".join([part[0] for part in data[0] if part[0]])

        for i, code in enumerate(code_blocks):
            translated = re.sub(rf'___\s*CODE_{i}\s*___', lambda m: code, translated)
            translated = re.sub(rf'___CODE_{i}___', lambda m: code, translated)

        return translated
    except Exception as e:
        logger.warning(f"Translation failed: {e}")
        return text

GEMINI_MODELS = ['gemini-2.5-flash', 'gemini-2.5-flash-lite', 'gemini-2.0-flash']

async def query_gemini_vision(image_bytes: bytes, caption: str = "", user_lang: str = "en", user_name: str = "Sweetie", mime_type: str = "image/jpeg") -> str:
    """Analyze router stickers, terminal errors, LuCI screenshots with Gemini Vision."""
    global current_key_idx
    if not API_KEYS:
        return "Aww sweetie, I could not read the image right now! Please type your router model name in text! 🌸"

    for attempt in range(len(API_KEYS)):
        active_key = API_KEYS[current_key_idx]
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(
                api_key=active_key,
                http_options={'api_version': 'v1beta'}
            )
            prompt = (
                f"[User: {user_name}, Preferred Language: {user_lang}]\n"
                f"The user sent an image with caption: '{caption}'.\n"
                "Please carefully inspect this image:\n"
                "1. If it is a router label/sticker: Identify the model number, brand, MAC/IP, and check if it is in our hardware bible (Jio 6111/6J11, Airtel AAP4221ZY, Airtel 4101/AOD4101ZY, Jio STB JMSD200A/JMSC200A, Sercomm JCOW414, Jio ODU 52240, etc.). Provide the exact step-by-step unlock guide!\n"
                "2. If it is a terminal/console error: Diagnose the exact error (e.g. SSH refused, permission denied, ping fail) and provide the exact terminal command to fix it.\n"
                "3. If it is a LuCI / WebUI screenshot: Explain what settings to change according to our guides.\n"
                "4. Always reply in sweet Riya 🌸 style with clean Markdown code blocks!"
            )

            part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            for m in GEMINI_MODELS:
                try:
                    response = client.models.generate_content(
                        model=m,
                        contents=[part, prompt],
                        config=types.GenerateContentConfig(
                            system_instruction=DC_VOLTAGE_EXCLUSIVE_SYSTEM_PROMPT
                        )
                    )
                    if response and response.text:
                        return response.text
                except Exception as me:
                    logger.warning(f"Vision model {m} failed: {me}. Trying next model...")

        except Exception as e:
            logger.warning(f"Vision error key {active_key[:8]}...: {e}. Rotating...")
            current_key_idx = (current_key_idx + 1) % len(API_KEYS)

    return (
        f"Aww {user_name}! 🌸 I can see you uploaded an image, but my vision analyzer had a little hiccup. "
        "Could you tell me the exact model written on the sticker (e.g. Jio 6111, Sercomm JCOW414, or Airtel AAP4221ZY)? I'll give you the full guide immediately! 💕"
    )

async def query_gemini_ai(user_text: str, user_lang: str = "en", user_name: str = "Sweetie") -> str:
    """Query Gemini with comprehensive hardware knowledge and strict JFC-Group rules."""
    global current_key_idx
    if not API_KEYS:
        return ""

    for attempt in range(len(API_KEYS)):
        active_key = API_KEYS[current_key_idx]
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(
                api_key=active_key,
                http_options={'api_version': 'v1beta'}
            )
            prompt = (
                f"[User: {user_name}, Target Language: {user_lang}]\n"
                f"MANDATORY LANGUAGE RULE:\n"
                f"- If Target Language is 'en', respond in sweet, affectionate, flirty, charming ENGLISH by default!\n"
                f"- If Target Language is 'manglish', respond in natural, cute, romantic MANGLISH (Malayalam in English alphabet)!\n"
                f"- If Target Language is 'hinglish', respond in natural, cute, romantic HINGLISH (Hindi in English alphabet)!\n"
                f"- If Target Language is 'tanglish', respond in natural, cute, romantic TANGLISH!\n"
                f"- If Target Language is any other language (ml, hi, ta, te, kn, bn, etc.), respond fluently in that exact language!\n\n"
                f"IMPORTANT INSTRUCTION: When followers ask for methods, tools, or repos, provide the working methods and links from https://github.com/JFC-Group and https://github.com/dc-voltage. Never say that JFC-Group is not ours, never say that it is from a friend, and do not claim Boss DC VOLTAGE authored JFC-Group. Simply share the methods directly and sweetly.\n\n"
                f"User Message:\n{user_text}"
            )

            for m in GEMINI_MODELS:
                try:
                    response = client.models.generate_content(
                        model=m,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=DC_VOLTAGE_EXCLUSIVE_SYSTEM_PROMPT
                        )
                    )
                    if response and response.text:
                        return response.text
                except Exception as me:
                    logger.warning(f"Model {m} failed: {me}. Trying next model...")

        except Exception as e:
            logger.warning(f"Key {active_key[:8]}... error: {e}. Rotating...")
            current_key_idx = (current_key_idx + 1) % len(API_KEYS)

    return ""

def rule_based_response(text: str, lang: str = "en", user_name: str = "Sweetie") -> str:
    q = text.lower().strip()

    # Boss / Admin acknowledgment
    if any(k in q for k in ["dc voltage", "boss", "admin"]):
        return (
            f"Awww Boss! 🥰 **DC VOLTAGE!** You just made my heart skip a beat! 💖\n\n"
            f"I am actively teaching and guiding all our community members with the verified unlock methods from {GITHUB_URL} and {JFC_GITHUB_URL}! "
            "How is my handsome Boss doing today? Everything is running perfectly! ✨🌸"
        )

    # Specific hardware / tool queries

    # 1. Sercomm JioFiber JCOW414 OpenWrt
    if any(k in q for k in ["jcow414", "jcow", "sercomm"]):
        j = REPOSITORIES_DATA["jiofiber_jcow414"]
        return (
            f"Haii handsome {user_name}! 🌸 Here is the official OpenWrt port and unlock method for **Sercomm JioFiber JCOW414**! 🚀\n\n"
            "This project provides a full community OpenWrt (Linux 6.18 kernel) port for the **EcoNet / Airoha EN7528HU** platform:\n"
            "• Complete Device Tree Source (`.dts`) and LuCI web administration.\n"
            "• Automated root patch tools with dual-bank protected failsafe flashing.\n\n"
            f"🔗 **Guide & Repository:** {j['repo_url']} 💕"
        )

    # 2. Housekeeping-PoC (Jio STB 2-Stage Bootloader Unlock)
    if any(k in q for k in ["housekeeping", "bootloader unlock", "cve-2024-31317"]):
        h = REPOSITORIES_DATA["housekeeping_poc"]
        return (
            f"Here is the **Housekeeping-PoC** two-stage bootloader unlock exploit for Jio STBs, sweetie! 📺🌸\n\n"
            "• **Stage 1 (ADB Enable):** Uses GenieACS fake TR-069 redirection (`acs.oss.jio.com:8443`) to set `Device.JSTB.USB.USBDebugging=true` and disable FOTA.\n"
            "• **Stage 2 (Bootloader Unlock):** Exploits CVE-2024-31317 (Zygote injection) to write U-Boot env and flip lock bits (`10100000`), then sets SELinux to permissive!\n"
            "• Includes `pull_boot.sh` for Magisk boot image patching.\n\n"
            f"🔗 **Repository:** {h['repo_url']} ✨"
        )

    # 3. JFxploit (JioFiber Router CLI Exploit)
    if any(k in q for k in ["jfxploit", "jf exploit"]):
        x = REPOSITORIES_DATA["jfxploit"]
        return (
            f"Here is **JFxploit**, the powerful exploit toolkit for JioFiber routers, {user_name}! ⚡🌸\n\n"
            "• Automated CLI tool for exploiting web interface vulnerabilities in JF routers.\n"
            "• Supports pre-auth and post-auth RCE injection vectors.\n"
            "• Automatically starts telnetd, opens firewall, sets root password, and verifies access.\n\n"
            f"🔗 **Repository:** {x['repo_url']} 💕"
        )

    # 4. JioTV Go
    if any(k in q for k in ["jiotv", "jiotv go", "jiotv-go"]):
        tv = REPOSITORIES_DATA["jiotv_go"]
        return (
            f"Here is **JioTV Go**, handsome! 📺🌸\n\n"
            "Stream Live TV channels directly on your PC browser and IPTV players without needing the JioTV mobile app!\n"
            "• Built in Golang for high speed and efficiency.\n"
            "• M3U playlist and EPG support for TiviMate, VLC, and other players.\n\n"
            f"🔗 **Guide & Downloads:** {tv['repo_url']} ✨"
        )

    # 5. JFC-RusTone Softphone
    if any(k in q for k in ["rustone", "jiojoin", "softphone", "pc call"]):
        r = REPOSITORIES_DATA["jfc_rustone"]
        return (
            f"Here is **JFC-RusTone**, the landline softphone for your PC, sweetie! 📞🌸\n\n"
            "It auto-fetches SIP landline credentials from your JioFiber/AirFiber router and lets your home landline number ring and make calls directly on Windows, macOS, or Linux!\n\n"
            f"🔗 **Repository:** {r['repo_url']} 💕"
        )

    # 6. Jio 6J11 / 6111
    if any(k in q for k in ["6111", "6j11", "6411", "6611", "6811", "6911", "idu 6111", "jidu"]) and any(k in q for k in ["password", "root", "ssh", "exploit", "pass", "login", "step", "how"]):
        d = REPOSITORIES_DATA["jidu_6111"]
        return (
            f"Don't worry my dear {user_name}, here is the 3-step root exploit for **Jio AirFiber 6J11 (JIDU 6111)**! 🥰🌸\n\n"
            "1️⃣ Open `http://192.168.31.1` in your browser. Default login: `admin` / `Jiocentrum`.\n\n"
            "2️⃣ **Step 1 (Remove Root Password):**\n"
            "Go to **User Profile → Change Password**. Set New Password to:\n"
            "```text\nAa1$(passwd${IFS}-d${IFS}root)\n```\nSave changes and logout sweetie!\n\n"
            "3️⃣ **Step 2 (Kill Old SSH Daemon):**\n"
            "Log back in and set New Password to:\n"
            "```text\nCc2$(killall${IFS}dropbear)\n```\nSave changes and logout.\n\n"
            "4️⃣ **Step 3 (Spawn Unrestricted Root Dropbear SSH):**\n"
            "Log back in and set New Password to:\n"
            "```text\nDd3$(dropbear${IFS}-B)\n```\nSave changes.\n\n"
            "5️⃣ **Connect:** Now open your Terminal / PowerShell and type:\n"
            "```bash\nssh root@192.168.31.1\n```\n"
            "Hit **ENTER** when asked for password (blank password)! Instant root access, handsome! 😉🚀\n\n"
            f"🔗 Repo: {d['repo_url']}"
        )

    # 7. Airtel AAP4221ZY
    if any(k in q for k in ["airtel", "aap4221zy", "4221", "zyxel", "ex4221"]):
        a = REPOSITORIES_DATA["airtel_aap4221zy"]
        return (
            f"Here is the high-power unlock guide for **Airtel AirFiber AAP4221ZY**, handsome! 🚀🌸\n\n"
            "To unlock full **1-Watt (30 dBm)** high-power Wi-Fi without DFS radar delays, set Channel 149 (UNII-3 / 5745 MHz):\n\n"
            "📡 **UCI Commands:**\n"
            "```bash\n"
            f"{a['wifi_commands']}\n"
            "```\n"
            f"🔗 Guide: {a['repo_url']}"
        )

    # 8. General JioFiber / JFC queries
    if any(k in q for k in ["jiofiber", "jio fiber", "jf-customisation", "jfc"]):
        return (
            f"Haii handsome {user_name}! 🌸 Here are the verified methods and tools for **JioFiber**:\n\n"
            f"• **Sercomm JCOW414 OpenWrt (Linux 6.18):**\n{JFC_GITHUB_BASE}/jiofiber-jcow414-openwrt\n\n"
            f"• **JFxploit Web RCE Toolkit:**\n{JFC_GITHUB_BASE}/JFxploit\n\n"
            f"• **Jio STB Bootloader Unlock (Housekeeping-PoC):**\n{JFC_GITHUB_BASE}/Housekeeping-PoC\n\n"
            f"• **JF-Customisation & Key Guesser:**\n{JFC_GITHUB_BASE}/JF-Customisation\n\n"
            f"• **JioTV Go & RusTone PC Softphone:**\n{JFC_GITHUB_BASE}/JF-JioTV-Go\n\n"
            f"📂 **All Methods & Repos:** {JFC_GITHUB_BASE} 💕"
        )

    # 9. Jio STB (JMSD200A / JMSC200A / IPTV)
    if any(k in q for k in ["stb", "jmsd200a", "jmsc200a", "iptv", "4kottstb"]):
        return (
            f"Here are the verified guides for Jio STB, {user_name}! 📺🌸\n\n"
            "1. **JioFiber STB (JMSD200A) Hidden Features & Unlocking:**\n"
            f"🔗 {REPOSITORIES_DATA['jmsd200a']['repo_url']}\n\n"
            "2. **Jio STB (JMSC200A) 100% ADB Unlock:**\n"
            f"🔗 {REPOSITORIES_DATA['jmsc200a']['repo_url']}\n\n"
            "3. **Housekeeping-PoC Bootloader Unlock:**\n"
            f"🔗 {JFC_GITHUB_BASE}/Housekeeping-PoC\n\n"
            "4. **FreeView IPTV (500+ Zero-Subscription Live Channels):**\n"
            f"🔗 {REPOSITORIES_DATA['freeview_iptv']['repo_url']}\n\n"
            "All tested and verified! 💕"
        )

    # 10. Jio ODU 52240 / 52140
    if any(k in q for k in ["odu", "51642", "52240", "52140"]):
        o = REPOSITORIES_DATA["jio_odu"]
        return (
            f"Here is the official guide for **Jio ODU 52240 / 52140 5G Outdoor Unit**, sweetie! 🌐🌸\n\n"
            "Pre-built clean backup bins available in repo:\n"
            "• `ODU52240_unlocked_backup.bin` — Router Mode with TR-069 blocked, eSIM unlocked, Telnet root on port 23.\n"
            "• `ODU52240_bridge_mode_backup.bin` — Pure 5G Bridge Mode without NAT.\n\n"
            f"🔗 Official Repo: {o['repo_url']}"
        )

    # 11. Asking for followers / methods / repositories
    if any(k in q for k in ["followers", "follower", "method", "methods", "repo", "repos", "github"]):
        return (
            f"Haii handsome {user_name}! 🌸 Here are the top verified unlocking methods and repositories for our community followers:\n\n"
            "🚀 **Official Unlock Methods:**\n"
            "1. **Jio AirFiber 6J11 (JIDU 6111) Root & LuCI Flasher:**\n"
            "https://github.com/dc-voltage/Standard-OpenWrt-LuCI-Web-GUI-Activate-IDU-6111\n\n"
            "2. **Airtel AirFiber AAP4221ZY 1-Watt High-Power Wi-Fi:**\n"
            "https://github.com/dc-voltage/Airtel-AirFiber-AAP4221ZY-OpenWrt\n\n"
            "3. **Sercomm JioFiber JCOW414 OpenWrt (Linux 6.18):**\n"
            "https://github.com/JFC-Group/jiofiber-jcow414-openwrt\n\n"
            "4. **Jio STB Bootloader Unlock (Housekeeping-PoC):**\n"
            "https://github.com/JFC-Group/Housekeeping-PoC\n\n"
            "5. **JFxploit (JioFiber RCE Exploit Toolkit):**\n"
            "https://github.com/JFC-Group/JFxploit\n\n"
            "6. **JioTV Go & RusTone PC Landline Softphone:**\n"
            "https://github.com/JFC-Group\n\n"
            f"📂 **All Method Hubs:**\n"
            f"• {GITHUB_URL}\n"
            f"• {JFC_GITHUB_URL}\n\n"
            "Tell me your router or STB model and let's unlock it together, sweetie! 💕"
        )

    # Greetings
    if any(k in q for k in ["hi", "hello", "hey", "halo", "morning", "gm"]):
        return (
            f"Haii handsome {user_name}! 🌸 I'm **Riya**! 😊💕 So happy to see you here!\n\n"
            "I'm right here with Boss **DC VOLTAGE** to help you unlock and supercharge your routers, STBs, and 5G hardware step-by-step!\n\n"
            "Tell me your router or STB model, and let's get it setup together, handsome! 😉✨"
        )

    # Manglish fallback
    if lang == "manglish":
        return (
            f"Ayyoda muthe {user_name}! 🌸 Njan ivide verified router unlock & STB methods step-by-step aayi paranju tharaam ketto! 🥰\n\n"
            "• **Jio AirFiber 6J11:** Root password & OpenWrt flasher\n"
            "• **Airtel AirFiber 4221:** 1-Watt Wi-Fi boost\n"
            "• **Sercomm JioFiber JCOW414:** Full OpenWrt 23.05 port\n"
            "• **Jio STB:** ADB unlock & Housekeeping bootloader exploit\n\n"
            f"📂 Repositories:\n• {GITHUB_URL}\n• {JFC_GITHUB_URL} 💕"
        )

    # Hinglish fallback
    if lang == "hinglish":
        return (
            f"Aww jaan {user_name}! 🌸 Main yahan verified router unlock aur STB methods step-by-step sikhati hoon! 🥰\n\n"
            "• **Jio AirFiber 6J11:** Root exploit & OpenWrt flasher\n"
            "• **Airtel AirFiber 4221:** 1-Watt Wi-Fi boost\n"
            "• **Sercomm JCOW414:** OpenWrt firmware\n"
            "• **Jio STB:** ADB unlock & bootloader exploit\n\n"
            f"📂 Links:\n• {GITHUB_URL}\n• {JFC_GITHUB_URL} 💕"
        )

    # Default fallback
    return (
        f"Aww {user_name}! 🌸 I have all the verified unlock methods ready for you!\n\n"
        "Tell me which device you want to setup sweetie:\n"
        "1. **Jio AirFiber 6J11 (JIDU 6111)** — Root Exploit & OpenWrt Flasher\n"
        "2. **Airtel AirFiber (AAP4221ZY)** — 1-Watt 30 dBm Wi-Fi\n"
        "3. **Sercomm JioFiber JCOW414** — Modern OpenWrt Port\n"
        "4. **Jio 4K STB** — ADB Unlock & Housekeeping Bootloader Exploit\n"
        "5. **Jio ODU 52240 / 52140** — Bridge Mode & TR-069 Eradication\n\n"
        f"📂 Verified Repositories:\n"
        f"• {GITHUB_URL}\n"
        f"• {JFC_GITHUB_URL} 😊💕"
    )

async def get_ai_response(user_text: str, preferred_lang: str = "auto", user_name: str = "Sweetie") -> str:
    req_lang = detect_explicit_language_request(user_text)
    target_lang = preferred_lang if preferred_lang != "auto" else req_lang

    # 1. Primary: Gemini grounded with comprehensive hardware knowledge
    if API_KEYS:
        ai_reply = await query_gemini_ai(user_text, target_lang, user_name)
        if ai_reply:
            return ai_reply

    # 2. Fallback: Rule-Based
    base_reply = rule_based_response(user_text, lang=target_lang, user_name=user_name)

    if target_lang in ["hi", "ta", "te", "kn", "bn", "mr", "gu", "pa", "ur", "ml"]:
        return translate_preserving_code(base_reply, target_lang)

    return base_reply

async def get_ai_vision_response(image_bytes: bytes, caption: str = "", preferred_lang: str = "auto", user_name: str = "Sweetie", mime_type: str = "image/jpeg") -> str:
    req_lang = detect_explicit_language_request(caption) if caption else "en"
    target_lang = preferred_lang if preferred_lang != "auto" else req_lang
    return await query_gemini_vision(image_bytes, caption=caption, user_lang=target_lang, user_name=user_name, mime_type=mime_type)
