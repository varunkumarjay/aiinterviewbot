from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes_interview import router as interview_router


app = FastAPI(
    title="AI Interview Engine",
    version="1.0.0",
    description="Adaptive AI-powered interview system with live evaluation and deep post-analysis."
)

# --------------------------------------------------
# CORS (allow frontend later)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Interview Routes
# --------------------------------------------------
app.include_router(interview_router, prefix="/interview")

# --------------------------------------------------
# Health Check
# --------------------------------------------------
@app.get("/")
def health():
    return {
        "status": "AI Core Running",
        "service": "Interview Engine",
        "version": "1.0.0"
    }

