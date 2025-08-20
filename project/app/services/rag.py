from typing import List, Dict, Any, Optional
import time
from app.services.llm import MODEL_NAME, get_llm_client
from app.services.cache import cache_manager
from app.vectorstores.faiss_store import HR_INDEX
from app.services.embeddings import embeddings
from app.config import settings

class RAGService:
    """Core RAG service for HR policy question answering"""
    
    def __init__(self):
        self.llm_client = get_llm_client()
    
    async def answer_question(self, query: str, top_k: 'Optional[int]' = None) -> Dict[str, Any]:
        """Main RAG pipeline: retrieve -> synthesize -> return"""
        start_time = time.time()
        
        # Use default or provided top_k
        top_k = top_k or settings.top_k_retrieval

        # Always define cache_key if response cache is enabled
        cache_key = None
        if settings.enable_response_cache:
            cache_key = cache_manager.generate_key("hrqa", {
                "query": query,
                "top_k": top_k,
                "model": MODEL_NAME
            })

            cached_response = cache_manager.get_response(cache_key)
            if cached_response:
                cached_response["cached"] = True
                cached_response["latency_ms"] = int((time.time() - start_time) * 1000)
                return cached_response
        
        # Step 1: Retrieve relevant contexts
        contexts = await self._retrieve_contexts(query, top_k)
        
        if not contexts:
            response = {
                "answer": "I couldn't find any relevant information in the HR policies to answer your question.",
                "contexts": [],
                "sources": [],
                "cached": False,
                "latency_ms": int((time.time() - start_time) * 1000)
            }
            return response
        
        # Step 2: Generate answer using LLM
        answer = await self._synthesize_answer(query, contexts)
        
        # Step 3: Prepare response
        sources = [
            {
                "source": ctx["meta"]["source"],
                "chunk": ctx["meta"]["chunk"],
                "score": round(ctx["score"], 4)
            }
            for ctx in contexts
        ]
        
        response = {
            "answer": answer,
            "contexts": [ctx["text"] for ctx in contexts],
            "sources": sources if settings.include_sources else [],
            "cached": False,
            "latency_ms": int((time.time() - start_time) * 1000)
        }
        # Cache the response (response cache)
        if settings.enable_response_cache and cache_key is not None:
            cache_manager.set_response(cache_key, response.copy())
        
        return response
        return response
    
    async def _retrieve_contexts(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Retrieve and rank relevant document chunks"""
        # Ensure HR index is loaded
        HR_INDEX.load()
        
        # Get query embedding — use embedding cache if enabled
        if settings.enable_embedding_cache:
            emb_key = cache_manager.generate_key("embedding", {"text_hash": hash(query)})
            try:
                cached_emb = cache_manager.get_embedding(emb_key)
            except Exception:
                cached_emb = None

            if cached_emb is not None:
                query_embedding = cached_emb
            else:
                query_embedding = embeddings.embed_one(query)
                try:
                    cache_manager.set_embedding(emb_key, query_embedding)
                except Exception:
                    pass
        else:
            query_embedding = embeddings.embed_one(query)
        
        # Search for similar chunks
        results = HR_INDEX.search(query_embedding, k=top_k)
        
        # Filter and prepare contexts
        contexts = []
        total_chars = 0
        
        for result in results:
            # Skip if context would be too long
            if total_chars + len(result["text"]) > settings.max_context_length:
                break
                
            contexts.append(result)
            total_chars += len(result["text"])
        
        return contexts
    
    async def _synthesize_answer(self, query: str, contexts: List[Dict[str, Any]]) -> str:
        """Use LLM to synthesize answer from retrieved contexts"""
        
        # Build context string
        context_parts = []
        for i, ctx in enumerate(contexts, 1):
            source = ctx["meta"]["source"]
            context_parts.append(f"[Context {i} - {source}]:\n{ctx['text']}")
        
        context_string = "\n\n".join(context_parts)
        
        # Create messages for LLM
        system_prompt = """You are an HR assistant helping employees with policy questions. 

INSTRUCTIONS:
1. Answer questions using ONLY the provided context from HR policies
2. If the answer is not in the context, say "I don't have that information in the available HR policies"
3. Be specific and cite relevant policy sections when possible
4. Keep answers concise but complete
5. If multiple contexts are relevant, synthesize information appropriately

IMPORTANT: Do not make up information not present in the contexts."""

        user_prompt = f"""Question: {query}

Available Context:
{context_string}

Please provide a clear, helpful answer based on the context above."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Generate response
        try:
            answer = await self.llm_client.generate_response(messages)
            return answer.strip()
        except Exception as e:
            return f"I encountered an error while processing your question: {str(e)}"

# Global RAG service instance
rag_service = RAGService()
