# API Examples

This directory contains examples and sample data for testing the Autonomous Incident Analyst API.

## Files

### `sample-incidents.json`
Pre-defined incident scenarios with expected root causes. These represent common types of errors you might encounter in production systems:

- Memory (OOM) errors
- Database connection failures
- Request timeouts
- Disk space issues
- Permission errors
- Application crashes
- Certificate expiration
- Rate limiting
- Network timeouts
- Configuration errors

Each example includes:
- Realistic log messages
- Relevant metrics
- Expected root causes for validation

### `curl-examples.sh`
Comprehensive collection of curl commands demonstrating all API endpoints. Includes:

- Health check examples
- Incident listing and retrieval
- Incident submission (various types)
- Fix application
- Incident resolution
- Complete workflow examples
- Advanced querying with jq

## Usage

### View Examples

```bash
# Display all curl examples
cat examples/curl-examples.sh

# View specific sections
grep "📍" examples/curl-examples.sh
```

### Run Examples

```bash
# Make sure API is running first
cd backend && uvicorn main:app --reload

# In another terminal, run examples
./examples/curl-examples.sh
```

### Test with Sample Data

```bash
# Submit a sample incident
curl -X POST http://localhost:8000/incident \
  -H "Content-Type: application/json" \
  -d @examples/sample-incidents.json
```

### Interactive Testing

```bash
# Use the automated test script instead
./test-api.sh
```

## Example Workflows

### Simple Workflow

```bash
# 1. Submit incident
RESPONSE=$(curl -s -X POST http://localhost:8000/incident \
  -H "Content-Type: application/json" \
  -d '{
    "logs": "[ERROR] OOMKilled",
    "metrics": "Memory: 100%"
  }')

# 2. Get incident ID
ID=$(echo $RESPONSE | jq -r '.incident_id')

# 3. Apply fix
curl -s -X POST http://localhost:8000/action \
  -H "Content-Type: application/json" \
  -d "{
    \"incident_id\": $ID,
    \"fix_applied\": \"Increased memory\"
  }" | jq

# 4. Resolve
curl -s -X POST http://localhost:8000/resolve \
  -H "Content-Type: application/json" \
  -d "{
    \"incident_id\": $ID,
    \"resolution_notes\": \"Memory optimized\"
  }" | jq
```

### Testing All Sample Incidents

```bash
# Loop through all sample incidents
jq -c '.examples[]' examples/sample-incidents.json | while read incident; do
  NAME=$(echo $incident | jq -r '.name')
  REQUEST=$(echo $incident | jq -c '.request')
  
  echo "Testing: $NAME"
  curl -s -X POST http://localhost:8000/incident \
    -H "Content-Type: application/json" \
    -d "$REQUEST" | jq '.suggested_fix'
  echo ""
done
```

## Tips

### Pretty Print with jq

```bash
# Install jq
# macOS: brew install jq
# Ubuntu: apt install jq
# Fedora: dnf install jq

# Use with curl
curl http://localhost:8000/incidents | jq
```

### Save Responses

```bash
# Save to file
curl http://localhost:8000/incidents > incidents.json

# Format and save
curl http://localhost:8000/incidents | jq > incidents-pretty.json
```

### Environment Variables

```bash
# Set custom API URL
export API_URL=https://your-api.com

# Use in examples
curl $API_URL/health | jq
```

### Error Handling

```bash
# Check HTTP status
curl -w "\nHTTP Status: %{http_code}\n" http://localhost:8000/health

# Include headers
curl -i http://localhost:8000/health

# Verbose output
curl -v http://localhost:8000/health
```

## Integration Testing

You can use these examples to:

1. **Validate API behavior**: Ensure responses match expected format
2. **Load testing**: Submit multiple incidents rapidly
3. **CI/CD pipelines**: Automated API validation
4. **Development**: Quick testing during development

## Creating Your Own Examples

### Custom Incident

```json
{
  "name": "My Custom Error",
  "request": {
    "logs": "[ERROR] Your log messages here\n[WARN] Warning message",
    "metrics": "CPU: 90%\nMemory: 75%"
  },
  "expected_causes": [
    "Cause 1",
    "Cause 2"
  ]
}
```

Add to `sample-incidents.json` and test!

## Postman Collection

Want a Postman collection? Export these curl commands:

```bash
# Use Postman's "Import" → "Raw text" feature
# Copy curl commands from curl-examples.sh
```

Or create a collection:
1. Create new collection in Postman
2. Add requests for each endpoint
3. Use environments for API_URL
4. Add tests for validation

## Advanced Usage

### Rate Limiting Test

```bash
# Submit 100 incidents quickly
for i in {1..100}; do
  curl -s -X POST http://localhost:8000/incident \
    -H "Content-Type: application/json" \
    -d '{
      "logs": "[ERROR] Test incident '$i'",
      "metrics": ""
    }' &
done
wait
```

### Memory Analysis Test

```bash
# Submit only memory-related incidents
jq -c '.examples[] | select(.name | contains("Memory"))' \
  examples/sample-incidents.json | while read incident; do
  REQUEST=$(echo $incident | jq -c '.request')
  curl -s -X POST http://localhost:8000/incident \
    -H "Content-Type: application/json" \
    -d "$REQUEST" | jq
done
```

### Similarity Testing

```bash
# Submit similar incidents to test memory retrieval
curl -s -X POST http://localhost:8000/incident \
  -H "Content-Type: application/json" \
  -d '{
    "logs": "[ERROR] OOMKilled",
    "metrics": "Memory: 100%"
  }' | jq '.similar_incidents'
```

## Need Help?

- Full API documentation: http://localhost:8000/docs
- Project README: [../README.md](../README.md)
- Automated tests: [../test-api.sh](../test-api.sh)

## Contributing

Have useful examples to add? See [../CONTRIBUTING.md](../CONTRIBUTING.md)!
