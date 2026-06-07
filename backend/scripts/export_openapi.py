#!/usr/bin/env python3
"""
Export OpenAPI schema from FastAPI application.
This script generates openapi.json for contract testing.

NOTE: FastAPI already exposes /openapi.json endpoint automatically.
The simplest approach is to use that endpoint directly:

  # With docker-compose (API running)
  docker compose exec api curl -s http://localhost:8000/openapi.json > openapi.json

  # Or from host
  curl -s http://localhost:8000/openapi.json > openapi.json

This script is optional for CI/CD pipelines that need the file as artifact
without starting the full server.

Usage (with docker-compose, no server needed):
  docker compose run --rm api uv run python scripts/export_openapi.py
"""

import json
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.main import app

def main():
    """Export OpenAPI schema to openapi.json."""
    output_path = Path(__file__).parent.parent / "openapi.json"
    
    schema = app.openapi()
    
    with open(output_path, "w") as f:
        json.dump(schema, f, indent=2)
    
    print(f"OpenAPI schema exported to {output_path}")

if __name__ == "__main__":
    main()
