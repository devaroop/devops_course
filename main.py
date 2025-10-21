"""
Health API Service

A simple REST API service that provides health check functionality.
This service implements a GET /health endpoint that returns the current
status of the application.

Author: DevOps Course Student
Date: 2025-01-13
"""

import logging
from datetime import datetime, timezone
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="Health API Service",
    description="A simple health check API service for DevOps course",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/", response_model=Dict[str, str])
async def root():
    """
    Root endpoint that provides basic API information.
    
    Returns:
        Dict with API information
    """
    return {
        "message": "Health API Service",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """
    Health check endpoint that returns the current status of the application.
    
    Returns:
        JSON response with basic health status
    """
    try:
        logger.info("Health check requested")
        timestamp = datetime.now(timezone.utc).isoformat()
        
        health_response = {
            "status": "Healthy",
            "timestamp": timestamp
        }
        
        logger.info("Health check completed successfully")
        return health_response
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Health check failed"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled exceptions.
    
    Args:
        request: The request that caused the exception
        exc: The exception that occurred
        
    Returns:
        JSON response with error details
    """
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred"
        }
    )



