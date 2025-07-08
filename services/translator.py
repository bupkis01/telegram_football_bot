import httpx
from services.groq_service import translate_name_with_groq

async def translate_to_english(text: str) -> str:
    """
    Try LibreTranslate first. If it doesn't translate (returns same text),
    fall back to Groq to improve quality.
    """
    url = "https://libretranslate.de/translate"
    payload = {
        "q": text,
        "source": "auto",
        "target": "en",
        "format": "text"
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                out = resp.json().get("translatedText", text).strip()
                if out == text.strip():
                    # Try Groq fallback
                    groq_out = await translate_name_with_groq(text)
                    return groq_out or out
                return out
    except Exception as e:
        print(f"Translation failed: {e}")

    # Final fallback
    groq_out = await translate_name_with_groq(text)
    return groq_out or text.strip()
