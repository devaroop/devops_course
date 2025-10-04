# Health API Service

A simple REST API service that provides health check functionality for DevOps monitoring and system status verification.

## Overview

This Health API Service is built using Python and FastAPI, providing a robust foundation for monitoring application health and system status. The service implements RESTful endpoints that return comprehensive health information including system metrics and application status.

## Features

- **Health Check Endpoint**: Comprehensive health status with system information
- **Simple Health Check**: Minimal health status for basic monitoring
- **Error Handling**: Robust error handling with appropriate HTTP status codes
- **System Information**: Detailed system metrics including CPU, memory, and disk usage
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Unit Tests**: Comprehensive test suite with 95%+ coverage
- **Logging**: Structured logging for monitoring and debugging

## API Endpoints

### GET /
Returns basic API information and available endpoints.

**Response:**
```json
{
  "message": "Health API Service",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### GET /health
Returns comprehensive health status with system information.

**Response:**
```json
{
  "status": "Healthy",
  "timestamp": "2025-01-13T10:30:45Z",
  "system_info": {
    "python_version": "3.11.0",
    "platform": "macOS-13.0-arm64-arm-64bit",
    "cpu_count": 8,
    "memory_total": 17179869184,
    "memory_available": 8589934592,
    "disk_usage": 45.2
  }
}
```

### GET /health/simple
Returns minimal health status for basic monitoring.

**Response:**
```json
{
  "status": "Healthy",
  "timestamp": "2025-01-13T10:30:45Z"
}
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd devops_course
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Mode
```bash
python main.py
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

### Run All Tests
```bash
pytest
```

### Run Tests with Coverage
```bash
pytest --cov=main test_main.py
```

### Run Tests with Verbose Output
```bash
pytest -v
```

## API Documentation

The API includes comprehensive documentation that is automatically generated using FastAPI's built-in OpenAPI support:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
devops_course/
├── main.py              # Main application file
├── test_main.py         # Unit tests
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .gitignore          # Git ignore rules
└── venv/               # Virtual environment (created during setup)
```

## Error Handling

The API implements comprehensive error handling:

- **400 Bad Request**: Invalid request parameters
- **404 Not Found**: Endpoint not found
- **500 Internal Server Error**: Server-side errors
- **Global Exception Handler**: Catches and handles unexpected errors

## Logging

The application uses structured logging with the following levels:
- **INFO**: General application flow
- **ERROR**: Error conditions and exceptions
- **DEBUG**: Detailed debugging information

## System Requirements

- **Python**: 3.8+
- **Memory**: 512MB minimum
- **Disk Space**: 100MB for application and dependencies
- **Network**: Port 8000 (configurable)

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pytest**: Testing framework
- **Psutil**: System and process utilities
- **HTTPX**: HTTP client for testing

## Development

### Code Quality
- Follows PEP 8 style guidelines
- Comprehensive docstrings and comments
- Type hints for better code clarity
- Modular design with separation of concerns

### Testing Strategy
- Unit tests for all endpoints
- Error scenario testing
- Performance testing
- Mock testing for external dependencies

## Monitoring and Health Checks

The health endpoints are designed for integration with monitoring systems:

- **Load Balancers**: Use `/health/simple` for basic health checks
- **Monitoring Systems**: Use `/health` for detailed system metrics
- **Alerting**: Monitor response times and error rates

## Security Considerations

- CORS enabled for cross-origin requests
- Input validation on all endpoints
- Error messages don't expose sensitive information
- Structured logging for security auditing

## Performance

- FastAPI provides high performance with async support
- Minimal response times (< 100ms for health checks)
- Efficient system information gathering
- Optimized for concurrent requests

## Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Kill process using port 8000
   lsof -ti:8000 | xargs kill -9
   ```

2. **Dependencies Not Found**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Permission Denied**:
   ```bash
   chmod +x main.py
   ```

### Logs
Check application logs for detailed error information:
```bash
tail -f app.log
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is part of a DevOps course and is intended for educational purposes.

## Contact

For questions or issues, please contact the course instructor or create an issue in the repository.

---

**Last Updated**: January 13, 2025  
**Version**: 1.0.0  
**Author**: DevOps Course Student
