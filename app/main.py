from fastapi import FastAPI
from app.api import metrics, users

app = FastAPI(title="CX‑Analytics MVP")

app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
app.include_router(users.router, prefix="/users", tags=["users"])
