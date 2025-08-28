from pathlib import Path
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Server
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)
    debug: bool = Field(default=False)

    # DeepSeek (do NOT hardcode real keys here; use .env)
    gemini_api_key: str = Field(default="")
    gemini_model: str = Field(default="gemini-default")
    gemini_base_url: str = Field(default="https://generativelanguage.googleapis.com")  # change if different

    # Embeddings
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")

    # Storage paths
    hr_policies_path: str = Field(default="./data/HR Polices")
    indices_path: str = Field(default="./data/indices")
    # (Cache removed) retain path var only if future use needed; removing
    # cache_path field to simplify configuration

    # FAISS filenames
    faiss_index_name: str = Field(default="hr_faiss.index")
    faiss_metadata_name: str = Field(default="hr_meta.json")

    # Chunking
    chunk_size: int = Field(default=1000)
    chunk_overlap: int = Field(default=200)

    # Cache removed (ttl/enable flags deleted)

    # Retrieval / RAG defaults
    top_k_retrieval: int = Field(default=5)
    include_sources: bool = Field(default=True)
    max_context_length: int = Field(default=20000)

    # LLM settings
    llm_temperature: float = Field(default=0.2)
    max_tokens: int = Field(default=600)

    # Uploads
    allowed_file_types: List[str] = Field(default=[".pdf", ".txt", ".docx"])
    max_file_size_mb: int = Field(default=10)

    # pydantic-settings v2 config (do not define inner Config)
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
    # cache_dir removed

    @property
    def faiss_index_path(self) -> str:
        return str(self.indices_dir / self.faiss_index_name)

    @property
    def faiss_metadata_path(self) -> str:
        return str(self.indices_dir / self.faiss_metadata_name)

    def ensure_directories(self) -> None:
        for d in (self.hr_policies_dir, self.indices_dir):
            d.mkdir(parents=True, exist_ok=True)

    # Removed compatibility shims related to caching

    


# instantiate and ensure folders exist
settings = Settings()
settings.ensure_directories()
