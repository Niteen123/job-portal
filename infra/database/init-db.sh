#!/bin/bash

# This script runs inside the PostgreSQL container on first initialization
# It creates the database and runs the schema

set -e

echo "Setting up Job Portal Database..."

# Create the main database if it doesn't exist
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    SELECT 'CREATE DATABASE job_portal'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'job_portal')\gexec
EOSQL

# Create alias database for backward compatibility
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    SELECT 'CREATE DATABASE jobportal TEMPLATE job_portal'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'jobportal')\gexec
EOSQL

echo "Databases 'job_portal' and 'jobportal' are ready"
