from app.config import settings  # Adjust the import path as needed
from langchain.embeddings import HuggingFaceEmbeddings

def get_embedding_model():
    model = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    return model

Embedding = get_embedding_model()