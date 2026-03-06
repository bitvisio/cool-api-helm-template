from fastapi import FastAPI
from src.api.message_api import router as api_router

app = FastAPI()

@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok"}

# Include the API router
app.include_router(api_router)
