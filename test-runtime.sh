#!/bin/bash

# Test script for Job Portal runtime

echo "=== Job Portal Runtime Test ===\n"

TESTS_PASSED=0
TESTS_FAILED=0

# TEST 1: Check if docker-compose.yml exists
echo "Test 1: Checking docker-compose.yml exists..."
if [ -f "docker-compose.yml" ]; then
    echo "PASS: docker-compose.yml found"
    ((TESTS_PASSED++))
else
    echo "FAIL: docker-compose.yml not found"
    ((TESTS_FAILED++))
fi

# TEST 2: Check Docker Compose syntax
echo "Test 2: Validating docker-compose.yml syntax..."
if docker compose config > /dev/null 2>&1; then
    echo "PASS: docker-compose.yml syntax is valid"
    ((TESTS_PASSED++))
else
    echo "FAIL: docker-compose.yml has syntax errors"
    ((TESTS_FAILED++))
fi

# TEST 3: Check if services are running
echo "Test 3: Checking if services are running..."
RUNNING_CONTAINERS=$(docker compose ps -q 2>/dev/null | wc -l)
if [ "$RUNNING_CONTAINERS" -gt 0 ]; then
    echo "PASS: $RUNNING_CONTAINERS containers are running"
    ((TESTS_PASSED++))
else
    echo "FAIL: No containers running"
    echo "Run: docker compose up -d"
    ((TESTS_FAILED++))
    exit 1
fi

# TEST 4: Check PostgreSQL
echo "Test 4: Checking PostgreSQL..."
if docker compose exec -T postgres pg_isready -U jobportal > /dev/null 2>&1; then
    echo "PASS: PostgreSQL is running"
    ((TESTS_PASSED++))
else
    echo "FAIL: PostgreSQL connection failed"
    ((TESTS_FAILED++))
fi

# TEST 5: Check Redis
echo "Test 5: Checking Redis..."
if docker compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "PASS: Redis is running"
    ((TESTS_PASSED++))
else
    echo "FAIL: Redis connection failed"
    ((TESTS_FAILED++))
fi

# TEST 6: Test API Gateway Health
echo "Test 6: Testing API Gateway health endpoint..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null)
if [ "$RESPONSE" = "200" ]; then
    echo "PASS: API Gateway is healthy (HTTP $RESPONSE)"
    ((TESTS_PASSED++))
else
    echo "FAIL: API Gateway health check failed (HTTP $RESPONSE)"
    ((TESTS_FAILED++))
fi

# TEST 7: Test Auth Service Health
echo "Test 7: Testing Auth Service health endpoint..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/health 2>/dev/null)
if [ "$RESPONSE" = "200" ]; then
    echo "PASS: Auth Service is healthy (HTTP $RESPONSE)"
    ((TESTS_PASSED++))
else
    echo "FAIL: Auth Service health check failed (HTTP $RESPONSE)"
    ((TESTS_FAILED++))
fi

# TEST 8: Test User Service Health
echo "Test 8: Testing User Service health endpoint..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8002/health 2>/dev/null)
if [ "$RESPONSE" = "200" ]; then
    echo "PASS: User Service is healthy (HTTP $RESPONSE)"
    ((TESTS_PASSED++))
else
    echo "FAIL: User Service health check failed (HTTP $RESPONSE)"
    ((TESTS_FAILED++))
fi

# TEST 9: Test Job Service Health
echo "Test 9: Testing Job Service health endpoint..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8003/health 2>/dev/null)
if [ "$RESPONSE" = "200" ]; then
    echo "PASS: Job Service is healthy (HTTP $RESPONSE)"
    ((TESTS_PASSED++))
else
    echo "FAIL: Job Service health check failed (HTTP $RESPONSE)"
    ((TESTS_FAILED++))
fi

# TEST 10: Test Application Service Health
echo "Test 10: Testing Application Service health endpoint..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8004/health 2>/dev/null)
if [ "$RESPONSE" = "200" ]; then
    echo "PASS: Application Service is healthy (HTTP $RESPONSE)"
    ((TESTS_PASSED++))
else
    echo "FAIL: Application Service health check failed (HTTP $RESPONSE)"
    ((TESTS_FAILED++))
fi

# TEST 11: Test API Docs
echo "Test 11: Testing API Documentation accessibility..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs 2>/dev/null)
if [ "$RESPONSE" = "200" ]; then
    echo "PASS: Swagger UI is accessible at http://localhost:8000/docs"
    ((TESTS_PASSED++))
else
    echo "FAIL: Swagger UI not accessible (HTTP $RESPONSE)"
    ((TESTS_FAILED++))
fi

# Print Summary
echo ""
echo "================================"
echo "Test Summary"
echo "================================"
echo "Passed: $TESTS_PASSED"
echo "Failed: $TESTS_FAILED"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo "All tests passed! Architecture is working!"
    echo ""
    echo "Next Steps:"
    echo "1. View API Documentation: http://localhost:8000/docs"
    echo "2. Check logs: docker compose logs -f"
    echo "3. Test API calls using Swagger UI"
    exit 0
else
    echo ""
    echo "Some tests failed"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check if services are running: docker compose ps"
    echo "2. View logs for errors: docker compose logs"
    echo "3. Restart services: docker compose restart"
    exit 1
fi
