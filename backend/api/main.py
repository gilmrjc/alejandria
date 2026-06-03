"""
FastAPI Application - Placeholder

This module will contain the main FastAPI application.
"""

from fastapi import FastAPI

# Placeholder for FastAPI app
app = FastAPI(
    title="Alejandria API",
    description="Document Management System with LLM Integration",
    version="0.1.0",
)


@app.get("/")
async def root():
    """Root endpoint - placeholder."""
    return {"message": "Alejandria API - Placeholder"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
