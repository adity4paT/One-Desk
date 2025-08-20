from pydantic import BaseModel, Field
from typing import List, Optional, Any

# Request Models
class HRQueryRequest(BaseModel):
    query: str = Field(..., description="The HR policy question to answer")
    top_k: Optional[int] = Field(None, description="Number of relevant contexts to retrieve")

class SummarizeTextRequest(BaseModel):
    meeting_content: str = Field(..., description="The meeting content to summarize")
    meeting_title: str = Field("Untitled Meeting", description="Title of the meeting")

# Response Models
class SourceInfo(BaseModel):
    source: str = Field(..., description="Source document name")
    chunk: int = Field(..., description="Chunk number within document")
    score: float = Field(..., description="Relevance score")

class HRQueryResponse(BaseModel):
    answer: str = Field(..., description="Generated answer to the question")
    contexts: List[str] = Field(..., description="Retrieved context chunks")
    sources: List[SourceInfo] = Field(..., description="Source information")
    cached: bool = Field(..., description="Whether response was cached")
    latency_ms: int = Field(..., description="Response latency in milliseconds")

class SummaryResponse(BaseModel):
    summary: str = Field(..., description="Generated meeting summary")
    meeting_title: str = Field(..., description="Meeting title")
    text_length: int = Field(..., description="Original text length")
    cached: bool = Field(..., description="Whether response was cached")
    latency_ms: int = Field(..., description="Response latency in milliseconds")
    chunks_stored: Optional[int] = Field(None, description="Number of chunks stored")
