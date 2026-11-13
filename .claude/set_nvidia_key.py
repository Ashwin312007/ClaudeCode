import sys
import re
import json
import urllib.request
from pathlib import Path

SETTINGS_PATH = Path(r"C:\Users\teash\.claude\settings.json")
CONFIG_PATH = Path(r"C:\Users\teash\.claude\litellm-config.yaml")
ENV_PATH = Path(r"C:\Users\teash\.claude\.env")

def validate_key(key: str) -> bool:
    print(f"Validating NVIDIA API key against NVIDIA NIM API...")
    try:
        req = urllib.request.Request(
            "https://integrate.api.nvidia.com/v1/models",
            headers={"Authorization": f"Bearer {key}"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                print("[OK] Key authenticated successfully (HTTP 200).")
                return True
    except Exception as e:
        print(f"[ERROR] Key validation failed: {e}")
        return False
    return False

def update_files(key: str):
    # 1. Update settings.json
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "env" in data:
            data["env"]["NVIDIA_API_KEY"] = key
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[OK] Updated {SETTINGS_PATH.name}")

    # 2. Update .env
    if ENV_PATH.exists():
        content = ENV_PATH.read_text(encoding="utf-8")
        content = re.sub(r'NVIDIA_API_KEY=.*', f'NVIDIA_API_KEY={key}', content)
        ENV_PATH.write_text(content, encoding="utf-8")
        print(f"[OK] Updated {ENV_PATH.name}")

    # 3. Update litellm-config.yaml
    if CONFIG_PATH.exists():
        content = CONFIG_PATH.read_text(encoding="utf-8")
        content = re.sub(r'api_key:\s*"nvapi-[^"]*"', f'api_key: "{key}"', content)
        CONFIG_PATH.write_text(content, encoding="utf-8")
        print(f"[OK] Updated {CONFIG_PATH.name}")

    print("\n[SUCCESS] NVIDIA API key updated across all Claude Code harness configurations.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: set-nvidia-key <your-nvapi-key>")
        sys.exit(1)

    new_key = sys.argv[1].strip()
    if not new_key.startswith("nvapi-"):
        print("[WARNING] Key does not start with 'nvapi-'. Proceeding anyway...")

    if validate_key(new_key):
        update_files(new_key)
    else:
        sys.exit(1)
