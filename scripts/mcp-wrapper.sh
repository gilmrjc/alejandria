#!/bin/bash
# Wrapper script for MCP server to run on host with Docker services
# Note: The MCP server now uses HTTP transport, so this script is only
# used for local development when running the server directly

set -e

# Change to the project directory
cd "$(dirname "$0")/.."

# Set environment variables to connect to Docker services
export APP_ENV="development"
export DEBUG="true"
export LOG_LEVEL="INFO"
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/alejandria"
export REDIS_URL="redis://localhost:6379/0"
export QDRANT_URL="http://localhost:6333"
export QDRANT_GRPC_URL="http://localhost:6334"
export OLLAMA_URL="http://localhost:11434"
export SECRET_KEY="dev-secret-key-change-in-production"
export ALGORITHM="HS256"
export ACCESS_TOKEN_EXPIRE_MINUTES="30"
export MCP_API_KEY_REQUIRED="true"

# Execute the MCP server directly on the host using uv
# The server will start in HTTP mode on http://localhost:8000
cd backend
uv run python -m mcp_server.server
