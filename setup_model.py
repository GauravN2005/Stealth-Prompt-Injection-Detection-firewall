"""
setup_model.py
--------------
Run this script ONCE after cloning the repository to download the
DistilBERT model weights from Hugging Face Hub.

Usage:
    python setup_model.py
"""

import os
import sys
from pathlib import Path


HF_REPO_ID = "gaurav-nimbalkar/stealth-prompt-injection-detector"
MODEL_DIR = Path(__file__).resolve().parent / "backend" / "prompt_injection_detector"
MODEL_FILE = MODEL_DIR / "model.safetensors"


def download_model():
    print("=" * 60)
    print("  Shield — Stealth Prompt Injection Detector")
    print("  Model Setup Script")
    print("=" * 60)

    if MODEL_FILE.exists():
        size_mb = MODEL_FILE.stat().st_size / (1024 * 1024)
        print(f"\n[OK] Model already exists at: {MODEL_FILE}")
        print(f"     Size: {size_mb:.1f} MB")
        print("\nSetup complete. You can start the backend now.")
        return

    print(f"\n[INFO] Downloading model from Hugging Face Hub...")
    print(f"       Repo : {HF_REPO_ID}")
    print(f"       File : model.safetensors (~267 MB)")
    print(f"       To   : {MODEL_FILE}")
    print()

    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        print("[ERROR] huggingface_hub is not installed.")
        print("        Run: pip install huggingface_hub")
        sys.exit(1)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    try:
        downloaded_path = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename="model.safetensors",
            local_dir=str(MODEL_DIR),
            local_dir_use_symlinks=False,
        )
        size_mb = Path(downloaded_path).stat().st_size / (1024 * 1024)
        print(f"\n[OK] Download complete!")
        print(f"     Saved to : {downloaded_path}")
        print(f"     Size     : {size_mb:.1f} MB")
        print("\nSetup complete. You can now start the backend:")
        print("  cd backend")
        print("  python -m uvicorn app:app --host 127.0.0.1 --port 8000")

    except Exception as e:
        print(f"\n[ERROR] Download failed: {e}")
        print()
        print("Manual download steps:")
        print(f"  1. Visit: https://huggingface.co/{HF_REPO_ID}/resolve/main/model.safetensors")
        print(f"  2. Save the file to: {MODEL_FILE}")
        sys.exit(1)


if __name__ == "__main__":
    download_model()
