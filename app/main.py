from fastapi import FastAPI
from app.core.config import settings
from app.db.base import engine
from app.api import auth, requests, feedback
import uvicorn

app = FastAPI(title="Bareez Hotel Dashboard")

# Include routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(requests.router, prefix="/api", tags=["requests"])
app.include_router(feedback.router, prefix="/api", tags=["feedback"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)