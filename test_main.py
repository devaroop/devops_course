"""
Unit tests for the Health API Service.

This module contains comprehensive tests for all API endpoints,
error handling scenarios, and edge cases.

Author: DevOps Course Student
Date: 2025-01-13
"""

import pytest
import json
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app, HealthService

# Initialize test client
client = TestClient(app)


class TestHealthService:
    """Test cases for the HealthService class."""
    
    def test_get_system_info_success(self):
        """Test successful system info gathering."""
        system_info = HealthService.get_system_info()
        
        assert isinstance(system_info, dict)
        assert "python_version" in system_info
        assert "platform" in system_info
        assert "cpu_count" in system_info
        assert "memory_total" in system_info
        assert "memory_available" in system_info
        assert "disk_usage" in system_info
    
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    @patch('psutil.cpu_count')
    def test_get_system_info_with_mock(self, mock_cpu_count, mock_disk_usage, mock_memory):
        """Test system info gathering with mocked psutil calls."""
        # Setup mocks
        mock_cpu_count.return_value = 4
        mock_memory.return_value = MagicMock(total=8589934592, available=4294967296)
        mock_disk_usage.return_value = MagicMock(percent=50.0)
        
        system_info = HealthService.get_system_info()
        
        assert system_info["cpu_count"] == 4
        assert system_info["memory_total"] == 8589934592
        assert system_info["memory_available"] == 4294967296
        assert system_info["disk_usage"] == 50.0


class TestRootEndpoint:
    """Test cases for the root endpoint."""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns correct information."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Health API Service"
        assert data["version"] == "1.0.0"
        assert data["docs"] == "/docs"


class TestHealthEndpoint:
    """Test cases for the health check endpoint."""
    
    def test_health_endpoint_success(self):
        """Test successful health check."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "status" in data
        assert "timestamp" in data
        assert "system_info" in data
        
        # Check status value
        assert data["status"] == "Healthy"
        
        # Check timestamp format (ISO format)
        timestamp = datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
        assert isinstance(timestamp, datetime)
        
        # Check system info structure
        system_info = data["system_info"]
        assert isinstance(system_info, dict)
        assert "python_version" in system_info
        assert "platform" in system_info
    
    def test_health_endpoint_timestamp_format(self):
        """Test that timestamp is in correct ISO format."""
        response = client.get("/health")
        data = response.json()
        
        # Parse timestamp to ensure it's valid ISO format
        timestamp_str = data["timestamp"]
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        
        # Verify it's a recent timestamp (within last minute)
        now = datetime.now(timezone.utc)
        time_diff = abs((now - timestamp).total_seconds())
        assert time_diff < 60  # Should be within 1 minute
    
    @patch('main.HealthService.get_system_info')
    def test_health_endpoint_system_info_error(self, mock_get_system_info):
        """Test health endpoint when system info gathering fails."""
        mock_get_system_info.side_effect = Exception("System info error")
        
        response = client.get("/health")
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "System info error" in data["detail"]


class TestSimpleHealthEndpoint:
    """Test cases for the simple health check endpoint."""
    
    def test_simple_health_endpoint_success(self):
        """Test successful simple health check."""
        response = client.get("/health/simple")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "status" in data
        assert "timestamp" in data
        
        # Check status value
        assert data["status"] == "Healthy"
        
        # Check timestamp format
        timestamp = datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
        assert isinstance(timestamp, datetime)
    
    def test_simple_health_endpoint_minimal_response(self):
        """Test that simple health endpoint returns minimal response."""
        response = client.get("/health/simple")
        data = response.json()
        
        # Should only have status and timestamp
        assert len(data) == 2
        assert "status" in data
        assert "timestamp" in data
        assert "system_info" not in data


class TestErrorHandling:
    """Test cases for error handling scenarios."""
    
    def test_nonexistent_endpoint(self):
        """Test that non-existent endpoints return 404."""
        response = client.get("/nonexistent")
        
        assert response.status_code == 404
    
    @patch('main.datetime')
    def test_health_endpoint_timestamp_error(self, mock_datetime):
        """Test health endpoint when timestamp generation fails."""
        mock_datetime.now.side_effect = Exception("Timestamp error")
        
        response = client.get("/health")
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Timestamp error" in data["detail"]
    
    def test_health_endpoint_response_structure(self):
        """Test that health endpoint response has correct structure."""
        response = client.get("/health")
        data = response.json()
        
        # Verify all expected keys are present
        expected_keys = {"status", "timestamp", "system_info"}
        assert set(data.keys()) == expected_keys
        
        # Verify system_info has expected structure
        system_info = data["system_info"]
        expected_system_keys = {
            "python_version", "platform", "cpu_count",
            "memory_total", "memory_available", "disk_usage"
        }
        assert set(system_info.keys()) == expected_system_keys


class TestAPIDocumentation:
    """Test cases for API documentation endpoints."""
    
    def test_docs_endpoint_accessible(self):
        """Test that API documentation is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_endpoint_accessible(self):
        """Test that ReDoc documentation is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200


class TestEdgeCases:
    """Test cases for edge cases and boundary conditions."""
    
    def test_concurrent_health_checks(self):
        """Test multiple concurrent health check requests."""
        import threading
        import time
        
        results = []
        
        def make_request():
            response = client.get("/health")
            results.append(response.status_code)
        
        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 5
    
    def test_health_endpoint_performance(self):
        """Test that health endpoint responds quickly."""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        assert response.status_code == 200
        # Should respond within 1 second
        assert (end_time - start_time) < 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
