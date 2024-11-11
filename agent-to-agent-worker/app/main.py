from fastapi import FastAPI
from .api.routes import router

app = FastAPI(title="Agent-to-Agent Worker")

app.include_router(router, prefix="/agent") 