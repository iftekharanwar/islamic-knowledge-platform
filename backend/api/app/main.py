from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from app.routers import knowledge_base, accessibility, personalization, regional
from app.config import settings
from app.services.ai_service import ai_service

app = FastAPI(
    title="Islamic Knowledge Platform API",
    description="AI-powered Islamic knowledge platform providing authentic information and personalized learning",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
async def startup_event():
    await ai_service.initialize()

# Include routers
app.include_router(knowledge_base.router, prefix=settings.API_V1_PREFIX)
app.include_router(accessibility.router, prefix=settings.API_V1_PREFIX)
app.include_router(personalization.router, prefix=settings.API_V1_PREFIX)
app.include_router(regional.router, prefix=settings.API_V1_PREFIX)

@app.get("/healthz")
async def healthz():
    return {"status": "ok", "version": "1.0.0"}
