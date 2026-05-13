from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from app.config import ALLOWED_ORIGINS


app = FastAPI(title="INFINITY ERMA API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
