from pathlib import Path
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Server
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)
    debug: bool = Field(default=False)

    # DeepSeek
    deepseek_api_key: str = Field(default="sk-a23ee41ab1e14c07ad3d934a9fb27f5e")
    deepseek_model: str = Field(default="deepseek-chat")
    deepseek_base_url: str = Field(default="https://api.deepseek.com")

    # Embeddings
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")

    # Storage
    hr_policies_path: str = Field(default="./data/HR Polices")
    indices_path: str = Field(default="./data/indices")
    cache_path: str = Field(default="./data/cache")

    # FAISS
    faiss_index_name: str = Field(default="hr_faiss.index")
    faiss_metadata_name: str = Field(default="hr_meta.json")

    # Chunking
    chunk_size: int = Field(default=1000)
    chunk_overlap: int = Field(default=200)

    # Cache (used by cache.py)
    cache_ttl_seconds: int = Field(default=3600)
    enable_cache: bool = Field(default=True)

    # Retrieval / RAG defaults (compatibility & expected by rag.py)
    top_k_retrieval: int = Field(default=5)
    include_sources: bool = Field(default=True)
    max_context_length: int = Field(default=20000)

    # Uploads
    allowed_file_types: List[str] = Field(default=[".pdf", ".txt"])
    max_file_size_mb: int = Field(default=10)

    # Pydantic v2 settings config (do NOT also define inner Config)
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def hr_policies_dir(self) -> Path:
        return Path(self.hr_policies_path)

    @property
    def indices_dir(self) -> Path:
        return Path(self.indices_path)

    @property
    def cache_dir(self) -> Path:
        return Path(self.cache_path)

    @property
    def faiss_index_path(self) -> str:
        return str(self.indices_dir / self.faiss_index_name)

    @property
    def faiss_metadata_path(self) -> str:
        return str(self.indices_dir / self.faiss_metadata_name)
    @property
    def embedding_cache_ttl(self) -> int:
        return self.cache_ttl_seconds

    @property
    def response_cache_ttl(self) -> int:
        return self.cache_ttl_seconds

    @property
    def enable_embedding_cache(self) -> bool:
        return self.enable_cache

    @property
    def enable_response_cache(self) -> bool:
        return self.enable_cache

    def ensure_directories(self) -> None:
        for d in (self.hr_policies_dir, self.indices_dir, self.cache_dir):
            d.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_directories()
