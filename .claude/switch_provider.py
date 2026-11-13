import json
import os
import sys
from pathlib import Path

SETTINGS_PATH = Path(r"C:\Users\teash\.claude\settings.json")

def load_settings():
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_settings(data):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def set_openrouter(model="anthropic/claude-3.7-sonnet"):
    settings = load_settings()
    env = settings.get("env", {})
    openrouter_key = env.get("OPENROUTER_API_KEY", os.environ.get("OPENROUTER_API_KEY", ""))

    env["ANTHROPIC_BASE_URL"] = "https://openrouter.ai/api"
    env["ANTHROPIC_AUTH_TOKEN"] = openrouter_key
    env["ANTHROPIC_API_KEY"] = ""
    env["CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY"] = "1"
    env["ANTHROPIC_MODEL"] = model
    settings["env"] = env
    settings["model"] = model
    save_settings(settings)
    print(f"[OK] Claude Code configured for Direct OpenRouter. Model: {model}")

def set_gateway(model="claude-3-5-sonnet"):
    settings = load_settings()
    env = settings.get("env", {})
    env["ANTHROPIC_BASE_URL"] = "http://localhost:4000"
    env["ANTHROPIC_AUTH_TOKEN"] = "sk-claude-local-proxy-key"
    env["ANTHROPIC_API_KEY"] = ""
    env["CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY"] = "1"
    env["ANTHROPIC_MODEL"] = model
    env["ANTHROPIC_DEFAULT_SONNET_MODEL"] = model
    env["ANTHROPIC_DEFAULT_OPUS_MODEL"] = model
    env["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = model
    settings["env"] = env
    settings["model"] = model
    save_settings(settings)
    print(f"[OK] Claude Code configured for Local Gateway (http://localhost:4000). Model: {model}")
    print("     Make sure the gateway is running by executing: start-claude-gateway")

def set_model(model_name):
    settings = load_settings()
    settings["model"] = model_name
    if "env" in settings:
        settings["env"]["ANTHROPIC_MODEL"] = model_name
        settings["env"]["ANTHROPIC_DEFAULT_SONNET_MODEL"] = model_name
        settings["env"]["ANTHROPIC_DEFAULT_OPUS_MODEL"] = model_name
        settings["env"]["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = model_name
    save_settings(settings)
    print(f"[OK] Model set to: {model_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python switch_provider.py openrouter [optional_model_name]")
        print("  python switch_provider.py gateway [optional_model_name]")
        print("  python switch_provider.py nvidia [optional_model_name]")
        print("  python switch_provider.py model <model_name>")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "openrouter":
        m = sys.argv[2] if len(sys.argv) > 2 else "anthropic/claude-3.7-sonnet"
        set_openrouter(m)
    elif cmd in ("gateway", "nvidia"):
        m = sys.argv[2] if len(sys.argv) > 2 else "claude-3-5-sonnet"
        set_gateway(m)
    elif cmd == "model":
        if len(sys.argv) < 3:
            print("Please provide a model name, e.g.: python switch_provider.py model claude-3-5-sonnet")
            sys.exit(1)
        set_model(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
