# Microservices Architecture Guide

## Directory Structure

```
job-portal/
│
├── services/                          # All microservices
│   ├── api-gateway/                   # Request routing & aggregation
│   ├── auth-service/                  # User authentication
│   ├── user-service/                  # Job seeker profiles
│   ├── employer-service/              # Company profiles
│   ├── job-service/                   # Job postings
│   ├── application-service/           # Job applications
│   ├── resume-service/                # Resume management
│   ├── search-service/                # Advanced search (Week 5)
│   ├── notification-service/          # Email/SMS (Week 5)
│   └── frontend-service/              # Frontend placeholder
│
├── shared/                            # Shared code across services
│   └── job-portal-common/
│       ├── job_portal_common/
│       │   ├── models/               # Pydantic schemas
│       │   ├── exceptions/           # Common exceptions
│       │   ├── middleware/           # Shared middleware
│       │   ├── utils/                # Utilities (JWT, password, etc)
│       │   ├── logger/               # Logging setup
│       │   └── __init__.py
│       ├── pyproject.toml
│       └── README.md
│
├── infra/                            # Infrastructure & deployment
│   ├── database/
│   │   ├── schema.sql                # PostgreSQL schema
│   │   ├── migrations/               # Alembic migrations
│   │   │   └── versions/
│   │   └── seeds/                    # Test data
│   ├── docker/
│   │   ├── docker-compose.yml        # Main orchestration
│   │   ├── docker-compose.dev.yml    # Development
│   │   ├── docker-compose.staging.yml
│   │   └── docker-compose.prod.yml
│   ├── kubernetes/                   # K8s manifests (optional)
│   ├── monitoring/                   # Logging, metrics
│   ├── nginx/                        # Reverse proxy (optional)
│   └── scripts/                      # Automation scripts
│
├── docs/                             # Documentation
│   ├── architecture.md               # System design
│   ├── api-contracts/                # API specifications
│   │   ├── auth-service.md
│   │   ├── user-service.md
│   │   ├── employer-service.md
│   │   ├── job-service.md
│   │   ├── application-service.md
│   │   └── resume-service.md
│   ├── database/
│   │   └── schema-diagram.md
│   ├── setup.md                      # Setup guide
│   └── contributing.md
│
├── tests/                            # Integration & e2e tests
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── fixtures/
│   └── conftest.py
│
├── .github/                          # CI/CD
│   └── workflows/
│       ├── test.yml
│       ├── build.yml
│       └── deploy.yml
│
├── .env.example                      # Environment template
├── .env                              # Environment vars (not in git)
├── .gitignore
├── docker-compose.yml                # Quick reference symlink
├── README.md                         # Main readme
└── CONTRIBUTING.md
```

## Each Microservice Structure

```
service-name/
├── app/
│   ├── __init__.py
│   ├── main.py                       # FastAPI app
│   │
│   ├── core/
│   │   ├── config.py                 # Settings & env vars
│   │   ├── security.py               # Auth logic
│   │   ├── exceptions.py             # Service-specific errors
│   │   └── logger.py                 # Logging setup
│   │
│   ├── database/
│   │   ├── db.py                     # Connection & session
│   │   ├── base.py                   # Base ORM model
│   │   └── models.py                 # SQLAlchemy models
│   │
│   ├── schemas/                      # Request/Response models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── job.py
│   │   └── base.py
│   │
│   ├── services/                     # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── base_service.py
│   │
│   ├── routes/                       # API endpoints
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── job.py
│   │   └── health.py
│   │
│   ├── middleware/
│   │   ├── auth.py
│   │   ├── error_handler.py
│   │   ├── logging.py
│   │   └── request_id.py
│   │
│   ├── utils/
│   │   ├── decorators.py
│   │   ├── validators.py
│   │   └── helpers.py
│   │
│   └── dependencies.py               # FastAPI dependencies
│
├── tests/
│   ├── conftest.py                   # Pytest fixtures
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── migrations/                       # Alembic (optional per service)
│
├── Dockerfile
├── pyproject.toml
├── main.py                           # Entry point
├── .env.example
└── README.md
```

## Communication Flow

```
Client/Frontend
     ↓
[API Gateway:8000] ← Central routing point
     ↓ (routes requests)
     ├→ [Auth Service:8001]
     ├→ [User Service:8002]
     ├→ [Employer Service:8005]
     ├→ [Job Service:8003]
     ├→ [Application Service:8004]
     ├→ [Resume Service:8006]
     ├→ [Search Service:8007]
     └→ [Notification Service:8008]
     ↓
PostgreSQL Database
     ↓
Redis Cache
```

## Service Responsibilities

### Core Services

| Service | Port | Responsibility |
|---------|------|-----------------|
| API Gateway | 8000 | Route requests, authentication, error handling |
| Auth | 8001 | User registration, login, JWT tokens |
| User | 8002 | Job seeker profiles, skills, saved jobs |
| Employer | 8005 | Company profiles, management |
| Job | 8003 | Job CRUD, filtering, views tracking |
| Application | 8004 | Job application tracking, status |
| Resume | 8006 | Resume upload, storage, retrieval |
| Search | 8007 | Advanced search, filters (Week 5+) |
| Notification | 8008 | Email, SMS, notifications (Week 5+) |

## Development Workflow

### 1. Setup Local Environment
```bash
cp .env.example .env
docker-compose up -d  # Start DB, Redis
cd services/auth-service
uv sync
uv run uvicorn app.main:app --reload
```

### 2. Add New Endpoint
1. Create schema in `schemas/`
2. Add route in `routes/`
3. Implement service logic in `services/`
4. Write tests in `tests/`

### 3. Create Database Migration
```bash
cd services/auth-service
alembic revision --autogenerate -m "Add new field"
alembic upgrade head
```

### 4. Test Service
```bash
cd services/auth-service
uv run pytest tests/ -v
curl http://localhost:8001/health
```

## Shared Package Usage

### In any service:
```python
# models/exceptions
from job_portal_common.exceptions import AuthenticationError, NotFoundError

# models/schemas
from job_portal_common.models import UserResponse, StandardResponse

# utilities
from job_portal_common.utils import hash_password, verify_password, create_access_token

# middleware
from job_portal_common.middleware import RequestIDMiddleware, LoggingMiddleware

# logger
from job_portal_common.logger import setup_logger
```

## Key Principles

1. **Service Independence**: Each service owns its data
2. **Shared Code**: Only utilities go in shared package
3. **Logging**: All services log request_id for tracing
4. **Error Handling**: Use common exceptions
5. **Database**: PostgreSQL for all services (shared instance)
6. **Authentication**: JWT tokens verified by gateway
7. **Testing**: Unit tests per service, integration tests in root `/tests`

## Deployment Topology

```
Environment
  ├── Development: docker-compose.dev.yml (local machine)
  ├── Staging: docker-compose.staging.yml (staging server)
  └── Production: docker-compose.prod.yml + K8s (optional)
```

## Monitoring & Logging

- **Logs**: All go to stdout (captured by Docker)
- **Request ID**: Tracked across services for debugging
- **Health Checks**: Each service has `/health` endpoint
- **Metrics**: Prometheus-ready (to add in future)
