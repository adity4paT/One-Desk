from typing import Dict, Any
import time
from app.services.llm import get_llm_client
from app.config import settings

class SummaryService:
    """LLM-powered meeting summarization service"""
    
    def __init__(self):
        self.llm_client = get_llm_client()
    
    async def summarize_text(self, text: str, meeting_title: str = "Meeting") -> Dict[str, Any]:
        """Summarize meeting text using LLM"""
        start_time = time.time()
        
    # Caching removed for simplicity; always compute fresh summary
        
        # Generate summary using LLM
        summary = await self._generate_summary(text, meeting_title)
        
        response = {
            "summary": summary,
            "meeting_title": meeting_title,
            "text_length": len(text),
            "cached": False,
            "latency_ms": int((time.time() - start_time) * 1000)
        }
        
        return response
    
    async def _generate_summary(self, text: str, meeting_title: str) -> str:
        """Generate meeting summary using LLM"""
        
        system_prompt = """You are an expert meeting summarizer. Create concise, structured summaries of meeting transcripts.

SUMMARY FORMAT:
## Meeting Overview
[Brief 1-2 sentence overview]

## Key Discussions
[Main topics and decisions, bullet points]

## Action Items
[Who needs to do what, with deadlines if mentioned]

## Next Steps
[Follow-up meetings, decisions needed, etc.]

Keep summaries professional, actionable, and well-organized."""
        
        user_prompt = f"""Meeting Title: {meeting_title}

Meeting Content:
{text}

Please provide a structured summary following the format above."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            summary = await self.llm_client.generate_response(messages)
            return summary.strip()
        except Exception as e:
            return f"Error generating summary: {str(e)}"

# Global summary service instance
summary_service = SummaryService()
