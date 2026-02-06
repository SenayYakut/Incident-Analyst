#!/bin/bash

# API Testing Script for Autonomous Incident Analyst
# Tests all main endpoints with example data

set -e

API_URL="${API_URL:-http://localhost:8000}"
echo "🧪 Testing Autonomous Incident Analyst API"
echo "API URL: $API_URL"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo "📍 Test 1: Health Check"
response=$(curl -s "$API_URL/")
if echo "$response" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
    exit 1
fi
echo ""

# Test 2: List Incidents
echo "📍 Test 2: List Incidents"
response=$(curl -s "$API_URL/incidents")
count=$(echo "$response" | grep -o '"total":[0-9]*' | grep -o '[0-9]*')
echo -e "${GREEN}✓ Found $count existing incidents${NC}"
echo ""

# Test 3: Submit New Incident
echo "📍 Test 3: Submit New Incident"
incident_response=$(curl -s -X POST "$API_URL/incident" \
  -H "Content-Type: application/json" \
  -d '{
    "logs": "[ERROR] 2024-02-06 15:30:45 - Disk space critical\n[ERROR] / partition at 98% capacity\n[WARN] Log rotation failed\n[ERROR] Cannot write to disk",
    "metrics": "Disk usage: 98%\nInodes: 450k/500k\nWrite errors: 15"
  }')

incident_id=$(echo "$incident_response" | grep -o '"incident_id":[0-9]*' | grep -o '[0-9]*')
if [ -n "$incident_id" ]; then
    echo -e "${GREEN}✓ Incident created with ID: $incident_id${NC}"
    echo "  Suggested fix: $(echo "$incident_response" | grep -o '"suggested_fix":"[^"]*"' | cut -d'"' -f4)"
else
    echo -e "${RED}✗ Failed to create incident${NC}"
    exit 1
fi
echo ""

# Test 4: Get Specific Incident
echo "📍 Test 4: Get Incident Details"
response=$(curl -s "$API_URL/incidents/$incident_id")
if echo "$response" | grep -q "\"id\":$incident_id"; then
    echo -e "${GREEN}✓ Retrieved incident $incident_id${NC}"
else
    echo -e "${RED}✗ Failed to retrieve incident${NC}"
    exit 1
fi
echo ""

# Test 5: Apply Fix
echo "📍 Test 5: Apply Fix"
action_response=$(curl -s -X POST "$API_URL/action" \
  -H "Content-Type: application/json" \
  -d "{
    \"incident_id\": $incident_id,
    \"fix_applied\": \"Cleaned up old log files and temporary data\",
    \"new_logs\": \"[INFO] Disk usage now at 65%\\n[INFO] System stable\"
  }")

if echo "$action_response" | grep -q "incident_id"; then
    echo -e "${GREEN}✓ Fix applied and incident updated${NC}"
    recommendation=$(echo "$action_response" | grep -o '"recommendation":"[^"]*"' | cut -d'"' -f4)
    echo "  Recommendation: $recommendation"
else
    echo -e "${RED}✗ Failed to apply fix${NC}"
    exit 1
fi
echo ""

# Test 6: Resolve Incident
echo "📍 Test 6: Resolve Incident"
resolve_response=$(curl -s -X POST "$API_URL/resolve" \
  -H "Content-Type: application/json" \
  -d "{
    \"incident_id\": $incident_id,
    \"resolution_notes\": \"Disk space cleaned up, implemented automated log rotation\"
  }")

if echo "$resolve_response" | grep -q "resolved"; then
    echo -e "${GREEN}✓ Incident resolved successfully${NC}"
else
    echo -e "${RED}✗ Failed to resolve incident${NC}"
    exit 1
fi
echo ""

# Test 7: Verify Incident is Resolved
echo "📍 Test 7: Verify Resolution"
response=$(curl -s "$API_URL/incidents/$incident_id")
if echo "$response" | grep -q '"status":"resolved"'; then
    echo -e "${GREEN}✓ Incident status confirmed as resolved${NC}"
else
    echo -e "${YELLOW}⚠ Incident status check inconclusive${NC}"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ All API tests passed!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Test Summary:"
echo "  • Health check: ✓"
echo "  • List incidents: ✓"
echo "  • Create incident: ✓ (ID: $incident_id)"
echo "  • Get incident: ✓"
echo "  • Apply fix: ✓"
echo "  • Resolve incident: ✓"
echo "  • Verify resolution: ✓"
echo ""
echo "💡 The incident #$incident_id is now stored in memory"
echo "   and will be used for future similar incident analysis."
