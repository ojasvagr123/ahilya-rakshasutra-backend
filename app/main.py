from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# load .env early
load_dotenv()

from .db import init_db

# ✅ import the actual router objects directly
from app.routers.auth import router as auth_router
from app.routers.reports import router as reports_router
from app.routers.admin import router as admin_router

app = FastAPI(title="Ahilya RakshaSutra API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

@app.on_event("startup")
def on_startup():
    init_db()

# ✅ include the routers directly (no .router attribute)
app.include_router(auth_router)
app.include_router(reports_router)
app.include_router(admin_router)

@app.get("/health")
def health():
    return {"ok": True}
