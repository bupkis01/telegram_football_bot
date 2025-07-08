import re
from services.groq_service import call_groq
from utils.text_utils import is_long

IMPORTANT_PHRASES = ["HERE WE GO!", "Here we go!", "here we go!"]
UNWANTED_PHRASES = [
    "Breaking news", "Breaking:", "BREAKING", "Stay tuned",
    "report", "sources say", "Latest update", "Exclusive"
]
BAD_REPLIES = [
    "no factual information",
    "nothing to rewrite",
    "breaking"
]

def extract_important_phrases(text: str) -> str:
    return " ".join([phrase for phrase in IMPORTANT_PHRASES if phrase in text])

def remove_unwanted_phrases(text: str) -> str:
    for phrase in UNWANTED_PHRASES:
        # Use regex to remove phrases case-insensitively
        text = re.sub(re.escape(phrase), "", text, flags=re.IGNORECASE)
    return text.strip()

async def rewrite_professionally(text: str) -> str:
    preserved = extract_important_phrases(text)
    cleaned_text = text
    for phrase in IMPORTANT_PHRASES:
        cleaned_text = cleaned_text.replace(phrase, "")  # Remove before sending

    # Skip rewrite if not enough content
    if len(cleaned_text.strip()) < 10:
        return cleaned_text.strip()

    prompt = (
        "You are a football journalist assistant for a Telegram bot.\n"
        "Your job is to rephrase football news messages in exactly 1–2 factual sentences.\n"
        "DO NOT include names or lines that do not contain actual football info.\n"
        "DO NOT echo the journalist’s name or metadata.\n"
        "DO NOT generate headlines or introductions like 'Breaking'.\n"
        "ONLY include the core football facts (e.g. transfers, negotiations, injuries, etc).\n\n"
        f"Original:\n{cleaned_text.strip()}\n\n"
        "Rephrased (only football content):"
    )

    result = await call_groq(prompt)
    if not result:
        return cleaned_text.strip()

    final = remove_unwanted_phrases(result.strip())

    # Fallback: If the output is only a name or too short
    if len(final.split()) < 4 or final.lower() in text.lower():
        return cleaned_text.strip()

    if preserved:
        final += f" {preserved}"
    return final.strip()
