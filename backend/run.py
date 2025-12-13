#!/usr/bin/env python
"""
Run script for the Document-Based QA System backend
"""
import os
import sys
import subprocess

def main():
    """Start the FastAPI server"""
    print("=" * 60)
    print("Document-Based Question Answering System")
    print("=" * 60)
    print("\nStarting FastAPI server...")
    print("API will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 60)
    
    # Change to backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    # Run the FastAPI server
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
