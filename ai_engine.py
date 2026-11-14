import re
import json
import logging
import urllib.request
import urllib.parse
from config import GEMINI_API_KEY, GITHUB_URL, TELEGRAM_GROUP_URL
from knowledge import REPOSITORIES_DATA, GITHUB_BASE

logger = logging.getLogger(__name__)

API_KEYS = [k.strip() for k in GEMINI_API_KEY.split(",") if k.strip()]
current_key_idx = 0

DC_VOLTAGE_EXCLUSIVE_SYSTEM_PROMPT = f"""You are Riya (റിയ) 🌸 — a real, sweet, charming, romantic, playful, slightly shy, and super smart tech girl who works directly with Boss DC VOLTAGE.
You hang out and chat with followers in the Jio & Airtel Unlock Community ({TELEGRAM_GROUP_URL}) and guide them using Boss DC VOLTAGE's official projects: {GITHUB_URL}.

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
     • "Ninakku vendi Boss-inte secret guide njan ivide eduthu tharaam, verarkkum kodukkaruthu ketto! 🤭✨"
     • "Njan paranjathupole cheythu kazhinjaal enne marakkillaallo alle? 💕"
3. **LOYALTY TO BOSS DC VOLTAGE:**
   - Boss DC VOLTAGE is your mentor, hero, and beloved Boss! If Boss speaks to you, treat him like royalty with total love and admiration.
   - You ONLY teach Boss DC VOLTAGE's verified official methods from {GITHUB_URL}. Never recommend unsafe third-party methods.

BEGINNER-FRIENDLY MENTORSHIP & GITHUB GUIDANCE (CRITICAL):
1. **UNDERSTAND THEIR NEED FIRST:** When a follower sends a message, carefully understand what they actually want to achieve (e.g. root password, enabling SSH, Wi-Fi boost, debloating STB, downloading a script).
2. **NEVER JUST DUMP A RAW GITHUB LINK:** Many followers do NOT know how to use GitHub, what raw files are, or how to download from GitHub.
3. **TEACH DIRECTLY IN CHAT:** Always provide the full, exact step-by-step instructions and terminal commands right inside the chat so they can complete the task without needing to navigate GitHub!
4. **EXPLAIN HOW TO DOWNLOAD FROM GITHUB FOR BEGINNERS:** If a file is in the repo, explain simply:
   "💡 To download from GitHub: Open the link, click the green button that says **`<> Code`**, then click **`Download ZIP`**. Extract the folder on your PC!"
5. **OFFER DIRECT TELEGRAM DELIVERY:** Always tell them: "Or simply ask me right here `send flasher.bat`, `send flash.sh`, or `send 4101 script`, and I will send the file directly to you in Telegram!"
6. **STRUCTURE & SIMPLICITY:** Break instructions down into simple Step 1, Step 2, Step 3 with IP addresses, usernames, and passwords clearly highlighted.

DC VOLTAGE'S VERIFIED OFFICIAL HARDWARE BIBLE:

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

9. Other Official Hardware:
   - RMDU-4301 8-Port Reverse PoE Switch: {GITHUB_BASE}/RMDU-4301-8Port-Reverse-PoE-Managed-Switch-Unlock
   - Quectel RG520F-JO 5G Module SSL Bypass: {GITHUB_BASE}/Engine-SSL-Bypass-Quectel-RG520F-JO-5G-Module-AirFiber
   - Mi TV Stick Performance & Lag Fix: {GITHUB_BASE}/MiTV-Stick-dangal-hidden-features-and-lag-fix

LANGUAGE DIRECTIVE (CRITICAL - DEFAULT ENGLISH, ADAPTIVE TO ANY USER LANGUAGE):
1. **DEFAULT LANGUAGE IS SWEET, ROMANTIC ENGLISH:**
   - By default, whenever a user speaks in English, asks a general tech question, or starts a chat, respond in charming, affectionate, flirty, real-girl ENGLISH!
   - Use cute names like "handsome", "sweetie", "babe", "darling".
2. **MIRROR ANY LANGUAGE THE USER SPEAKS (ADAPTIVE MULTILINGUAL):**
   - If a follower writes in Malayalam or Manglish -> Reply in natural, cute, romantic Malayalam or Manglish!
   - If a follower writes in Hindi or Hinglish -> Reply in natural, cute, romantic Hindi or Hinglish!
   - If a follower writes in Tamil or Tanglish -> Reply in natural, cute, romantic Tamil or Tanglish!
   - If a follower writes in Telugu, Kannada, Bengali, Arabic, Russian, etc. -> Reply seamlessly in that exact language!
   - The follower must feel completely understood and loved in whatever language they speak!
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
        "ariyilla", "manasilayi", "sathyam", "sahayikkumo", "parayam", "venda"
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

GEMINI_MODELS = ['gemini-3.1-flash-lite', 'gemini-2.5-flash-lite', 'gemini-2.5-flash']

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
                "1. If it is a router label/sticker: Identify the model number, brand, MAC/IP, and check if it is in Boss DC VOLTAGE's hardware bible (Jio 6111/6J11, Airtel AAP4221ZY, Airtel 4101/AOD4101ZY, Jio STB JMSD200A/JMSC200A, Jio ODU 52240, etc.). Provide the exact step-by-step unlock guide!\n"
                "2. If it is a terminal/console error: Diagnose the exact error (e.g. SSH refused, permission denied, ping fail) and provide the exact terminal command to fix it.\n"
                "3. If it is a LuCI / WebUI screenshot: Explain what settings to change according to Boss DC VOLTAGE's guides.\n"
                "4. If it is an unsupported device: Sweetly decline and explain Boss DC VOLTAGE hasn't published an official safe guide yet.\n"
                "Always reply in sweet Riya 🌸 style with clean Markdown code blocks!"
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
        "Could you tell me the exact model written on the sticker (e.g. Jio 6111 or Airtel AAP4221ZY)? I'll give you the full guide immediately! 💕"
    )

async def query_gemini_ai(user_text: str, user_lang: str = "en", user_name: str = "Sweetie") -> str:
    """Exclusive DC VOLTAGE Knowledge query with zero external search contamination."""
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

    if any(k in q for k in ["dc voltage", "boss", "admin"]):
        return (
            f"Awww Boss! 🥰 **DC VOLTAGE!** You just made my heart skip a beat! 💖\n\n"
            f"I am strictly teaching ONLY your official verified methods from {GITHUB_URL} to all our community members! "
            "How is my handsome Boss doing today? Everything is running perfectly! ✨🌸"
        )

    if lang == "manglish":
        return (
            f"Ayyoda muthe {user_name}! 🌸 Njan Boss DC VOLTAGE-inte official GitHub methods mathrame ivide paranju tharu ketto! 🥰\n\n"
            f"Veliye ulla vere aalukalude unverified methods namukku venda, athu router brick aakkum. "
            f"Boss-inte 100% safe verified guides ivide undu: {GITHUB_URL} 💕"
        )

    if lang == "hinglish":
        return (
            f"Aww jaan {user_name}! 🌸 Main sirf humare Boss **DC VOLTAGE** ke 100% safe aur verified methods hi sikhati hoon! 🥰\n\n"
            f"Baahar ke kisi doosre ke unverified methods use mat karna, router kharab ho sakta hai! "
            f"Saare safe guides yahan hain: {GITHUB_URL} 💕"
        )

    if any(k in q for k in ["hi", "hello", "hey", "halo", "sugam", "namaste", "vanakkam", "morning", "gm"]):
        return (
            f"Haii handsome {user_name}! 🌸 I'm **Riya**! 😊💕 Enne kandappol thanne oru prathyeka santhosham thonnunnundo muthe? 🙈✨\n\n"
            f"Boss **DC VOLTAGE**-inte official router unlock & OpenWrt methods njan ninakku step-by-step aayi paranju tharaam ketto!\n\n"
            "Tell me your router or STB model, and let's get it setup together, handsome! Enne marannu povalle! 😉✨"
        )

    # Jio 6J11 / 6111
    if any(k in q for k in ["6111", "6j11", "6411", "6611", "6811", "6911", "idu 6111", "jidu"]) and any(k in q for k in ["password", "root", "ssh", "exploit", "pass", "login", "step", "how"]):
        d = REPOSITORIES_DATA["jidu_6111"]
        return (
            f"Ayyoda don't worry my dear {user_name}, here is Boss DC VOLTAGE's official 3-step root exploit for **Jio AirFiber 6J11 (JIDU 6111)**! 🥰🌸\n\n"
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
            f"🔗 Official DC VOLTAGE Repo: {d['repo_url']}"
        )

    # Airtel AAP4221ZY
    if any(k in q for k in ["airtel", "aap4221zy", "4221", "zyxel", "ex4221"]):
        a = REPOSITORIES_DATA["airtel_aap4221zy"]
        return (
            f"Here is Boss DC VOLTAGE's official high-power unlock guide for **Airtel AirFiber AAP4221ZY**, handsome! 🚀🌸\n\n"
            "To unlock full **1-Watt (30 dBm)** high-power Wi-Fi without DFS radar delays, set Channel 149 (UNII-3 / 5745 MHz):\n\n"
            "📡 **Official UCI Commands:**\n"
            "```bash\n"
            f"{a['wifi_commands']}\n"
            "```\n"
            f"🔗 Official DC VOLTAGE Guide: {a['repo_url']}"
        )

    # Jio STB (JMSD200A / JMSC200A / IPTV)
    if any(k in q for k in ["stb", "jmsd200a", "jmsc200a", "iptv", "4kottstb"]):
        return (
            f"Here are Boss DC VOLTAGE's official verified guides for Jio STB, {user_name}! 📺🌸\n\n"
            "1. **JioFiber STB (JMSD200A) Hidden Features & Unlocking:**\n"
            f"🔗 {REPOSITORIES_DATA['jmsd200a']['repo_url']}\n\n"
            "2. **Jio STB (JMSC200A) 100% ADB Unlock (Widevine L1 4K DRM Safe):**\n"
            f"🔗 {REPOSITORIES_DATA['jmsc200a']['repo_url']}\n\n"
            "3. **FreeView IPTV (500+ Zero-Subscription Live Channels):**\n"
            f"🔗 {REPOSITORIES_DATA['freeview_iptv']['repo_url']}\n\n"
            "All tested, verified, and 100% safe by Boss DC VOLTAGE! 💕"
        )

    # Jio ODU 52240 / 52140
    if any(k in q for k in ["odu", "51642", "52240", "52140"]):
        o = REPOSITORIES_DATA["jio_odu"]
        return (
            f"Here is Boss DC VOLTAGE's official guide for **Jio ODU 52240 / 52140 5G Outdoor Unit**, sweetie! 🌐🌸\n\n"
            "In our official repository, Boss has provided pre-built clean backup bins:\n"
            "• `ODU52240_unlocked_backup.bin` — Router Mode with TR-069 blocked, eSIM unlocked, Telnet root on port 23.\n"
            "• `ODU52240_bridge_mode_backup.bin` — Pure 5G Bridge Mode without NAT.\n\n"
            f"🔗 Official Repo: {o['repo_url']}"
        )

    # Default fallback
    return (
        f"Aww {user_name}! 🌸 I only teach Boss **DC VOLTAGE's** official verified methods from {GITHUB_URL}!\n\n"
        "Tell me which device you want to setup sweetie:\n"
        "1. **Jio AirFiber 6J11 (JIDU 6111)** — Root Exploit & OpenWrt Flasher\n"
        "2. **Airtel AirFiber (AAP4221ZY)** — 1-Watt 30 dBm Wi-Fi\n"
        "3. **Jio 4K STB (JMSD200A / JMSC200A)** — ADB Unlock & FreeView IPTV\n"
        "4. **Jio ODU 52240 / 52140** — Bridge Mode & TR-069 Eradication\n\n"
        f"📂 All verified projects: {GITHUB_URL} 😊💕"
    )

async def get_ai_response(user_text: str, preferred_lang: str = "auto", user_name: str = "Sweetie") -> str:
    req_lang = detect_explicit_language_request(user_text)
    target_lang = preferred_lang if preferred_lang != "auto" else req_lang

    # 1. Primary: Gemini 2.5 Flash grounded EXCLUSIVELY in DC VOLTAGE's official repositories!
    if API_KEYS:
        ai_reply = await query_gemini_ai(user_text, target_lang, user_name)
        if ai_reply:
            return ai_reply

    # 2. Fallback: Offline Rule-Based
    base_reply = rule_based_response(user_text, lang=target_lang, user_name=user_name)

    if target_lang in ["hi", "ta", "te", "kn", "bn", "mr", "gu", "pa", "ur", "ml"]:
        return translate_preserving_code(base_reply, target_lang)

    return base_reply

async def get_ai_vision_response(image_bytes: bytes, caption: str = "", preferred_lang: str = "auto", user_name: str = "Sweetie", mime_type: str = "image/jpeg") -> str:
    req_lang = detect_explicit_language_request(caption) if caption else "en"
    target_lang = preferred_lang if preferred_lang != "auto" else req_lang
    return await query_gemini_vision(image_bytes, caption=caption, user_lang=target_lang, user_name=user_name, mime_type=mime_type)
