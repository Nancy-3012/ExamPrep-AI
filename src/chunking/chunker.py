def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Splits text into overlapping chunks.

    Args:
        text (str): cleaned text
        chunk_size (int): size of each chunk
        overlap (int): overlap between chunks

    Returns:
        list of text chunks
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks