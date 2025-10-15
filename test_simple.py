#!/usr/bin/env python3
"""
Simple test script to verify the simplified Health API works correctly.
"""

import json
from fastapi.testclient import TestClient
from main import app

def test_health_endpoint():
    """Test the simplified health endpoint."""
    client = TestClient(app)
    
    print("Testing simplified Health API...")
    
    # Test root endpoint
    print("\n1. Testing root endpoint (GET /)")
    response = client.get("/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test health endpoint
    print("\n2. Testing health endpoint (GET /health)")
    response = client.get("/health")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    # Verify response structure
    assert response.status_code == 200
    assert "status" in data
    assert "timestamp" in data
    assert data["status"] == "Healthy"
    assert len(data) == 2  # Only status and timestamp
    
    print("\n✅ All tests passed! The simplified Health API is working correctly.")
    pint(f"Response contains: {list(data.keys())}")

if __name__ == "__main__":
    test_health_endpoint()
