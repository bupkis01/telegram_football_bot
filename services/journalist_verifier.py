from services.role_extractor import extract_roles

TRUSTED_JOURNALISTS = [
    "fabrizio romano", "ashraf ben ayad", "david ornstein",
    "جيانلوكا دي مارزيو", "فابريزيو رومانو", "gerard romero",
    "santi aouna", "nicolò schira", "نيكولو شيرا"
]

async def is_trusted_journalist_from_text(text: str) -> str | None:
    """
    Extract journalist name from the text using AI and check if it's trusted.
    Returns the journalist name if trusted, otherwise None.
    """
    roles = await extract_roles(text)
    name = roles.get("journalist", "").strip().lower()

    for trusted in TRUSTED_JOURNALISTS:
        if trusted.lower() in name:
            return name

    return None
