"""
FastAPI Application - Alejandria API

Main application with document management, authentication, and health check endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import auth, documents, gaps, health, organizations, projects, proposals

# FastAPI app
app = FastAPI(
    title="Alejandria API",
    description="Document Management System with LLM Integration",
    version="0.1.0",
)

from shared.utils.logging import configure_logging  # noqa: E402

configure_logging()

from api.middleware.error_handler import setup_error_handling  # noqa: E402

setup_error_handling(app)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(gaps.router, prefix="/api/v1")
app.include_router(proposals.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")
app.include_router(organizations.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Alejandria API - Document Management System"}
