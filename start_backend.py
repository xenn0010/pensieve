#!/usr/bin/env python3
"""
Startup script for Pensieve main backend
Handles all import path setup before starting the server
"""

import sys
import os
from pathlib import Path

# Setup all paths BEFORE any imports
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "intelligence-engine"))
sys.path.insert(0, str(project_root / "data-pipeline"))
sys.path.insert(0, str(project_root / "mcp-servers"))

# Now we can import
import uvicorn

# Set environment variable to help modules find the project root
os.environ['PENSIEVE_ROOT'] = str(project_root)

if __name__ == "__main__":
    print("=" * 60)
    print("STARTING PENSIEVE CIO BACKEND")
    print("=" * 60)
    print(f"Project root: {project_root}")
    print(f"Python path: {sys.path[:3]}")
    print("=" * 60)
    
    # Import and run the app
    from main import app
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )