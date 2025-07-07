import httpx
import logging
from config import GROQ_API_KEY, GROQ_MODEL

logger = logging.getLogger(__name__)

async def call_groq(prompt: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": GROQ_MODEL,  # ✅ Updated model
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2
                }
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            else:
                logger.error(f"Groq error {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Groq exception: {e}")
    return None
