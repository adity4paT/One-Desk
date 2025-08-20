from fastapi import FastAPI

from app.config import settings
from app.routers import hr, meetings
from app.vectorstores.faiss_store import HR_INDEX, MEET_INDEX


app = FastAPI(title="One-Desk Backend API", version="1.0.0")

app.include_router(hr.router)
app.include_router(meetings.router)


@app.on_event("startup")
async def _startup():
    settings.ensure_directories()
    HR_INDEX.load()
    MEET_INDEX.load()


@app.get("/")
async def root():
    return {"name": "One-Desk Backend API", "docs": "/docs"}
