import os
import re
import uuid
import logging
import edge_tts

logger = logging.getLogger(__name__)

VOICE_MAP = {
    "ml": "ml-IN-SobhanaNeural",
    "hi": "hi-IN-SwaraNeural",
    "ta": "ta-IN-PallaviNeural",
    "te": "te-IN-ShrutiNeural",
    "en": "en-IN-NeerjaExpressiveNeural",
    "manglish": "en-IN-NeerjaExpressiveNeural",
    "hinglish": "hi-IN-SwaraNeural",
}

TEMP_AUDIO_DIR = "/tmp/riya_audio"
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

def clean_text_for_speech(text: str) -> str:
    """Strip complex code blocks, URLs, and excessive formatting for natural audio speech."""
    # Replace markdown code blocks with spoken summary
    text = re.sub(r'```[\s\S]*?```', ' Check the exact terminal commands sent in the chat below sweetie! ', text)
    text = re.sub(r'`[^`\n]+`', '', text)
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    # Remove hashtags and excessive symbols
    text = re.sub(r'[*#_~`>•]', ' ', text)
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Limit speech length to ~400 characters for snappy voice note
    if len(text) > 400:
        text = text[:400] + "... I have sent all detailed steps and commands in the text right below sweetie!"
    return text

async def generate_voice_note(text: str, lang: str = "en") -> str:
    """Generate an MP3 voice note file from text using Edge-TTS."""
    voice = VOICE_MAP.get(lang, "en-IN-NeerjaExpressiveNeural")
    clean_text = clean_text_for_speech(text)
    if not clean_text:
        clean_text = "Haii sweetie! Boss DC VOLTAGE and I are here to help you anytime!"

    file_id = uuid.uuid4().hex[:8]
    output_path = os.path.join(TEMP_AUDIO_DIR, f"riya_{file_id}.mp3")

    communicate = edge_tts.Communicate(clean_text, voice)
    await communicate.save(output_path)
    return output_path
