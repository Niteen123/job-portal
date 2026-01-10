# Job Portal - Microservices Architecture

## Overview
This is a microservices-based job portal application built with FastAPI and Docker. The architecture consists of multiple independent services that communicate via HTTP.

## Services

### API Gateway
- **Port**: 8000
- **Role**: Central entry point for all client requests
- **Responsibilities**:
  - Route requests to appropriate microservices
  - Handle request/response transformations
  - Implement cross-cutting concerns (logging, request tracking)
  - Error handling and service unavailability management

### Auth Service
- **Port**: 8001
- **Role**: Authentication and authorization
- **Responsibilities**:
  - User login/logout
  - Token generation and validation
  - Session management

### User Service
- **Port**: 8002
- **Role**: User profile management
- **Responsibilities**:
  - User profile CRUD operations
  - User data retrieval

### Job Service
- **Port**: 8003
- **Role**: Job listings management
- **Responsibilities**:
  - Job creation and management
  - Job search and filtering
  - Job details retrieval

### Application Service
- **Port**: 8004
- **Role**: Job applications
- **Responsibilities**:
  - Application submission
  - Application tracking
  - Application status management

### Frontend Service
- **Port**: 3000
- **Role**: User interface
- **Responsibilities**:
  - Web interface for job portal

## Communication Pattern
- Services communicate via HTTP REST APIs
- API Gateway proxies all client requests to appropriate services
- Service-to-service communication through HTTP clients

## Deployment
- All services are containerized using Docker
- Orchestration via Docker Compose
- Environment-based configuration for service URLs

## Technology Stack
- **Framework**: FastAPI
- **Language**: Python 3.12+
- **Package Manager**: uv
- **Server**: Uvicorn
- **Containerization**: Docker
- **Orchestration**: Docker Compose
