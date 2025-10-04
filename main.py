"""
Health API Service

A simple REST API service that provides health check functionality.
This service implements a GET /health endpoint that returns the current
status of the application along with system information.

Author: DevOps Course Student
Date: 2025-01-13
"""

import logging
import sys
from datetime import datetime, timezone
from typing import Dict, Any
import platform
import psutil

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


class HealthService:
    """Service class for health check functionality."""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """
        Gather system information for health check.
        
        Returns:
            Dict containing system information
        """
        try:
            return {
                "python_version": sys.version,
                "platform": platform.platform(),
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total,
                "memory_available": psutil.virtual_memory().available,
                "disk_usage": psutil.disk_usage('/').percent
            }
        except Exception as e:
            logger.error(f"Error gathering system info: {e}")
            return {"error": "Unable to gather system information"}


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


@app.get("/health", response_model=Dict[str, Any])
async def health_check():
    """
    Health check endpoint that returns the current status of the application.
    
    Returns:
        JSON response with health status and system information
        
    Raises:
        HTTPException: If there's an error during health check
    """
    try:
        logger.info("Health check requested")
        
        # Get current timestamp in ISO format
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Gather system information
        system_info = HealthService.get_system_info()
        
        # Prepare health response
        health_response = {
            "status": "Healthy",
            "timestamp": timestamp,
            "system_info": system_info
        }
        
        logger.info("Health check completed successfully")
        return health_response
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )


@app.get("/health/simple", response_model=Dict[str, str])
async def simple_health_check():
    """
    Simple health check endpoint with minimal response.
    
    Returns:
        JSON response with basic health status
    """
    try:
        timestamp = datetime.now(timezone.utc).isoformat()
        return {
            "status": "Healthy",
            "timestamp": timestamp
        }
    except Exception as e:
        logger.error(f"Simple health check failed: {e}")
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
