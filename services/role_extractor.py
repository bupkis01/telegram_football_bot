from services.groq_service import call_groq

async def extract_roles(text: str) -> dict:
    prompt = (
        "Analyze the following football news and identify roles.\n"
        "Return a JSON object with keys: journalist, player, club.\n"
        f"Text:\n{text}\n\n"
        "Respond in JSON only."
    )
    result = await call_groq(prompt)
    try:
        return eval(result) if result else {}
    except:
        return {}
