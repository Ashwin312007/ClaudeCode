import os
import re
import sys
import json
from pathlib import Path

# Resolve home and config paths dynamically
HOME_DIR = Path.home()
CLAUDE_DIR = HOME_DIR / ".claude"
SETTINGS_PATH = CLAUDE_DIR / "settings.json"

# Search for proxy .env in multiple locations
POTENTIAL_ENV_PATHS = [
    Path(__file__).resolve().parent.parent / "proxy" / ".env",
    CLAUDE_DIR / "proxy" / ".env",
    Path(os.environ.get("TEMP", "")) / "free-claude-code" / ".env",
]

def get_env_path():
    for p in POTENTIAL_ENV_PATHS:
        if p.is_file():
            return p
    # Default to ~/.claude/proxy/.env
    default_p = CLAUDE_DIR / "proxy" / ".env"
    default_p.parent.mkdir(parents=True, exist_ok=True)
    return default_p

def update_env_file(model_str):
    env_path = get_env_path()
    lines = []
    if env_path.exists():
        lines = env_path.read_text(encoding="utf-8").splitlines()
    
    new_lines = []
    keys_updated = set()
    
    for line in lines:
        stripped = line.strip()
        matched = False
        for k in ["MODEL", "MODEL_SONNET", "MODEL_HAIKU"]:
            if stripped.startswith(f"{k}=") or stripped.startswith(f"{k} ="):
                new_lines.append(f'{k}="{model_str}"')
                keys_updated.add(k)
                matched = True
                break
        if not matched:
            new_lines.append(line)
            
    for k in ["MODEL", "MODEL_SONNET", "MODEL_HAIKU"]:
        if k not in keys_updated:
            new_lines.append(f'{k}="{model_str}"')
            
    env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"[OK] Updated proxy .env at: {env_path}")

def update_settings_json():
    if not SETTINGS_PATH.exists():
        SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        settings = {}
    else:
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                settings = json.load(f)
        except Exception:
            settings = {}

    env = settings.get("env", {})
    env["ANTHROPIC_BASE_URL"] = "http://127.0.0.1:8082"
    env["ANTHROPIC_AUTH_TOKEN"] = "dummy"
    env["ANTHROPIC_API_KEY"] = "dummy"
    env["CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY"] = "1"
    env["ANTHROPIC_MODEL"] = "claude-3-5-sonnet"
    env["ANTHROPIC_DEFAULT_SONNET_MODEL"] = "claude-3-5-sonnet"
    env["ANTHROPIC_DEFAULT_OPUS_MODEL"] = "claude-3-opus"
    env["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = "claude-3-5-haiku"
    
    settings["env"] = env
    settings["model"] = "claude-3-5-sonnet"
    
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
    print(f"[OK] Settings verified at: {SETTINGS_PATH}")

MODELS_MENU = [
    # Category, ID, Display Name
    ("--- NVIDIA NIM Models (Free with NVIDIA API Key) ---", None, None),
    (
        "NVIDIA NIM",
        "nvidia_nim/nvidia/nemotron-3.5-lightning-30b-a3b",
        "NVIDIA Nemotron 3.5 Lightning (30B MoE Flash - Fast & Executable Tools - Recommended)"
    ),
    (
        "NVIDIA NIM",
        "nvidia_nim/mistralai/mistral-large-4-1t-a52b",
        "Mistral Large 4 (1 Trillion Param MoE - Frontier Architecture)"
    ),
    (
        "NVIDIA NIM",
        "nvidia_nim/nvidia/nemotron-3-ultra-550b-a55b",
        "NVIDIA Nemotron 3 Ultra (550B Frontier Model)"
    ),
    (
        "NVIDIA NIM",
        "nvidia_nim/nvidia/nemotron-3.5-bolt-e4b",
        "NVIDIA Nemotron 3.5 Bolt (4B Ultra-Fast Flash)"
    ),
    (
        "NVIDIA NIM",
        "nvidia_nim/poolside/laguna-xs-2.1",
        "Poolside Laguna XS 2.1 (Fast Coding)"
    ),

    ("--- OpenRouter Free Models (Requires OPENROUTER_API_KEY in .env) ---", None, None),
    (
        "OpenRouter",
        "open_router/moonshotai/kimi-k2.5:free",
        "Kimi K2.5 (Moonshot AI - Free on OpenRouter)"
    ),
    (
        "OpenRouter",
        "open_router/z-ai/glm-4.5-air:free",
        "GLM 4.5 Air (Zhipu AI - Free on OpenRouter)"
    ),
    (
        "OpenRouter",
        "open_router/stepfun/step-3.5-flash:free",
        "StepFun 3.5 Flash (Free on OpenRouter)"
    ),
    (
        "OpenRouter",
        "open_router/deepseek/deepseek-r1-0528:free",
        "DeepSeek R1 Reasoning (Free on OpenRouter)"
    ),
    (
        "OpenRouter",
        "open_router/openai/gpt-oss-120b:free",
        "OpenAI GPT-OSS 120B (Free on OpenRouter)"
    ),

    ("--- DeepSeek Direct API (Requires DEEPSEEK_API_KEY in .env) ---", None, None),
    (
        "DeepSeek",
        "deepseek/deepseek-chat",
        "DeepSeek V3 (Chat & Coding Specialist)"
    ),
    (
        "DeepSeek",
        "deepseek/deepseek-reasoner",
        "DeepSeek R1 (Frontier Reasoning)"
    ),

    ("--- Local Models (No API Key Required) ---", None, None),
    (
        "Local",
        "lmstudio/unsloth/Qwen3.5-35B-A3B-GGUF",
        "LM Studio: Qwen 3.5 35B GGUF (http://localhost:1234)"
    ),
    (
        "Local",
        "llamacpp/local-model",
        "llama.cpp: Local Server (http://localhost:8080)"
    ),

    ("--- Custom ---", None, None),
    (
        "Custom",
        "__CUSTOM__",
        "Enter custom model ID manually (e.g. nvidia_nim/..., open_router/...)"
    )
]

def main():
    try:
        from InquirerPy import inquirer
        from InquirerPy.base.control import Choice
        from InquirerPy.separator import Separator

        choices = []
        for cat, mid, name in MODELS_MENU:
            if mid is None:
                choices.append(Separator(cat))
            else:
                choices.append(Choice(mid, name=name))

        selected = inquirer.select(
            message="Select Active Model for Claude Code:",
            choices=choices,
            default="nvidia_nim/nvidia/nemotron-3.5-lightning-30b-a3b"
        ).execute()

    except ImportError:
        # Fallback text menu if InquirerPy is not installed
        print("\n=== Select Model for Claude Code ===")
        selectable = []
        for cat, mid, name in MODELS_MENU:
            if mid is None:
                print(f"\n{cat}")
            else:
                selectable.append((mid, name))
                print(f"  [{len(selectable)}] {name}")
        print()
        val = input(f"Enter choice [1-{len(selectable)}]: ").strip()
        try:
            idx = int(val) - 1
            selected = selectable[idx][0]
        except Exception:
            selected = "nvidia_nim/nvidia/nemotron-3.5-lightning-30b-a3b"

    if selected == "__CUSTOM__":
        selected = input("\nEnter custom model (e.g., nvidia_nim/nvidia/nemotron-3.5-lightning-30b-a3b): ").strip()
        if not selected:
            print("No model entered. Exiting.")
            return

    update_env_file(selected)
    update_settings_json()
    print(f"\n[SUCCESS] Active Claude Code model set to: {selected}")
    print("If the gateway is running, it will automatically route all Claude Code requests to this model!")

if __name__ == "__main__":
    main()
