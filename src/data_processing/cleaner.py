import re

def clean_text(text: str) -> str:
    """
    Clean extracted text.
    """

    if not text:
        return ""

    # remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    # remove strange characters
    text = re.sub(r"[^\w\s.,()-]", "", text)

    return text.strip()