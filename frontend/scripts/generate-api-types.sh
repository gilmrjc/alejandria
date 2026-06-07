#!/bin/bash
# Generate TypeScript types from OpenAPI schema
# This script downloads openapi.json from the running API and generates types

set -e

API_URL="${VITE_API_URL:-http://localhost:8000}"
OPENAPI_URL="${API_URL}/openapi.json"
OUTPUT_DIR="./src/types"
OUTPUT_FILE="${OUTPUT_DIR}/api.ts"

echo "Downloading OpenAPI schema from ${OPENAPI_URL}..."

# Download openapi.json
curl -s "${OPENAPI_URL}" -o /tmp/openapi.json

if [ ! -f /tmp/openapi.json ]; then
  echo "Error: Failed to download OpenAPI schema"
  echo "Make sure the API is running at ${API_URL}"
  exit 1
fi

echo "Generating TypeScript types..."

# Create output directory if it doesn't exist
mkdir -p "${OUTPUT_DIR}"

# Generate types
npx openapi-typescript /tmp/openapi.json -o "${OUTPUT_FILE}"

echo "Types generated successfully at ${OUTPUT_FILE}"

# Cleanup
rm /tmp/openapi.json
