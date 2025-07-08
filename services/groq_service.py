import httpx
import logging
from config import GROQ_API_KEY, GROQ_MODEL

logger = logging.getLogger(__name__)

async def call_groq(prompt: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2
                }
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"].strip()
            else:
                logger.error(f"Groq error {resp.status_code}: {resp.text}")
    except Exception as e:
        logger.error(f"Groq exception: {e}")
    return None

async def translate_name_with_groq(name: str) -> str:
    prompt = (
        "Translate this personal name into proper English spelling only. "
        "Only give the name:\n"
        f"{name}"
    )
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": [
                        {"role": "system", "content": "You are a name transliteration assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2
                }
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"].strip()
            else:
                logger.error(f"Groq error {resp.status_code}: {resp.text}")
    except Exception as e:
        logger.error(f"Groq exception: {e}")
    return None
