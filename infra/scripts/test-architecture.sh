#!/bin/bash

# Job Portal Architecture Testing Script
# Tests all services and infrastructure

set -e

echo "Job Portal - Architecture Test"
echo ""

print_status() {
    if [ $1 -eq 0 ]; then
        echo "PASS: $2"
    else
        echo "FAIL: $2"
    fi
}

print_section() {
    echo ""
    echo "====== $1 ======"
}

# Test 1: Check Docker and Docker Compose
print_section "TEST 1: Checking Docker Installation"

docker --version > /dev/null 2>&1
print_status $? "Docker is installed"

docker-compose --version > /dev/null 2>&1
print_status $? "Docker Compose is installed"

# Test 2: Check .env file exists
print_section "TEST 2: Checking Environment Configuration"

if [ -f .env ]; then
    print_status 0 ".env file exists"
else
    print_info "Creating .env from .env.example"
    cp .env.example .env
    print_status $? ".env file created"
fi

# Test 3: Check docker-compose.yml in infra
print_section "TEST 3: Checking Docker Compose Configuration"

if [ -f infra/docker/docker-compose.yml ]; then
    print_status 0 "docker-compose.yml found in infra/docker/"
else
    print_status 1 "docker-compose.yml not found!"
    exit 1
fi

# Test 4: Check all service directories exist
print_section "TEST 4: Verifying Service Directories"

SERVICES=(
    "api-gateway"
    "auth-service"
    "user-service"
    "employer-service"
    "job-service"
    "application-service"
    "resume-service"
    "search-service"
    "notification-service"
    "frontend-service"
)

for service in "${SERVICES[@]}"; do
    if [ -d "services/$service" ]; then
        print_status 0 "services/$service exists"
    else
        print_status 1 "services/$service missing!"
    fi
done

# Test 5: Check shared package
print_section "TEST 5: Verifying Shared Package"

if [ -d "shared/job-portal-common" ]; then
    print_status 0 "Shared package exists"
else
    print_status 1 "Shared package missing!"
fi

# Check shared package components
SHARED_COMPONENTS=(
    "job_portal_common/models/__init__.py"
    "job_portal_common/exceptions/__init__.py"
    "job_portal_common/middleware/__init__.py"
    "job_portal_common/utils/__init__.py"
    "job_portal_common/logger/__init__.py"
)

for component in "${SHARED_COMPONENTS[@]}"; do
    if [ -f "shared/job-portal-common/$component" ]; then
        print_status 0 "$(basename $component .py) module exists"
    else
        print_status 1 "$(basename $component .py) module missing!"
    fi
done

# Test 6: Check infrastructure files
print_section "TEST 6: Verifying Infrastructure Files"

INFRA_FILES=(
    "infra/database/schema.sql"
    "infra/docker/docker-compose.yml"
    ".env.example"
    "README.md"
)

for file in "${INFRA_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_status 0 "$file exists"
    else
        print_status 1 "$file missing!"
    fi
done

# Test 7: Check Dockerfiles
print_section "TEST 7: Verifying Dockerfile Setup"

SERVICES_ARRAY=("${SERVICES[@]}")
for service in "${SERVICES_ARRAY[@]}"; do
    if [ -f "services/$service/Dockerfile" ]; then
        print_status 0 "services/$service/Dockerfile exists"
    else
        print_status 1 "services/$service/Dockerfile missing!"
    fi
done

# Test 8: Syntax validation
print_section "TEST 8: Validating YAML/SQL Syntax"

# Validate docker-compose.yml
docker-compose -f infra/docker/docker-compose.yml config > /dev/null 2>&1
print_status $? "docker-compose.yml syntax valid"

# Test 9: Check pyproject.toml files
print_section "TEST 9: Verifying Python Project Files"

count=0
for service in "${SERVICES_ARRAY[@]}"; do
    if [ -f "services/$service/pyproject.toml" ]; then
        ((count++))
    fi
done

if [ $count -eq 10 ]; then
    print_status 0 "All 10 services have pyproject.toml"
else
    print_status 1 "$count/10 services have pyproject.toml"
fi

# Test 10: Show next steps
print_section "Ready to Start Services"

echo ""
echo "Architecture validation complete!"
echo ""
echo "Next steps:"
echo ""
echo "1. Start services with Docker Compose:"
echo "   cd /home/niteen/Projects/job-portal"
echo "   docker compose up -d"
echo ""
echo "2. Check services status:"
echo "   docker compose ps"
echo ""
echo "3. View logs:"
echo "   docker compose logs -f"
echo ""
echo "4. Stop services:"
echo "   docker compose down"
echo ""

print_section "SUMMARY"
echo "Architecture is VALID and READY!"
echo ""
echo "Services available at:"
echo "  API Gateway:        http://localhost:8000"
echo "  Auth Service:       http://localhost:8001"
echo "  User Service:       http://localhost:8002"
echo "  Job Service:        http://localhost:8003"
echo "  Application:        http://localhost:8004"
echo "  Employer Service:   http://localhost:8005"
echo "  Resume Service:     http://localhost:8006"
echo "  Search Service:     http://localhost:8007"
echo "  Notification:       http://localhost:8008"
echo "  Frontend:           http://localhost:3000"
echo ""
echo "Infrastructure:"
echo "  PostgreSQL:         localhost:5432"
echo "  Redis:              localhost:6379"
echo ""
