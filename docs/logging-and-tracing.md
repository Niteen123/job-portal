# Logging and Tracing

## Overview
Comprehensive logging and request tracing across all microservices to enable debugging, monitoring, and audit trails.

## Request ID Propagation
- Every request receives a unique `X-Request-ID` header
- This ID is propagated through all downstream service calls
- Enables end-to-end request tracing across services

## Logging Strategy

### Log Levels
- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error messages for errors that occurred
- **CRITICAL**: Critical errors that may cause system failure

### Logged Information
- Request method and path
- Request ID for correlation
- Response status codes
- Execution time
- Error stack traces
- Service-specific business logic events

## Middleware

### Request ID Middleware
- Adds or extracts `X-Request-ID` header
- Ensures all requests have unique identifiers
- Passes ID through logging context

### Logging Middleware
- Logs all HTTP requests and responses
- Records request duration
- Captures error information
- Includes request ID in all log entries

## Monitoring
- Services expose `/health` endpoint for monitoring
- Log aggregation ready (centralized logging to be implemented)
- Metrics collection ready for Prometheus integration
