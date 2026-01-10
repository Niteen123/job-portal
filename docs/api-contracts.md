# API Contracts

## Auth Service

### Login
- **Endpoint**: `POST /login`
- **Request**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response** (200):
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

## User Service

### Get User
- **Endpoint**: `GET /users/{user_id}`
- **Response** (200):
  ```json
  {
    "id": "integer",
    "name": "string",
    "email": "string"
  }
  ```

## Job Service

### List Jobs
- **Endpoint**: `GET /jobs`
- **Response** (200):
  ```json
  {
    "jobs": [
      {
        "id": "integer",
        "title": "string",
        "description": "string"
      }
    ]
  }
  ```

## Application Service

### Create Application
- **Endpoint**: `POST /applications`
- **Request**:
  ```json
  {
    "job_id": "integer",
    "user_id": "integer"
  }
  ```
- **Response** (201):
  ```json
  {
    "id": "integer",
    "job_id": "integer",
    "user_id": "integer",
    "status": "string"
  }
  ```

## Error Responses

### Service Unavailable
- **Status Code**: 503
- **Response**:
  ```json
  {
    "detail": "Service unavailable"
  }
  ```
