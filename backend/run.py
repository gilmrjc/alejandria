#!/usr/bin/env python3
"""
Alejandria - Unified Entry Point

This script is the unified entry point to run:
- FastAPI API
- Celery Workers
- MCP Server

Usage:
    python run.py api          # Start FastAPI API
    python run.py worker       # Start Celery worker
    python run.py mcp          # Start MCP server
    python run.py scheduler    # Start Celery beat scheduler
"""

import argparse
import sys


def run_api():
    """Start the FastAPI API."""
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


def run_worker():
    """Start Celery worker."""
    from jobs.celery_app import celery_app

    celery_app.worker_main(argv=["worker", "--loglevel=info"])


def run_scheduler():
    """Start Celery beat scheduler."""
    from jobs.celery_app import celery_app

    celery_app.start(argv=["beat", "--loglevel=info"])


def run_mcp():
    """Start MCP server."""
    from mcp_server.server import main

    main()


def main():
    parser = argparse.ArgumentParser(
        description="Alejandria - Unified Entry Point",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run.py api          # Start API server
    python run.py worker       # Start Celery worker
    python run.py mcp          # Start MCP server
    python run.py scheduler    # Start Celery beat
        """,
    )

    parser.add_argument(
        "command",
        choices=["api", "worker", "mcp", "scheduler"],
        help="Component to run",
    )

    args = parser.parse_args()

    commands = {
        "api": run_api,
        "worker": run_worker,
        "mcp": run_mcp,
        "scheduler": run_scheduler,
    }

    try:
        commands[args.command]()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
