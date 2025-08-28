from fastapi import APIRouter, HTTPException, Form
from app.models import HRQueryRequest, HRQueryResponse
from app.services.rag import rag_service

router = APIRouter(prefix="/api/hr", tags=["HR Policies"])

@router.post("/ask", response_model=HRQueryResponse)
async def ask_hr_question(
    query: str = Form(...),
    top_k: int = Form(5)
):
    """Ask a question about HR policies using RAG"""
    
    # Validate input
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    if top_k < 1 or top_k > 20:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 20")
    
    try:
        # Use RAG service to generate answer
        response = await rag_service.answer_question(query.strip(), top_k)
        return HRQueryResponse(**response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
