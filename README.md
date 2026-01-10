# Job Portal - Microservices Application

A modern microservices-based job portal application built with FastAPI and Docker.

## Architecture

The application consists of multiple independent microservices:

- **API Gateway** (Port 8000): Central entry point for all requests
- **Auth Service** (Port 8001): Authentication and authorization
- **User Service** (Port 8002): User profile management
- **Job Service** (Port 8003): Job listings management
- **Application Service** (Port 8004): Job applications handling
- **Frontend Service** (Port 3000): Web interface

## Quick Start

### Prerequisites
- Docker
- Docker Compose
- Python 3.12+

### Running the Application

```bash
# Start all services
docker-compose up

# Or in detached mode
docker-compose up -d
```

All services will be available at:
- Frontend: http://localhost:3000
- API Gateway: http://localhost:8000
- Auth Service: http://localhost:8001
- User Service: http://localhost:8002
- Job Service: http://localhost:8003
- Application Service: http://localhost:8004

### Health Check

Each service exposes a health endpoint:
```bash
curl http://localhost:8000/health
```

## Project Structure

```
job-portal/
├── api-gateway/          # API Gateway service
├── auth-service/         # Authentication service
├── user-service/         # User management service
├── job-service/          # Job listings service
├── application-service/  # Job applications service
├── frontend-service/     # Frontend service
├── docs/                 # Documentation
└── docker-compose.yml    # Docker Compose configuration
```

## Documentation

See the `docs/` folder for:
- [Architecture Overview](docs/architecture.md)
- [API Contracts](docs/api-contracts.md)
- [Logging and Tracing](docs/logging-and-tracing.md)
- [Async Events and Message Queues](docs/async-events.md)

## Development

### Local Development Setup

1. Each service has its own `pyproject.toml` with dependencies
2. Use `uv` for package management (modern Python package manager)
3. Run individual services with:

```bash
cd api-gateway
uv run uvicorn app.main:app --reload
```

### Testing

Run tests for each service:

```bash
cd api-gateway
pytest tests/
```

## API Endpoints

### Auth Service
- `POST /login`: User login

### User Service
- `GET /users/{user_id}`: Get user details

### Job Service
- `GET /jobs`: List all jobs

### Application Service
- `POST /applications`: Submit job application

## Features

- ✅ Microservices architecture
- ✅ API Gateway pattern for request routing
- ✅ Request ID tracking across services
- ✅ Structured logging and middleware
- ✅ Docker containerization
- ✅ Health check endpoints
- ✅ Error handling and service resilience
- 🚀 Async events and message queues (planned)
- 🚀 Database integration (planned)
- 🚀 Authentication with JWT (planned)

## Environment Variables

Services use the following environment variables (see `docker-compose.yml`):

- `AUTH_SERVICE_URL`: URL for Auth Service
- `USER_SERVICE_URL`: URL for User Service
- `JOB_SERVICE_URL`: URL for Job Service
- `APPLICATION_SERVICE_URL`: URL for Application Service

## Contributing

1. Create a feature branch
2. Make your changes
3. Test locally with Docker Compose
4. Commit and push

## License

MIT
