from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.brain import router as brain_router
from app.api.documents import router as documents_router
from app.api.knowledge import router as knowledge_router
from app.api.memory import router as memory_router
from app.db import engine, init_db
from app.sss import models as sss_models  # noqa: F401
from app.sss.router import router as sss_router
from app.sss_v2 import models as sss_v2_models  # noqa: F401
from app.sss_v2.router import router as sss_v2_router
from app.load_balancer import models as load_balancer_models  # noqa: F401
from app.load_balancer.router import router as load_balancer_router
from app.llm.router import router as llm_browser_router
from app.heart.router import router as heart_router
from app.mouth.router import router as mouth_router
from app.eyes.router import router as eyes_router
from Heart.api.heart_api import router as heart_v2_router

app = FastAPI(title="NESLA AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5000",
        "http://localhost:8080",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(memory_router)
app.include_router(knowledge_router)
app.include_router(documents_router)
app.include_router(brain_router)
app.include_router(sss_router)
app.include_router(sss_v2_router)
app.include_router(load_balancer_router)
app.include_router(llm_browser_router)
app.include_router(heart_router)
app.include_router(heart_v2_router)
app.include_router(mouth_router)
app.include_router(eyes_router)


@app.on_event("startup")
def startup_event() -> None:
    init_db()
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))


@app.get("/")
def read_root() -> dict:
    return {"name": "NESLA AI", "status": "running"}


@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "database": "connected"}
