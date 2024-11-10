from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Evo Concierge Agent")

app.include_router(router, prefix="/agent") 