"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

from app.routes import documents, qa


# Create FastAPI app
app = FastAPI(
    title="Document-Based Question Answering System",
    description="Upload documents and ask questions based on their content",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router)
app.include_router(qa.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Document-Based Question Answering System API",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "documents": "/api/documents",
            "qa": "/api/qa"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
