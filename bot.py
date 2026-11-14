import logging
import asyncio
import re
import os
import random
from datetime import time, timezone, timedelta
from telegram import Update
from telegram.constants import ParseMode, ChatType
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ChatJoinRequestHandler,
    ContextTypes,
    filters,
)

from config import (
    BOT_TOKEN,
    GITHUB_URL,
    TELEGRAM_GROUP_URL,
    COMMUNITY_CHAT_ID,
    FILES_DIR,
    ADMIN_USER_IDS,
)
from knowledge import GUIDES, REPOSITORIES
from ai_engine import get_ai_response, get_ai_vision_response, translate_preserving_code
from database import init_db, record_user, record_event, get_all_users, get_db_stats
from tts_engine import generate_voice_note

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

SPAM_PATTERNS = [
    r't\.me/(?!JIo_Airtel_Unlock\b|JioUnlockHelper_bot\b)[a-zA-Z0-9_+]+',
    r'(?:binance|forex\s*trading|invest\s*\$|earn\s*\$|crypto\s*signals|free\s*bitcoin)',
    r'(?:join\s*my\s*channel|dm\s*me\s*for\s*earnings|whatsapp\s*\+)',
]

TECH_TIPS = [
    "⚡ **DC VOLTAGE Pro Tip #1 (Jio 6111):** Always disable TR-069 (`/etc/init.d/tr069 stop && /etc/init.d/tr069 disable`) immediately after gaining root. This stops Jio from remotely pushing restrictive firmware updates that lock dropbear! 🌸",
    "🚀 **DC VOLTAGE Pro Tip #2 (Airtel AAP4221ZY):** Switch your 5GHz Wi-Fi to Channel 149 (UNII-3 / 5745 MHz). This unlocks the full 1-Watt (30 dBm) maximum transmit power and avoids DFS radar wait delays! 📡",
    "📺 **DC VOLTAGE Pro Tip #3 (Jio STB JMSD200A):** Set Window, Transition, and Animator scales to 0.5x in Developer Options (`adb shell settings put global window_animation_scale 0.5`) for buttery smooth UI! 🌸",
    "🔥 **DC VOLTAGE Pro Tip #4 (MediaTek MT7981B):** Enable MediaTek PPE hardware flow offloading on OpenWrt to route full 1Gbps gigabit traffic at zero CPU load! ⚡",
    "📺 **DC VOLTAGE Pro Tip #5 (FreeView IPTV):** Pair TiviMate with DC VOLTAGE's legal Indian M3U stream list on your unlocked Jio STB to watch 500+ live HD channels on any broadband! 🌸",
    "🌐 **DC VOLTAGE Pro Tip #6 (OpenWrt Wi-Fi 6):** Enable BSS Coloring (`uci set wireless.default_radio1.he_bss_color='1'`) to eliminate packet collision from neighboring Wi-Fi networks in crowded flats! ✨"
]

async def send_smart_split_message(message, text: str) -> None:
    """Split long responses to prevent Telegram 4096 character limit errors."""
    MAX_LEN = 3500
    if len(text) <= MAX_LEN:
        chunks = [text]
    else:
        chunks = []
        remaining = text
        while remaining:
            if len(remaining) <= MAX_LEN:
                chunks.append(remaining)
                break
            split_idx = remaining.rfind("\n\n", 0, MAX_LEN)
            if split_idx == -1:
                split_idx = remaining.rfind("\n", 0, MAX_LEN)
            if split_idx == -1:
                split_idx = remaining.rfind(" ", 0, MAX_LEN)
            if split_idx == -1:
                split_idx = MAX_LEN
            chunks.append(remaining[:split_idx].strip())
            remaining = remaining[split_idx:].strip()

    for chunk in chunks:
        if not chunk:
            continue
        try:
            await message.reply_text(
                chunk,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.warning(f"Markdown failed ({e}), sending plain text...")
            await message.reply_text(chunk, disable_web_page_preview=True)

async def delete_after_delay(msg, delay: int = 15):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except Exception:
        pass

async def is_sender_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user = update.effective_user
    if not user:
        return False
    if user.id in ADMIN_USER_IDS:
        return True
    chat = update.effective_chat
    if chat and chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        try:
            admins = await context.bot.get_chat_administrators(chat.id)
            return any(a.user.id == user.id for a in admins)
        except Exception:
            return False
    # If in private chat, check if user is admin in community group
    try:
        member = await context.bot.get_chat_member(COMMUNITY_CHAT_ID, user.id)
        return member.status in ["creator", "administrator"]
    except Exception:
        return False

async def check_and_filter_spam(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if not message or not message.text or not chat:
        return False

    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        if await is_sender_admin(update, context):
            return False

        text = message.text
        for pat in SPAM_PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                logger.warning(f"Spam deleted from {user.first_name} ({user.id}): '{text}'")
                try:
                    await message.delete()
                    warn = await chat.send_message(
                        f"⚠️ Hey {user.first_name}! External channel invites and spam links are not allowed here to keep our DC VOLTAGE group clean and safe! 🌸"
                    )
                    asyncio.create_task(delete_after_delay(warn, 15))
                except Exception as e:
                    logger.warning(f"Error handling spam deletion: {e}")
                return True
    return False

def get_requested_file(text: str):
    q = text.lower()
    if any(k in q for k in ["flasher.bat", "bat flasher", "windows flasher", "6111 flasher", "jio flasher"]):
        fpath = FILES_DIR / "DC_Voltage_Jio_6J11_Flasher.bat"
        if fpath.exists():
            return fpath, "DC_Voltage_Jio_6J11_Flasher.bat", "Jio AirFiber 6111 Windows 1-Click Dual-Slot Flasher 🚀"
    if any(k in q for k in ["flash.sh", "linux flasher", "sh flasher"]):
        fpath = FILES_DIR / "flash.sh"
        if fpath.exists():
            return fpath, "flash.sh", "Jio AirFiber 6111 Linux Bash Flasher 🚀"
    if any(k in q for k in ["m3u", "playlist", "iptv file", "freeview file", "iptv playlist"]):
        fpath = FILES_DIR / "FreeView_IPTV_India.m3u"
        if fpath.exists():
            return fpath, "FreeView_IPTV_India.m3u", "FreeView IPTV India Legal M3U Playlist 📺"
    if any(k in q for k in ["debloater", "debloater script", "stb script", "auto_debloater"]):
        fpath = FILES_DIR / "auto_debloater.py"
        if fpath.exists():
            return fpath, "auto_debloater.py", "Jio STB ADB Automated Debloater Script ⚡"
    if any(k in q for k in ["airtel script", "wifi boost script", "airtel_wifi"]):
        fpath = FILES_DIR / "airtel_wifi_boost.sh"
        if fpath.exists():
            return fpath, "airtel_wifi_boost.sh", "Airtel AAP4221ZY 1-Watt Wi-Fi Boost Script 📡"
    if any(k in q for k in ["4101 script", "universal_cpe", "unlock 4101", "aod4101 script", "zyxel 4101 script", "4101 flasher"]):
        fpath = FILES_DIR / "universal_cpe_unlock.sh"
        if fpath.exists():
            return fpath, "universal_cpe_unlock.sh", "Airtel Zyxel 4101 (AOD4101ZY) Universal Unlock Script 🚀"
    return None, None, None

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    name = user.first_name if user else "Friend"
    record_user(user.id, user.username, name)
    record_event("cmd_start")

    base_text = (
        f"Haii handsome {name}! 🌸 I'm **Riya**! 😊💕\n\n"
        "I'm right here with Boss **DC VOLTAGE** to help you unlock and supercharge your routers, STBs, and 5G hardware!\n\n"
        "🌟 **What I Can Do For You:**\n"
        "• **Step-by-Step Guides:** Ask me your doubt and I'll explain every step with exact commands.\n"
        "• **Send Photos:** Got an error or router sticker? Send me the photo, I'll check it right away! 📸\n"
        "• **Direct Scripts:** Ask for flasher `.bat`, `.sh`, or IPTV files, and I'll send them directly to your chat!\n"
        "• **Sweet Voice Notes:** Want to hear my voice? Just ask for a voice note! 🎙️💕\n\n"
        f"⚡ Boss DC VOLTAGE Official Hub: {GITHUB_URL} 🌸"
    )

    lang = context.user_data.get("lang", "auto")
    if lang in ["hi", "ta", "te", "kn", "bn", "mr", "gu", "pa", "ml"]:
        text = translate_preserving_code(base_text, lang)
    else:
        text = base_text

    if update.message:
        await send_smart_split_message(update.message, text)

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "💡 **Riya Tech Assistant — DC VOLTAGE Official Guides:**\n\n"
        "Just ask your doubts directly, sweetie! Here is what Boss DC VOLTAGE covers:\n\n"
        "• **Jio AirFiber 6J11 (JIDU 6111):** `6111 root password exploit`\n"
        "• **Airtel AirFiber AAP4221ZY:** `airtel 1w wifi boost`\n"
        "• **Jio STB (JMSD200A / JMSC200A):** `stb adb unlock`\n"
        "• **FreeView IPTV:** `freeview iptv 500 channels`\n"
        "• **Jio ODU 52240 / 52140:** `jio odu bridge mode`\n"
        "• **Scripts:** Ask `send flasher.bat` or `send iptv playlist` for direct downloads!\n\n"
        f"📂 All 100% verified repos & scripts: {GITHUB_URL} 🌸"
    )
    if update.message:
        await send_smart_split_message(update.message, text)

async def cmd_techtip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tip = random.choice(TECH_TIPS)
    text = f"🌸 **Riya's Tech Tip!** ⚡\n\n{tip}\n\n🔗 Official Source: {GITHUB_URL}"
    if update.message:
        await send_smart_split_message(update.message, text)

async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await is_sender_admin(update, context):
        await update.message.reply_text("Aww sweetie, this dashboard is only for Boss DC VOLTAGE and admins! 🌸")
        return

    st = get_db_stats()
    text = (
        "👑 **DC VOLTAGE Bot Analytics Dashboard:**\n\n"
        f"👥 **Registered Community Members:** {st['total_users']}\n"
        f"💬 **Text Queries Answered:** {st['text_queries']}\n"
        f"📸 **Photos & Screenshots Analyzed:** {st['image_queries']}\n"
        f"🎙️ **Voice Notes Delivered:** {st['voice_queries']}\n"
        f"⚡ **Total Interactions:** {st['total_events']}\n\n"
        "Everything is running smoothly for Boss! 💖✨"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def cmd_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await is_sender_admin(update, context):
        await update.message.reply_text("Aww sweetie, only Boss DC VOLTAGE can use broadcast! 🌸")
        return

    if not context.args:
        await update.message.reply_text("Usage: `/broadcast <your announcement message>`")
        return

    msg = " ".join(context.args)
    users = get_all_users()
    count = 0
    fail = 0

    await update.message.reply_text(f"🚀 Starting broadcast to {len(users)} community members...")

    broadcast_text = f"📢 **Announcement from DC VOLTAGE** ⚡\n\n{msg}\n\n🌸 Community: {TELEGRAM_GROUP_URL}"

    for user_id, uname in users:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=broadcast_text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            count += 1
            await asyncio.sleep(0.05)
        except Exception:
            fail += 1

    await update.message.reply_text(f"✅ Broadcast complete! Delivered to {count} members (Failed: {fail}).")

async def cmd_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    query = " ".join(context.args) if context.args else "Haii handsome! What can I help you with today?"
    user = update.effective_user
    user_name = user.first_name if user else "Friend"

    record_user(user.id, user.username, user_name)
    record_event("voice_query")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="record_voice")

    ai_reply = await get_ai_response(query, user_name=user_name)
    try:
        voice_file = await generate_voice_note(ai_reply, lang="en")
        with open(voice_file, "rb") as vf:
            await update.message.reply_voice(voice=vf, caption="Riya 🌸")
    except Exception as e:
        logger.warning(f"Voice generation failed: {e}")

    await send_smart_split_message(update.message, ai_reply)

async def handle_photo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.photo:
        return

    user = update.effective_user
    user_name = user.first_name if user else "Friend"
    chat = update.effective_chat
    caption = update.message.caption or ""

    record_user(user.id, user.username, user_name)
    record_event("image_query")

    logger.info(f"[PHOTO] Received photo from {user_name} with caption: '{caption}'")
    await context.bot.send_chat_action(chat_id=chat.id, action="typing")

    try:
        photo_file = await update.message.photo[-1].get_file()
        img_bytes = await photo_file.download_as_bytearray()

        reply = await get_ai_vision_response(bytes(img_bytes), caption=caption, user_name=user_name)
        await send_smart_split_message(update.message, reply)
    except Exception as e:
        logger.error(f"Error handling photo: {e}")
        await update.message.reply_text(
            f"Aww {user_name}! 🌸 I had a little trouble analyzing this photo. "
            "Could you please tell me the router or STB model in text sweetie? 💕"
        )

async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.voice:
        return

    user = update.effective_user
    user_name = user.first_name if user else "Friend"
    chat = update.effective_chat

    record_user(user.id, user.username, user_name)
    record_event("voice_query")

    logger.info(f"[VOICE] Received voice note from {user_name}")
    await context.bot.send_chat_action(chat_id=chat.id, action="record_voice")

    reply_text = (
        f"Aww sweetie {user_name}! 🌸 I heard your voice message! "
        "Type your specific router model (like Jio 6111 or Airtel AAP4221ZY) right here in the chat, "
        "and I will give you the exact step-by-step unlock commands from Boss DC VOLTAGE's verified GitHub guides! 💕"
    )

    try:
        voice_path = await generate_voice_note(reply_text, lang="en")
        with open(voice_path, "rb") as vf:
            await update.message.reply_voice(voice=vf, caption="Riya 🌸")
    except Exception as e:
        logger.warning(f"Voice generation failed: {e}")
        await update.message.reply_text(reply_text)

async def handle_chat_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    join_request = update.chat_join_request
    if not join_request:
        return

    user = join_request.from_user
    user_id = user.id
    user_name = user.first_name or "Friend"
    chat = join_request.chat

    record_user(user_id, user.username, user_name)
    record_event("join_request")

    logger.info(f"[JOIN REQUEST] From {user_name} ({user_id}) for chat '{chat.title}'")

    try:
        await context.bot.approve_chat_join_request(
            chat_id=chat.id,
            user_id=user_id
        )
        logger.info(f"Approved join request for {user_name}")
    except Exception as e:
        logger.warning(f"Could not approve join request for {user_name}: {e}")

    dm_text = (
        f"Haii handsome {user_name}! 🌸 Welcome to the **Jio & Airtel Unlock Community**! 😊✨\n\n"
        "I am Riya, right here with Boss **DC VOLTAGE**! 💕\n\n"
        "Here are the direct links to our official verified guides and automated toolkits:\n\n"
        "⚡ **1. Jio AirFiber 6J11 (JIDU 6111) Root Password & Flasher:**\n"
        f"🔗 [Jio 6111 OpenWrt Guide]({GUIDES['jidu_6111']['repo_url']})\n\n"
        "🚀 **2. Airtel AirFiber AAP4221ZY 1-Watt High-Power Wi-Fi:**\n"
        f"🔗 [Airtel OpenWrt Guide]({GUIDES['airtel_aap4221zy']['repo_url']})\n\n"
        "📺 **3. Jio STB 100% ADB Unlock & FreeView IPTV (500+ Live Channels):**\n"
        f"🔗 [Jio STB ADB Repo]({GUIDES['jio_stb']['repo_url']})\n\n"
        f"📂 **All Tools & Scripts by DC VOLTAGE:**\n{GITHUB_URL}\n\n"
        "Feel free to ask me any technical questions, send error photos, or ask for flasher files right here! 🌸✌️"
    )

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=dm_text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        logger.info(f"Successfully delivered Auto-DM to {user_name}")
    except Exception as e:
        logger.warning(f"Failed to deliver DM to {user_name}: {e}")

async def handle_new_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.new_chat_members:
        return

    chat = update.effective_chat
    service_msg = update.message

    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            welcome_text = (
                "⚡ **DC VOLTAGE COMMUNITY ONLINE** 🌸\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "Haii everyone! I am **Riya** 🌸, right here with Boss **DC VOLTAGE**.\n\n"
                "I am here 24/7 to help you with router unlocking, OpenWrt flashing, "
                "ADB debloating, and network troubleshooting. Just ask your doubts directly! ✨\n\n"
                f"🔗 **Verified Hub:** [github.com/dc-voltage]({GITHUB_URL})\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "*(⏱ Auto-clearing in 12h to keep chat clean)*"
            )
            try:
                sent = await chat.send_message(
                    welcome_text,
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
                asyncio.create_task(delete_after_delay(sent, 12 * 3600))
            except Exception as e:
                logger.warning(f"Failed to send bot join message: {e}")
        else:
            member_name = member.first_name or "Engineer"
            record_user(member.id, member.username, member_name)
            record_event("new_member")

            text = (
                "⚡ **WELCOME TO DC VOLTAGE COMMUNITY** ⚡\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👋 Hello **{member_name}**, welcome aboard!\n\n"
                "🚀 **Official Reverse-Engineering & Unlock Hub:**\n"
                "• **Jio 6J11 (JIDU):** Root Password Injection & LuCI Flasher\n"
                "• **Airtel AAP4221ZY:** 1-Watt 30 dBm Wi-Fi & MTK PPE Offload\n"
                "• **Jio 4K STB:** 100% ADB Unlock & FreeView IPTV (500+ Ch)\n"
                "• **Jio 5G ODU:** TR-069 Eradication & Pure Bridge Mode\n\n"
                "🌸 *I am Riya. Ask any technical doubt or send router photos directly here!*\n\n"
                f"🔗 **Verified Tools:** [github.com/dc-voltage]({GITHUB_URL})\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "*(⏱ Auto-clearing in 12h to keep chat clean)*"
            )
            try:
                sent = await chat.send_message(
                    text,
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
                asyncio.create_task(delete_after_delay(sent, 12 * 3600))
                if service_msg:
                    asyncio.create_task(delete_after_delay(service_msg, 12 * 3600))
            except Exception as e:
                logger.warning(f"Failed to send welcome message: {e}")

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    # Check for group spam
    if await check_and_filter_spam(update, context):
        return

    user_text = update.message.text.strip()
    chat_type = update.message.chat.type
    user = update.effective_user
    user_name = user.first_name if user else "Friend"

    record_user(user.id, user.username, user_name)
    record_event("text_query")

    logger.info(f"[MSG] From {user_name} ({chat_type}): '{user_text}'")

    bot_username = context.bot.username or "JioUnlockHelper_bot"
    clean_text = re.sub(rf'@{bot_username}\b', '', user_text, flags=re.IGNORECASE).strip()
    if not clean_text:
        clean_text = "hi"

    # Check if user requested a downloadable file/script
    file_path, file_name, file_caption = get_requested_file(clean_text)
    if file_path and file_path.exists():
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_document")
        try:
            with open(file_path, "rb") as doc:
                await update.message.reply_document(
                    document=doc,
                    filename=file_name,
                    caption=f"🌸 Here is your file: **{file_caption}**\nCurated by **DC VOLTAGE**: {GITHUB_URL}",
                    parse_mode=ParseMode.MARKDOWN
                )
            logger.info(f"Delivered file {file_name} to {user_name}")
            return
        except Exception as e:
            logger.warning(f"Failed to send document: {e}")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    lang = context.user_data.get("lang", "auto")
    response_text = await get_ai_response(clean_text, preferred_lang=lang, user_name=user_name)

    # Check if user explicitly asked for a voice reply
    wants_voice = any(k in clean_text.lower() for k in [
        "voice message", "voice note", "voice il", "voiceil", "samsariku", "audio tha", "speak to me", "voice send"
    ])

    if wants_voice:
        try:
            voice_file = await generate_voice_note(response_text, lang="en")
            with open(voice_file, "rb") as vf:
                await update.message.reply_voice(voice=vf, caption="Riya 🌸")
        except Exception as e:
            logger.warning(f"Voice generation failed: {e}")

    await send_smart_split_message(update.message, response_text)
    logger.info(f"Replied automatically to {user_name} in {chat_type}")

async def post_daily_tech_tip(context: ContextTypes.DEFAULT_TYPE):
    tip = random.choice(TECH_TIPS)
    try:
        await context.bot.send_message(
            chat_id=COMMUNITY_CHAT_ID,
            text=f"🌸 **Riya's Tech Tip of the Day!** ⚡\n\n{tip}\n\n🔗 Curated with love by **DC VOLTAGE**: {GITHUB_URL}",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        logger.info("Daily tech tip posted successfully.")
    except Exception as e:
        logger.warning(f"Could not post daily tech tip: {e}")

async def post_init_health_server(application) -> None:
    port_str = os.environ.get("PORT")
    if not port_str:
        return
    try:
        from aiohttp import web
        port = int(port_str)
        server = web.Application()
        async def handle_ping(req):
            return web.Response(text="Riya AI Bot for DC VOLTAGE is Online! 🌸⚡")
        server.router.add_get("/", handle_ping)
        server.router.add_get("/health", handle_ping)
        runner = web.AppRunner(server)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        logger.info(f"Render/Cloud HTTP Health Server active on port {port}")
    except Exception as e:
        logger.warning(f"Could not start cloud health server: {e}")

def main() -> None:
    if not BOT_TOKEN:
        logger.error("No TELEGRAM_BOT_TOKEN found!")
        return

    init_db()

    logger.info("Initializing DC VOLTAGE Supercharged AI Bot (Riya 🌸)...")
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init_health_server).build()

    # Commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("techtip", cmd_techtip))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("broadcast", cmd_broadcast))
    app.add_handler(CommandHandler("voice", cmd_voice))

    # Join & Member Handlers
    app.add_handler(ChatJoinRequestHandler(handle_chat_join_request))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_chat_members))

    # Media Handlers
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice_message))

    # Text Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    # Schedule Daily Tech Tip (Every day at 13:30 UTC = 7:00 PM IST)
    if app.job_queue:
        app.job_queue.run_daily(
            post_daily_tech_tip,
            time=time(hour=13, minute=30, tzinfo=timezone.utc),
            name="daily_tech_tip"
        )
        logger.info("Scheduled Daily Tech Tip job at 19:00 IST.")

    logger.info("Riya Supercharged AI Bot is active and polling for updates!")
    app.run_polling(drop_pending_updates=False)

if __name__ == "__main__":
    main()
