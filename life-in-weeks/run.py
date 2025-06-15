import sys
from pathlib import Path
from uvicorn import run
import os

if __name__ == "__main__":
    # Add project root to Python path
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    
    # Set environment variable to prefer watchfiles
    os.environ["UVICORN_RELOAD"] = "watchfiles"
    
    # Run the application
    run(
        "backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(project_root / "backend")]
    )