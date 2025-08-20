from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import httpx
from app.config import settings
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(".env")) 

deepseek_api_key = os.getenv("deepseek_api_key", "")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

class LLMClient(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        pass

class DeepSeekClient(LLMClient):
    """DeepSeek API client using OpenAI-compatible format"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com"
        
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": DEEPSEEK_MODEL,
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


def get_llm_client() -> LLMClient:
    return DeepSeekClient(deepseek_api_key)
   