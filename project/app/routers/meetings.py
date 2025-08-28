from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from typing import Optional
import fitz  # PyMuPDF
import io
from app.models import SummaryResponse
from app.services.summary import summary_service
from app.services.chunking import chunk_text
from app.services.embeddings import embeddings
from app.vectorstores.faiss_store import MEET_INDEX
from app.config import settings

router = APIRouter(prefix="/api/meetings", tags=["Meeting Summarization"])

@router.post("/summarize/text", response_model=SummaryResponse)
async def summarize_text_meeting(
    meeting_content: str = Form(...),
    meeting_title: str = Form("Untitled Meeting"),
    store_for_search: bool = Form(False)
):
    """Summarize meeting content using LLM and optionally store for future search"""
    
    if not meeting_content.strip():
        raise HTTPException(status_code=400, detail="Meeting content cannot be empty")
    
    try:
        # Generate LLM-powered summary
        result = await summary_service.summarize_text(
            meeting_content.strip(), 
            meeting_title
        )
       
        return SummaryResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization error: {str(e)}")

@router.post("/summarize/pdf", response_model=SummaryResponse)
async def summarize_pdf_meeting(
    pdf_file: UploadFile = File(...),
    meeting_title: Optional[str] = Form(None),
    store_for_search: bool = Form(False)
):
    """Upload PDF, extract text, summarize using LLM and optionally store for search"""
    
    # Validate file
    if not pdf_file.filename or not pdf_file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Extract title from filename if notd
    if not meeting_title:
        meeting_title = pdf_file.filename.replace('.pdf', '').replace('_', ' ').title()
    
    try:
        # Extract text from PDF
        meeting_content = await _extract_pdf_text(pdf_file)
        
        if not meeting_content.strip():
            raise HTTPException(status_code=400, detail="No text content found in PDF")
        
        # Generate LLM-powered summary
        result = await summary_service.summarize_text(meeting_content, meeting_title)
        
        return SummaryResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF processing error: {str(e)}")

# Helper functions
async def _extract_pdf_text(file: UploadFile) -> str:
    """Extract text from uploaded PDF file"""
    try:
        pdf_bytes = await file.read()
        with fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf") as doc:
            text_content = ""
            for page in doc:
                text_content += page.get_text("text") + "\n"
        return text_content.strip()
    except Exception as e:
        raise Exception(f"Failed to extract PDF text: {str(e)}")

    """Store meeting chunks in vector database for future search"""
    try:
        chunks = chunk_text(content, settings.chunk_size, settings.chunk_overlap)
        
        if not chunks:
            return 0
        
        # Generate embeddings
        chunk_embeddings = embeddings.embed(chunks)
        
        # Create metadata
        metas = [
            {
                "source": title,
                "chunk": i,
                "type": "meeting"
            }
            for i in range(len(chunks))
        ]
        
        # Store in FAISS
        MEET_INDEX.add(chunk_embeddings, chunks, metas)
        MEET_INDEX.save()
        
        return len(chunks)
    
    except Exception as e:
        # Log error but don't fail the whole request
        print(f"Error storing meeting chunks: {str(e)}")
        return 0
