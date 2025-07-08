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
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                out = resp.json().get("translatedText", text).strip()
                return out  # ✅ Just return result, no fallback
    except Exception as e:
        print(f"Translation failed: {e}")

    return text.strip()  # final fallback
