from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Server Configuration
    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=False, description="Debug mode")
    
    # OpenAI Configuration
    openai_api_key: str = Field(default="", description="OpenAI API key")
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2", 
        description="Embedding model name"
    )
    
    # Storage Paths
    hr_policies_path: str = Field(default="./data/hr_policies", description="HR policies directory")
    indices_path: str = Field(default="./data/indices", description="FAISS indices directory")
    
    # FAISS Configuration
    faiss_index_name: str = Field(default="hr_faiss.index", description="FAISS index filename")
    faiss_metadata_name: str = Field(default="hr_meta.json", description="FAISS metadata filename")
    
    # Chunking Configuration
    chunk_size: int = Field(default=1000, description="Text chunk size")
    chunk_overlap: int = Field(default=200, description="Chunk overlap size")
    max_chunks_per_doc: int = Field(default=100, description="Maximum chunks per document")
    
    # Retrieval Configuration
    top_k_results: int = Field(default=5, description="Number of top results to retrieve")
    similarity_threshold: float = Field(default=0.7, description="Similarity threshold for retrieval")

    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60, description="Rate limit per minute")
    enable_rate_limiting: bool = Field(default=False, description="Enable rate limiting")
    
    # File Upload Limits
    max_file_size_mb: int = Field(default=25, description="Maximum file size in MB")
    allowed_file_types: List[str] = Field(
        default=[".pdf", ".txt"], 
        description="Allowed file types"
    )
    
    # Computed Properties
    @property
    def hr_policies_dir(self) -> Path:
        """Get HR policies directory as Path object"""
        return Path(self.hr_policies_path)
    
    @property
    def indices_dir(self) -> Path:
        """Get indices directory as Path object"""
        return Path(self.indices_path)
    
    @property
    def faiss_index_path(self) -> str:
        """Get full FAISS index file path"""
        return str(self.indices_dir / self.faiss_index_name)
    
    @property
    def faiss_metadata_path(self) -> str:
        """Get full FAISS metadata file path"""
        return str(self.indices_dir / self.faiss_metadata_name)
    
    def ensure_directories(self):
        """Ensure all required directories exist"""
        directories = [
            self.hr_policies_dir,
            self.indices_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Ensure directories exist on import
settings.ensure_directories()
