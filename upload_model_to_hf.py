"""
upload_model_to_hf.py
---------------------
Run this script ONCE (from this machine) to upload model.safetensors
to Hugging Face Hub so others can download it via setup_model.py.

Usage:
    python upload_model_to_hf.py --token hf_YOUR_TOKEN_HERE
"""

import argparse
import sys
from pathlib import Path


HF_REPO_ID = "gaurav-nimbalkar/stealth-prompt-injection-detector"
MODEL_DIR = Path(__file__).resolve().parent / "backend" / "prompt_injection_detector"


def upload_model(token: str):
    print("=" * 60)
    print("  Shield — Uploading Model to Hugging Face Hub")
    print("=" * 60)

    try:
        from huggingface_hub import HfApi
    except ImportError:
        print("[ERROR] huggingface_hub is not installed.")
        print("        Run: pip install huggingface_hub")
        sys.exit(1)

    api = HfApi(token=token)

    # Verify token
    try:
        user = api.whoami()
        print(f"\n[OK] Logged in as: {user['name']}")
    except Exception as e:
        print(f"\n[ERROR] Authentication failed: {e}")
        print("        Make sure your token has 'Write' permissions.")
        sys.exit(1)

    # Create repo if it doesn't exist
    try:
        api.create_repo(
            repo_id=HF_REPO_ID,
            repo_type="model",
            exist_ok=True,
            private=False
        )
        print(f"[OK] Repository ready: https://huggingface.co/{HF_REPO_ID}")
    except Exception as e:
        print(f"[ERROR] Could not create repository: {e}")
        sys.exit(1)

    # Upload only model.safetensors (other files already in git)
    model_file = MODEL_DIR / "model.safetensors"
    if not model_file.exists():
        print(f"\n[ERROR] Model file not found at: {model_file}")
        sys.exit(1)

    size_mb = model_file.stat().st_size / (1024 * 1024)
    print(f"\n[INFO] Uploading model.safetensors ({size_mb:.1f} MB)...")
    print("       This may take a few minutes depending on your internet speed.")

    try:
        api.upload_file(
            path_or_fileobj=str(model_file),
            path_in_repo="model.safetensors",
            repo_id=HF_REPO_ID,
            repo_type="model",
        )
        print(f"\n[OK] Upload complete!")
        print(f"\n     Model is now publicly available at:")
        print(f"     https://huggingface.co/{HF_REPO_ID}")
        print(f"\n     Anyone can now download it by running:")
        print(f"     python setup_model.py")
    except Exception as e:
        print(f"\n[ERROR] Upload failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload model to Hugging Face Hub")
    parser.add_argument(
        "--token",
        required=True,
        help="Your Hugging Face Write token (get from https://huggingface.co/settings/tokens)"
    )
    args = parser.parse_args()
    upload_model(args.token)
