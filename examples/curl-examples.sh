#!/bin/bash

# Curl Examples for Autonomous Incident Analyst API
# These examples demonstrate how to interact with all API endpoints

API_URL="${API_URL:-http://localhost:8000}"

echo "🔗 Using API URL: $API_URL"
echo ""

# ============================================
# Health Check Endpoints
# ============================================

echo "📍 1. Basic Health Check"
echo "curl $API_URL/"
echo ""

echo "📍 2. Detailed Health Status"
echo "curl $API_URL/health | jq"
echo ""

# ============================================
# List Incidents
# ============================================

echo "📍 3. List All Incidents"
echo "curl $API_URL/incidents | jq"
echo ""

echo "📍 4. Get Specific Incident"
echo "curl $API_URL/incidents/1 | jq"
echo ""

# ============================================
# Submit New Incidents
# ============================================

echo "📍 5. Submit Memory Error Incident"
cat << 'EOF'
curl -X POST $API_URL/incident \
  -H "Content-Type: application/json" \
  -d '{
    "logs": "[ERROR] 2024-02-06 10:23:45 - Container killed: OOMKilled\n[ERROR] Memory usage exceeded limit: 512Mi\n[WARN] Pod restarting",
    "metrics": "Memory: 512Mi/512Mi (100%)\nCPU: 85%\nRestarts: 5"
  }' | jq
EOF
echo ""

echo "📍 6. Submit Database Connection Error"
cat << 'EOF'
curl -X POST $API_URL/incident \
  -H "Content-Type: application/json" \
  -d '{
    "logs": "[ERROR] Connection refused: ECONNREFUSED 10.0.0.45:5432\n[ERROR] Database connection failed\n[ERROR] Max retries exceeded",
    "metrics": "Active connections: 0/100\nConnection pool: exhausted"
  }' | jq
EOF
echo ""

echo "📍 7. Submit Disk Space Error"
cat << 'EOF'
curl -X POST $API_URL/incident \
  -H "Content-Type: application/json" \
  -d '{
    "logs": "[ERROR] Disk space critical\n[ERROR] / partition at 98% capacity\n[ERROR] Cannot write to disk",
    "metrics": "Disk usage: 98%\nInodes: 450k/500k\nWrite errors: 15"
  }' | jq
EOF
echo ""

echo "📍 8. Submit Timeout Error"
cat << 'EOF'
curl -X POST $API_URL/incident \
  -H "Content-Type: application/json" \
  -d '{
    "logs": "[ERROR] Request timeout after 30000ms\n[WARN] Upstream service slow\n[ERROR] Circuit breaker opened",
    "metrics": "P99 latency: 45s\nError rate: 23%\nCircuit breaker: OPEN"
  }' | jq
EOF
echo ""

echo "📍 9. Submit Permission Error"
cat << 'EOF'
curl -X POST $API_URL/incident \
  -H "Content-Type: application/json" \
  -d '{
    "logs": "[ERROR] Permission denied accessing S3\n[ERROR] AccessDenied: User does not have s3:GetObject permission",
    "metrics": "Failed requests: 45\nHTTP 403 errors: 45"
  }' | jq
EOF
echo ""

# ============================================
# Apply Fixes
# ============================================

echo "📍 10. Apply Fix to Incident"
cat << 'EOF'
curl -X POST $API_URL/action \
  -H "Content-Type: application/json" \
  -d '{
    "incident_id": 1,
    "fix_applied": "Increased memory limit from 512Mi to 1Gi",
    "new_logs": "[INFO] Container running normally\n[INFO] Memory usage: 650Mi/1Gi"
  }' | jq
EOF
echo ""

echo "📍 11. Apply Multiple Fixes"
cat << 'EOF'
# First fix
curl -X POST $API_URL/action \
  -H "Content-Type: application/json" \
  -d '{
    "incident_id": 2,
    "fix_applied": "Restarted database pod",
    "new_logs": "[INFO] Database pod restarted\n[WARN] Still experiencing connection issues"
  }' | jq

# Second fix
curl -X POST $API_URL/action \
  -H "Content-Type: application/json" \
  -d '{
    "incident_id": 2,
    "fix_applied": "Updated network policy to allow traffic",
    "new_logs": "[INFO] Connection successful\n[INFO] Database responding normally"
  }' | jq
EOF
echo ""

# ============================================
# Resolve Incidents
# ============================================

echo "📍 12. Resolve Incident with Notes"
cat << 'EOF'
curl -X POST $API_URL/resolve \
  -H "Content-Type: application/json" \
  -d '{
    "incident_id": 1,
    "resolution_notes": "Increased memory limit to 1Gi and optimized application memory usage"
  }' | jq
EOF
echo ""

echo "📍 13. Resolve Incident (Simple)"
cat << 'EOF'
curl -X POST $API_URL/resolve \
  -H "Content-Type: application/json" \
  -d '{
    "incident_id": 2,
    "resolution_notes": "Fixed network policy"
  }' | jq
EOF
echo ""

# ============================================
# Delete Incidents (Testing Only)
# ============================================

echo "📍 14. Delete Incident (Testing Only)"
echo "curl -X DELETE $API_URL/incidents/99 | jq"
echo ""

# ============================================
# Complete Workflow Example
# ============================================

echo "📍 15. Complete Workflow (Submit → Fix → Resolve)"
cat << 'EOF'
# Step 1: Submit incident
RESPONSE=$(curl -s -X POST $API_URL/incident \
  -H "Content-Type: application/json" \
  -d '{
    "logs": "[ERROR] Application crash",
    "metrics": "Crash count: 3"
  }')

INCIDENT_ID=$(echo $RESPONSE | jq -r '.incident_id')
echo "Created incident: $INCIDENT_ID"
echo $RESPONSE | jq

# Step 2: Apply fix
curl -s -X POST $API_URL/action \
  -H "Content-Type: application/json" \
  -d "{
    \"incident_id\": $INCIDENT_ID,
    \"fix_applied\": \"Rolled back to previous stable version\"
  }" | jq

# Step 3: Resolve
curl -s -X POST $API_URL/resolve \
  -H "Content-Type: application/json" \
  -d "{
    \"incident_id\": $INCIDENT_ID,
    \"resolution_notes\": \"Application stable after rollback\"
  }" | jq
EOF
echo ""

# ============================================
# Advanced Examples
# ============================================

echo "📍 16. Check Health Before Operations"
cat << 'EOF'
# Check if API is healthy
HEALTH=$(curl -s $API_URL/health)
STATUS=$(echo $HEALTH | jq -r '.status')

if [ "$STATUS" = "healthy" ]; then
  echo "✓ API is healthy, proceeding with operations"
  # Your operations here
else
  echo "✗ API is not healthy"
  exit 1
fi
EOF
echo ""

echo "📍 17. Filter Resolved Incidents"
cat << 'EOF'
curl -s $API_URL/incidents | jq '.incidents[] | select(.status == "resolved")'
EOF
echo ""

echo "📍 18. Get Incident Count by Status"
cat << 'EOF'
curl -s $API_URL/health | jq '.statistics'
EOF
echo ""

echo "📍 19. Extract Suggested Fix from Analysis"
cat << 'EOF'
curl -s -X POST $API_URL/incident \
  -H "Content-Type: application/json" \
  -d '{
    "logs": "[ERROR] Some error",
    "metrics": ""
  }' | jq -r '.suggested_fix'
EOF
echo ""

echo "📍 20. Pretty Print All Incidents"
cat << 'EOF'
curl -s $API_URL/incidents | jq '.incidents[] | {
  id: .id,
  status: .status,
  root_causes: .suspected_root_causes,
  created: .created_at
}'
EOF
echo ""

# ============================================
# Usage Instructions
# ============================================

echo ""
echo "============================================"
echo "📚 How to Use These Examples"
echo "============================================"
echo ""
echo "1. Copy any command and run it in your terminal"
echo "2. Make sure the API is running at $API_URL"
echo "3. Install 'jq' for pretty JSON formatting: brew install jq (Mac) or apt install jq (Linux)"
echo "4. Set custom API URL: export API_URL=https://your-api.com"
echo ""
echo "💡 Tips:"
echo "  - Use | jq for formatted output"
echo "  - Use -s flag for silent mode (no progress bar)"
echo "  - Save incident_id from responses for subsequent operations"
echo "  - Check health endpoint before running tests"
echo ""
