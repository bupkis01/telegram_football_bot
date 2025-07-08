import httpx
from services.groq_service import translate_name_with_groq  # Keep this for journalist_verifier.py

async def translate_to_english(text: str) -> str:
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

                # If LibreTranslate didn’t change it, just keep the original text
                if out == text.strip():
                    return out

                return out
    except Exception as e:
        print(f"Translation failed: {e}")

    return text.strip()  # Final fallback
