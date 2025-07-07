import httpx

async def translate_to_english(text: str) -> str:
    url = "https://libretranslate.de/translate"
    payload = {
        "q": text,
        "source": "auto",       # Detects language automatically
        "target": "en",         # Translate to English
        "format": "text"
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                return response.json().get("translatedText", text)
    except Exception as e:
        print(f"Translation failed: {e}")

    return text  # fallback to original if translation fails
