import re
import emoji
from services.translator import translate_to_english

def remove_emojis(text: str) -> str:
    return emoji.replace_emoji(text, replace='')

async def extract_and_translate_name(text: str) -> str:
    match = re.match(r"^([^\n:：]{2,40})\s*[:：]", text.strip())
    if not match:
        print("❌ No name matched.")
        return ""

    name_raw = match.group(1).strip()
    name_clean = remove_emojis(name_raw).strip()

    print(f"🔍 Raw name: {name_raw}")
    print(f"🔍 Clean name: {name_clean}")

    try:
        translated = await translate_to_english(name_clean)
        print(f"🧠 Translated name: {translated}")

        if translated == name_clean:
            translated_retry = await translate_to_english(name_clean)
            print(f"🔁 Retry translation: {translated_retry}")
            return translated_retry.strip()

        return translated.strip()

    except Exception as e:
        print(f"⚠️ Translation error: {e}")
        return name_clean
