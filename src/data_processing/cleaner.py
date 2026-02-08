import re

def clean_text(text: str) -> str:
    """
    Cleans extracted text by removing extra spaces,
    line breaks, and unwanted characters.
    """
    if not text:
        return ""

    # Remove multiple newlines
    text = re.sub(r"\n+", "\n", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove non-printable characters
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    return text.strip()