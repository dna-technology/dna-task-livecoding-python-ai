from fastapi import FastAPI

from .routes import router

app = FastAPI(title="Simple RAG API", version="0.1.0")
app.include_router(router)
