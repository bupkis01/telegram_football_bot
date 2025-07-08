import re
import emoji
from services.groq_service import translate_name_with_groq

def remove_emojis(text: str) -> str:
    return emoji.replace_emoji(text, replace='')

async def extract_and_translate_name(text: str) -> str:
    """
    Extract the speaker name (any language) before the first colon,
    remove emojis, then transliterate/translate it to English via Groq.
    """
    # 1) Pull everything before the first colon
    match = re.match(r"^([^\n:：]{2,40})\s*[:：]", text.strip())
    if not match:
        return ""

    name_raw = match.group(1).strip()
    # 2) Remove any emoji
    name_clean = remove_emojis(name_raw).strip()

    # 3) Always use Groq for name transliteration
    try:
        name_en = await translate_name_with_groq(name_clean)
        if name_en:
            return name_en.strip()
    except Exception:
        pass

    # Fallback to the original cleaned name if Groq fails
    return name_clean
