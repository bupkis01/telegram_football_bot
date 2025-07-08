import re
from services.groq_service import call_groq

BAD_PREFIXES = [
    "Here is the rewritten", "Rewritten text", "Sure,", "Of course,",
    "The rewritten version is", "Here’s", "Here is"
]

async def rewrite_professionally(text: str) -> str:
    """
    Rewrites the input text into 1–2 short, factual sentences for Telegram.
    NEVER add, invent, or assume any information not explicitly present.
    """

    cleaned = text.strip()
    if not cleaned:
        return ""

    prompt = (
        "You are a professional football news editor.\n"
        "Below is the full text of a news item. Rewrite it into 1–2 short, clear Telegram-style sentences.\n"
        "DO NOT add or invent any details (e.g., job titles, outcomes) that are not in the original.\n"
        "ONLY rephrase what is there.\n\n"
        f"Original Text:\n{cleaned}\n\n"
        "Rewrite:"
    )

    result = await call_groq(prompt)
    if result:
        result = result.strip()

        # 🚫 Remove assistant-style intros
        for prefix in BAD_PREFIXES:
            if result.lower().startswith(prefix.lower()):
                result = result.split(":", 1)[-1].strip()
                break  # Remove only one match, then stop

        # 🧼 Normalize whitespace
        return re.sub(r"\s+", " ", result)

    # 🧯 Fallback: Use first 2 lines of the original
    lines = cleaned.splitlines()
    return " ".join(lines[:2]).strip()
