# run in Python from project root (or paste into a small script)
from app.vectorstores.faiss_store import HR_INDEX
HR_INDEX.load()                 # ensure loader runs
print("index_loaded:", HR_INDEX.load)     # or whatever property your class uses
print("num_vectors:", getattr(HR_INDEX, "ntotal", "unknown"))  # common for FAISS wrappers
# Try a test search
q = "vacation leave policy"
emb = HR_INDEX.get_query_embedding(q) if hasattr(HR_INDEX, "get_query_embedding") else None
res = HR_INDEX.search(emb, k=5) if emb is not None else HR_INDEX.search_by_text(q, k=5) if hasattr(HR_INDEX, "search_by_text") else None
print("sample_results:", res)