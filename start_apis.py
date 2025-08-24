#!/usr/bin/env python3
"""
Pensieve API Startup Script
Launch both backend and frontend APIs simultaneously
"""

import subprocess
import sys
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def start_apis():
    """Start both API servers"""
    project_root = Path(__file__).parent
    
    logger.info("Starting Pensieve API servers...")
    
    try:
        # Start backend API on port 8000
        logger.info("Starting backend API server on port 8000...")
        backend_process = subprocess.Popen([
            sys.executable, "api_server.py"
        ], cwd=project_root)
        
        # Wait a moment for backend to start
        time.sleep(3)
        
        # Start frontend API on port 8001
        logger.info("Starting frontend API server on port 8001...")
        frontend_process = subprocess.Popen([
            sys.executable, "frontend_api.py"
        ], cwd=project_root)
        
        logger.info("Both API servers started successfully!")
        logger.info("Backend API (autonomous agent): http://localhost:8000")
        logger.info("Frontend API (dashboard data): http://localhost:8001")
        logger.info("API Documentation: http://localhost:8000/docs and http://localhost:8001/docs")
        logger.info("Press Ctrl+C to stop both servers")
        
        # Wait for processes
        try:
            backend_process.wait()
            frontend_process.wait()
        except KeyboardInterrupt:
            logger.info("Shutting down API servers...")
            backend_process.terminate()
            frontend_process.terminate()
            backend_process.wait()
            frontend_process.wait()
            logger.info("All servers stopped")
            
    except Exception as e:
        logger.error(f"Failed to start API servers: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(start_apis())