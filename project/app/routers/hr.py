from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import numpy as np


from app.services.embeddings import Embeddings
from app.vectorstores.faiss_store import HR_INDEX


router = APIRouter(prefix="/api/hr", tags=["HR Policies"])

@router.post("/search")
async def search(query: str = Form(...), top_k: int = Form(5)):
    q = (query or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="Query required")

    HR_INDEX.load()

    emb = Embeddings()
    qv = emb.embed_one(q).astype(np.float32)
    hits = HR_INDEX.search(qv, k=max(1, min(top_k, 20)))
    results = [
        {
            "text": h["text"],
            "score": round(h["score"], 4),
            "source": h["meta"].get("source"),
            "chunk": h["meta"].get("chunk"),
        }
        for h in hits
    ]

    return {"query": q, "results": results}
