from typing import List


def chunk_text(text: str, size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Input text to chunk
        size: Size of each chunk in characters
        overlap: Overlap between chunks in characters
    
    Returns:
        List of text chunks
    """
    if size <= 0:
        return [text]
    
    chunks: List[str] = []
    i = 0
    n = len(text)
    
    while i < n:
        chunks.append(text[i : i + size])
        if i + size >= n:
            break
        i += max(1, size - overlap)
    
    return chunks
