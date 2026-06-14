#!/usr/bin/env python3
"""
Download YOLO models for the person counting system.
Saves to models/ directory.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from config import Config

def download_model():
    """Download YOLO11n model using ultralytics"""
    try:
        from ultralytics import YOLO
        
        model_dir = Path(Config.MODEL_PATH).parent
        model_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📥 Downloading YOLO model to: {Config.MODEL_PATH}")
        print("   (This may take a few minutes for the first time...)")
        
        # Download model
        model = YOLO("yolo12n.pt")
        
        print(f"✅ Model downloaded successfully!")
        print(f"   Location: {Config.MODEL_PATH}")
        
        return True
    
    except ImportError:
        print("❌ Error: ultralytics package not installed yet.")
        print("   Please wait for: pip install opencv-python numpy ultralytics ...")
        return False
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False


if __name__ == "__main__":
    success = download_model()
    sys.exit(0 if success else 1)
