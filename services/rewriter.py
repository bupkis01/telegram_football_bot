from services.groq_service import call_groq  # using Groq instead of Cohere
from utils.text_utils import is_long

IMPORTANT_PHRASES = ["HERE WE GO!", "Here we go!", "here we go!"]
UNWANTED_PHRASES = ["Breaking news", "Stay tuned", "report", "sources say"]

def extract_important_phrases(text: str) -> str:
    return " ".join([phrase for phrase in IMPORTANT_PHRASES if phrase in text])

def remove_unwanted_phrases(text: str) -> str:
    for phrase in UNWANTED_PHRASES:
        text = text.replace(phrase, "")
    return text.strip()

async def rewrite_professionally(text: str) -> str:
    preserved = extract_important_phrases(text)
    cleaned_text = text
    for phrase in IMPORTANT_PHRASES:
        cleaned_text = cleaned_text.replace(phrase, "")  # Remove before sending to model

    strict_rules = (
        "- ONLY use the facts explicitly mentioned.\n"
        "- NEVER speculate or include any facts not present in the original.\n"
        "- NEVER add or assume background details or context.\n"
        "- DO NOT invent clubs, managers, roles, or context not already in the text.\n"
        "- DO NOT change or guess player names. Only rewrite what is explicitly written.\n"
        "- DO NOT use emojis, markdown, or assistant phrases.\n"
        "- RETURN only the rewritten factual lines. Do NOT drop any football phrases if present.\n"
    )

    if is_long(cleaned_text):
        prompt = (
            "Rewrite the following football news into exactly 1–2 short lines for Telegram.\n"
            f"STRICT RULES (violation will invalidate output):\n{strict_rules}\n"
            f"Text:\n{cleaned_text.strip()}\n\n"
        )
    else:
        prompt = (
            "Rewrite this football news in 1–2 short factual lines for Telegram.\n"
            f"STRICT RULES (violation will invalidate output):\n{strict_rules}\n"
            f"Text:\n{cleaned_text.strip()}\n\n"
        )

    result = await call_groq(prompt)
    if not result:
        return "⚠️ Failed to rewrite."

    final = remove_unwanted_phrases(result.strip())
    if preserved:
        final += f" {preserved}"
    return final.strip()
