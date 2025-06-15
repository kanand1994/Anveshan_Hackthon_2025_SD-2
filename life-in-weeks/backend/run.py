import sys
from pathlib import Path

# Calculate absolute path to project root
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Now import and run your app
from backend.app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)