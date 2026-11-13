import sys
import re
import json
import urllib.request
from pathlib import Path

HOME_DIR = Path.home()
CLAUDE_DIR = HOME_DIR / ".claude"
SETTINGS_PATH = CLAUDE_DIR / "settings.json"
ENV_PATHS = [
    Path(__file__).resolve().parent.parent / "proxy" / ".env",
    CLAUDE_DIR / "proxy" / ".env",
    CLAUDE_DIR / ".env"
]

def validate_key(key: str) -> bool:
    print("Validating NVIDIA API key against NVIDIA NIM API...")
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
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "env" not in data:
                data["env"] = {}
            data["env"]["NVIDIA_API_KEY"] = key
            with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"[OK] Updated {SETTINGS_PATH}")
        except Exception as e:
            print(f"[WARN] Failed to update settings.json: {e}")

    # 2. Update .env files
    for env_p in ENV_PATHS:
        if env_p.exists():
            content = env_p.read_text(encoding="utf-8")
            if "NVIDIA_NIM_API_KEY" in content:
                content = re.sub(r'NVIDIA_NIM_API_KEY=.*', f'NVIDIA_NIM_API_KEY="{key}"', content)
            elif "NVIDIA_API_KEY" in content:
                content = re.sub(r'NVIDIA_API_KEY=.*', f'NVIDIA_API_KEY="{key}"', content)
            else:
                content += f'\nNVIDIA_NIM_API_KEY="{key}"\n'
            env_p.write_text(content, encoding="utf-8")
            print(f"[OK] Updated {env_p}")

def main():
    if len(sys.argv) > 1:
        key = sys.argv[1].strip()
    else:
        key = input("Enter your NVIDIA NIM API key (nvapi-...): ").strip()

    if not key.startswith("nvapi-"):
        print("[ERROR] NVIDIA NIM API keys must start with 'nvapi-'.")
        sys.exit(1)

    if not validate_key(key):
        sys.exit(1)

    update_files(key)
    print("\n[SUCCESS] NVIDIA API key updated across all configuration files!")

if __name__ == "__main__":
    main()
