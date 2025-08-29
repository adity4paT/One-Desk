from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text: str, size: int = 800, overlap: int = 120) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Input text to chunk
        size: Size of each chunk in characters
        overlap: Overlap between chunks in characters
    
    Returns:
        List of text chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap
    )
    chunks = text_splitter.split_text(text)
    return chunks
