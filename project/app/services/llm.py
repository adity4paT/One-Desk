from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import httpx
from app.config import settings

API_KEY = settings.gemini_api_key
MODEL_NAME = settings.gemini_model
BASE_URL = settings.gemini_base_url

class LLM():
    """DeepSeek API client using OpenAI-compatible format"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = BASE_URL
        
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": kwargs.get("temperature", settings.llm_temperature),
            "max_tokens": kwargs.get("max_tokens", settings.max_tokens),
            "stream": False
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]


def get_llm_client() :
    return LLM(API_KEY)
