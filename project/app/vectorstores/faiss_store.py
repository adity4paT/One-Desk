from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import faiss  # type: ignore

from app.config import settings


class SimpleFaissIndex:
    """Minimal FAISS IP index with simple JSON sidecar for texts+metas."""

    def __init__(self, index_path: Path, meta_path: Path) -> None:
        self.index_path = index_path
        self.meta_path = meta_path
        self.index: Optional[faiss.Index] = None
        self.texts: List[str] = []
        self.metas: List[Dict[str, Any]] = []
        self.dim: Optional[int] = None
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.meta_path.parent.mkdir(parents=True, exist_ok=True)

    def _ensure(self, dim: int) -> None:
        if self.index is None:
            self.index = faiss.IndexFlatIP(dim)
            self.dim = dim

    def add(self, embeddings: np.ndarray, texts: List[str], metas: List[Dict[str, Any]]) -> int:
        if embeddings.shape[0] != len(texts) or len(texts) != len(metas):
            raise ValueError("embeddings, texts, metas must be same length")
        if embeddings.dtype != np.float32:
            embeddings = embeddings.astype(np.float32)
        self._ensure(embeddings.shape[1])
        before = self.count
        self.index.add(embeddings)  # type: ignore[arg-type]
        self.texts.extend(texts)
        self.metas.extend(metas)
        return self.count - before

    def search(self, query_vec: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        if self.index is None or not self.texts:
            return []
        if query_vec.ndim == 1:
            query_vec = query_vec.reshape(1, -1).astype(np.float32)
        D, I = self.index.search(query_vec, k)
        out: List[Dict[str, Any]] = []
        for score, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self.texts):
                continue
            out.append({"text": self.texts[idx], "score": float(score), "meta": self.metas[idx]})
        return out

    def save(self) -> None:
        if self.index is None:
            return
        faiss.write_index(self.index, str(self.index_path))
        self.meta_path.write_text(json.dumps({
            "texts": self.texts,
            "metas": self.metas,
            "dim": self.dim,
        }, ensure_ascii=False))

    def load(self) -> bool:
        if not self.index_path.exists() or not self.meta_path.exists():
            return False
        self.index = faiss.read_index(str(self.index_path))
        data = json.loads(self.meta_path.read_text(encoding="utf-8"))
        self.texts = data.get("texts", [])
        self.metas = data.get("metas", [])
        self.dim = data.get("dim")
        return True

    def clear(self) -> None:
        self.index = None
        self.texts = []
        self.metas = []
        self.dim = None
        try:
            if self.index_path.exists():
                self.index_path.unlink()
            if self.meta_path.exists():
                self.meta_path.unlink()
        except Exception:
            pass

    @property
    def count(self) -> int:
        return len(self.texts)

# Two simple indices: HR and Meetings
HR_INDEX = SimpleFaissIndex(
    settings.indices_dir / "hr.index",
    settings.indices_dir / "hr.meta.json",
)

MEET_INDEX = SimpleFaissIndex(
    settings.indices_dir / "meet.index",
    settings.indices_dir / "meet.meta.json",
)
