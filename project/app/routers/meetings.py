from fastapi import APIRouter, HTTPException, Form

from app.services.chunking import chunk_text
from app.services.embeddings import Embeddings
from app.vectorstores.faiss_store import MEET_INDEX
from app.config import settings


router = APIRouter(prefix="/api/meetings", tags=["Meeting Summarization"])


def _simple_summary(text: str, max_sentences: int = 5) -> str:
    """Create a simple summary by taking first few sentences."""
    if not text.strip():
        return ""
    
    # Split by periods and take first few sentences
    sentences = [s.strip() + "." for s in text.split(".") if s.strip()]
    summary_sentences = sentences[:max_sentences]
    
    return " ".join(summary_sentences)

@router.post("/summarize/text")
async def summarize_text(meeting_content: str = Form(...)):
    """Summarize meeting text content."""
    if not meeting_content.strip():
        raise HTTPException(status_code=400, detail="Content required")
    
    summary = _simple_summary(meeting_content)
    return {"summary": summary}


@router.post("/summarize/text/store")
async def summarize_and_store_text(
    meeting_content: str = Form(...),
    meeting_title: str = Form("Untitled Meeting")
):
    """Summarize meeting content and optionally store for future search."""
    if not meeting_content.strip():
        raise HTTPException(status_code=400, detail="Content required")
    
    # Generate summary
    summary = _simple_summary(meeting_content)
    
    # Store in vector index for future search
    chunks = chunk_text(meeting_content, settings.chunk_size, settings.chunk_overlap)
    
    if chunks:
        embeddings = Embeddings().embed(chunks)
        metas = [{"source": meeting_title, "chunk": i, "type": "meeting"} for i in range(len(chunks))]
        MEET_INDEX.add(embeddings, chunks, metas)
        MEET_INDEX.save()
    
    return {
        "summary": summary,
        "chunks_stored": len(chunks),
        "total_meetings": len(MEET_INDEX.texts)
    }

