#!/bin/bash

echo "🧪 Testing Job Portal Services..."

echo -e "\n✓ Health Checks:"
curl -s http://localhost:8000/health | jq .
curl -s http://localhost:8001/health | jq .

echo -e "\n✓ Login Endpoint:"
curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"niteen","password":"pass123"}' | jq .

echo ""
echo "Tests Complete!"

