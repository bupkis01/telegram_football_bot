import re
import html

def is_long(text):
    return len(text.split()) > 35

def extract_possible_source(text: str) -> str:
    match = (
        re.search(r"@(\w+)", text) or
        re.search(r"via\s+([A-Za-z0-9_À-ÿ\u0600-\u06FF]+)", text, re.IGNORECASE) or
        re.search(r"\[([A-Za-z0-9_À-ÿ\u0600-\u06FF]+)\]", text)
    )
    if match:
        return match.group(1)

    # Manual fallback
    if "فابريزيو رومانو" in text or "Fabrizio Romano" in text:
        return "Fabrizio Romano"
    return ""

def escape_html(text: str) -> str:
    return html.escape(text)
