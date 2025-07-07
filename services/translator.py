import httpx

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
            # 🔁 First try
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                translated = response.json().get("translatedText", text).strip()

                # 🔁 Retry once with same payload if untranslated
                if translated == text.strip():
                    retry_response = await client.post(url, json=payload)
                    if retry_response.status_code == 200:
                        translated_retry = retry_response.json().get("translatedText", text).strip()
                        return translated_retry

                return translated
    except Exception as e:
        print(f"Translation failed: {e}")

    return text.strip()  # fallback
