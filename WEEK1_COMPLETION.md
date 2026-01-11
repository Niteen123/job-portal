# Week 1 Completion Summary

**Status:** ✅ Complete  
**Date:** January 11, 2026

## Overview
Week 1 focused on establishing the authentication service foundation with database connectivity, user management, and JWT-based authentication flows. All planned tasks have been implemented and tested.

## Completed Tasks

### 1. Database Layer
- **File:** `services/auth-service/app/core/database.py`
- SQLAlchemy engine connected to PostgreSQL via `DATABASE_URL`
- SessionLocal factory configured
- Declarative base established for ORM models

### 2. User Model
- **File:** `services/auth-service/app/models/user.py`
- SQLAlchemy ORM model with fields:
  - `id` (PK, auto-increment)
  - `email` (unique)
  - `password_hash` (hashed password storage)
  - `full_name`
  - `role` (employer/job_seeker)
  - `is_active` (boolean)
  - `created_at`, `updated_at` (timestamps)

### 3. Password Hashing
- **File:** `services/auth-service/app/utils/password.py`
- `hash_password(password: str) -> str` - SHA-256 hashing with salt
- `verify_password(password: str, password_hash: str) -> bool` - constant-time comparison
- *Note: Current implementation uses SHA-256 for demo stability. Consider upgrading to bcrypt/argon2 for production.*

### 4. JWT Token Management
- **File:** `services/auth-service/app/utils/jwt.py`
- `create_access_token(data: dict, expires_delta: timedelta = None) -> str`
- `decode_token(token: str) -> dict` - with expiration validation
- Token algorithm: HS256
- Configurable expiry (default 24 hours)

### 5. Pydantic Schemas
- **File:** `services/auth-service/app/schemas/__init__.py`
- `UserRegister` - email, password, full_name, role
- `UserLogin` - email, password
- `UserResponse` - id, email, full_name, role, is_active, created_at
- `LoginResponse` - access_token, token_type, user
- `TokenData` - sub (user_id)

### 6. Authentication Routes
- **File:** `services/auth-service/app/routes/auth.py`

#### POST /auth/register
- Request body: `{email, password, full_name, role}`
- Returns: 201 Created with `UserResponse`
- Validates email uniqueness
- Hashes password before storage

**Example:**
```bash
curl -X POST http://localhost:8001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secure123","full_name":"John Doe","role":"employer"}'
```

#### POST /auth/login
- Request body: `{email, password}`
- Returns: 200 OK with `LoginResponse` containing JWT token
- Validates credentials
- Generates access token on success

**Example:**
```bash
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secure123"}'
```

### 7. User Routes
- **File:** `services/auth-service/app/routes/user.py`

#### GET /users/profile (Protected)
- Requires: `Authorization: Bearer <token>`
- Returns: Current authenticated user's profile (`UserResponse`)
- Security: JWT token validation via HTTPBearer dependency

**Example:**
```bash
curl -H "Authorization: Bearer eyJhbGci..." http://localhost:8001/users/profile
```

#### GET /users/{user_id} (Public)
- Returns: User profile by ID
- No authentication required
- Returns 404 if user not found

**Example:**
```bash
curl http://localhost:8001/users/1
```

### 8. JWT Validation & Dependency Injection
- **File:** `services/auth-service/app/dependencies.py`
- `get_current_user()` - HTTPBearer token extraction and validation
- Automatically decodes JWT and retrieves user from database
- Raises 403 Forbidden on invalid/expired tokens

### 9. Application Setup
- **File:** `services/auth-service/app/main.py`
- Database table creation on startup: `Base.metadata.create_all(bind=engine)`
- Middleware: Request ID tracking, structured logging
- Routers: Auth routes, user routes
- Health endpoint: `GET /health`

### 10. Configuration
- **File:** `services/auth-service/.env`
- `DATABASE_URL` - PostgreSQL connection
- `SECRET_KEY` - JWT signing key
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token TTL

## Test Results

All endpoints have been manually tested and verified working:

✅ **POST /auth/register** - Creates new user, returns UserResponse (201)  
✅ **POST /auth/login** - Returns JWT token + user data (200)  
✅ **GET /users/profile** - Returns current user (requires Bearer token, 200)  
✅ **GET /users/{id}** - Returns public user profile (200)  
✅ **GET /health** - Service health check (200)  
✅ **Error handling** - Invalid tokens return 403, validation errors return 422  

## Database State
- PostgreSQL `job_portal` database initialized
- `user` table created with proper schema
- Test users created during validation

## Dependencies Added
```
sqlalchemy>=2.0.0
psycopg2-binary
python-jose[cryptography]
passlib[bcrypt]
pydantic[email]
python-dotenv
```

## Architecture Notes

### Authentication Flow
1. User registers via POST /auth/register with credentials
2. Password is hashed with SHA-256 and stored in DB
3. User logs in via POST /auth/login with email/password
4. Server validates credentials and returns JWT token
5. Client includes token in Authorization header: `Bearer <token>`
6. Protected endpoints extract and validate token via HTTPBearer dependency
7. Current user is fetched from DB and made available to route handlers

### Security Considerations
- **Current state (Demo):** SHA-256 with salt
- **Production recommendation:** Upgrade to bcrypt (bcrypt module) or Argon2
- **Token expiry:** 24 hours (configurable)
- **Protected routes:** /users/profile requires valid JWT
- **Password storage:** Never stored in plaintext, always hashed

## Known Limitations & Future Improvements

1. **Password Hashing:** Current SHA-256 implementation should be replaced with bcrypt or Argon2 for production
2. **Email Uniqueness:** Register endpoint now prevents duplicate emails
3. **Token Refresh:** No refresh token mechanism yet (add in Week 2)
4. **Logout:** No logout/token invalidation (add in Week 2)
5. **Password Reset:** Not implemented (add in Week 3)
6. **Rate Limiting:** Not implemented (add in Week 2)
7. **User Roles:** Basic role field exists but no role-based access control (add in Week 2)

## Running Week 1 Tests

```bash
# Start services
docker compose up -d

# Register user
curl -X POST http://localhost:8001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123","full_name":"Test","role":"job_seeker"}'

# Login
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123"}'

# Get profile with token
curl -H "Authorization: Bearer <token>" http://localhost:8001/users/profile
```

## Files Created/Modified

### Created
- `services/auth-service/app/core/database.py`
- `services/auth-service/app/models/user.py`
- `services/auth-service/app/utils/password.py`
- `services/auth-service/app/utils/jwt.py`
- `services/auth-service/app/schemas/__init__.py`
- `services/auth-service/app/routes/auth.py`
- `services/auth-service/app/routes/user.py`
- `services/auth-service/app/routes/__init__.py`
- `services/auth-service/app/dependencies.py`

### Modified
- `services/auth-service/pyproject.toml` - Added dependencies
- `services/auth-service/app/main.py` - DB init, router registration
- `.env` - Database and JWT configuration

## Next Steps (Week 2)
- Implement refresh tokens and logout
- Add role-based access control (RBAC)
- Add rate limiting to auth endpoints
- Create job application service with Job model
- Set up job routes (POST /jobs, GET /jobs, GET /jobs/{id})
- Integrate with API Gateway
