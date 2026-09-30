from fastapi import FastAPI
from backend.routes import router
app = FastAPI(title="LegalEaseAI - 210PocketSmart")
app.include_router(router)
