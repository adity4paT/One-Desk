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

# # Keep the old search endpoint for backward compatibility
# @router.post("/search")
# async def search_hr_policies(
#     query: str = Form(...), 
#     top_k: int = Form(5)
# ):
#     """Search HR policies (returns raw search results without LLM synthesis)"""
    
#     if not query.strip():
#         raise HTTPException(status_code=400, detail="Query required")
    
#     try:
#         from app.vectorstores.faiss_store import HR_INDEX
#         from app.services.embeddings import embeddings
        
#         HR_INDEX.load()
#         query_vector = embeddings.embed_one(query.strip())
#         hits = HR_INDEX.search(query_vector, k=max(1, min(top_k, 20)))
        
#         results = [
#             {
#                 "text": h["text"],
#                 "score": round(h["score"], 4),
#                 "source": h["meta"].get("source"),
#                 "chunk": h["meta"].get("chunk"),
#             }
#             for h in hits
#         ]
        
#         return {"query": query.strip(), "results": results}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")
