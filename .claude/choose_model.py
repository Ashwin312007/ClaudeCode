import sys
import json
import urllib.request
from pathlib import Path
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

SETTINGS_PATH = Path(r"C:\Users\teash\.claude\settings.json")
CLAUDE_EXE = r"C:\Users\teash\.local\bin\claude.exe"

CURATED_MODELS = [
    Separator("--- NVIDIA NIM Flash & High-Performance Models ---"),
    Choice("nemotron-bolt", name="NVIDIA NIM: Nemotron 3.5 Bolt (0.5s Ultra-Fast Flash - Recommended)"),
    Choice("nemotron-lightning", name="NVIDIA NIM: Nemotron 3.5 Lightning (30B MoE Reasoning)"),
    Choice("mistral-large-4", name="NVIDIA NIM: Mistral Large 4 (1T Parameter MoE)"),
    Choice("minimax-flash", name="NVIDIA NIM: MiniMax M3.1 Flash (428B MoE)"),

    Separator("--- Anthropic Claude (via OpenRouter) ---"),
    Choice("anthropic/claude-3.7-sonnet", name="Anthropic: Claude 3.7 Sonnet"),
    Choice("anthropic/claude-3.5-sonnet", name="Anthropic: Claude 3.5 Sonnet"),
    Choice("anthropic/claude-3.5-haiku", name="Anthropic: Claude 3.5 Haiku (Fast)"),
    Choice("anthropic/claude-3-opus", name="Anthropic: Claude 3 Opus"),

    Separator("--- Google Gemini (Direct AI Studio / Gateway) ---"),
    Choice("gemini-2.5-pro", name="Google: Gemini 2.5 Pro"),
    Choice("gemini-2.5-flash", name="Google: Gemini 2.5 Flash (Ultra Fast)"),
    Choice("gemini-2.0-flash", name="Google: Gemini 2.0 Flash"),
    Choice("gemini-1.5-pro", name="Google: Gemini 1.5 Pro"),

    Separator("--- DeepSeek & Coding Specialists ---"),
    Choice("openrouter/deepseek-chat", name="DeepSeek: DeepSeek V3 (Chat/Coding)"),
    Choice("deepseek/deepseek-r1", name="DeepSeek: DeepSeek R1 (Reasoning via OpenRouter)"),
    Choice("qwen/qwen-2.5-coder-32b-instruct", name="Qwen: Qwen 2.5 Coder 32B Instruct"),

    Separator("--- Free Tier Models on OpenRouter ---"),
    Choice("nvidia/nemotron-3.5-lightning:free", name="FREE: NVIDIA Nemotron 3.5 Lightning (OpenRouter)"),
    Choice("cohere/north-mini-code:free", name="FREE: Cohere North Mini Code"),

    Separator("--- More Options ---"),
    Choice("__SEARCH_ALL__", name="Search all models from catalog (Fuzzy Search)..."),
    Choice("__CUSTOM__", name="Enter custom model ID manually..."),
]

def load_settings():
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_settings(data):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def set_model_in_config(model_id):
    settings = load_settings()
    settings["model"] = model_id
    if "env" not in settings:
        settings["env"] = {}
    settings["env"]["ANTHROPIC_MODEL"] = model_id
    settings["env"]["ANTHROPIC_DEFAULT_SONNET_MODEL"] = model_id
    settings["env"]["ANTHROPIC_DEFAULT_OPUS_MODEL"] = model_id
    settings["env"]["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = model_id
    save_settings(settings)

def fetch_all_models():
    print("Fetching live model catalog from OpenRouter...")
    try:
        req = urllib.request.Request("https://openrouter.ai/api/v1/models", headers={"User-Agent": "ClaudeCode/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        models = data.get("data", [])
        return [Choice(m["id"], name=f"{m.get('name', m['id'])} ({m['id']})") for m in sorted(models, key=lambda x: x.get("name", ""))]
    except Exception as e:
        print(f"Warning: Could not fetch live models ({e}). Using cached models.")
        return []

def main():
    settings = load_settings()
    current_model = settings.get("model", "claude-3-5-sonnet")

    # If model was passed as CLI argument, use it directly
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        selected = sys.argv[1]
        set_model_in_config(selected)
        print(f"\n[OK] Model updated to: {selected}\n")
        return selected

    print("=" * 60)
    print("  Claude Code Model Selector (All Providers & Models)")
    print(f"  Current Model: {current_model}")
    print("=" * 60)

    selected = inquirer.fuzzy(
        message="Select model (type to search, Enter to choose):",
        choices=CURATED_MODELS,
        default=current_model,
        border=True,
    ).execute()

    if selected == "__CUSTOM__":
        selected = inquirer.text(
            message="Enter model ID (e.g. minimax-flash):"
        ).execute().strip()
    elif selected == "__SEARCH_ALL__":
        all_models = fetch_all_models()
        if not all_models:
            print("Falling back to default.")
            selected = current_model
        else:
            selected = inquirer.fuzzy(
                message="Search all models:",
                choices=all_models,
                border=True
            ).execute()

    if selected:
        set_model_in_config(selected)
        print(f"\n[OK] Active model set to: {selected}\n")
        return selected

    return current_model

if __name__ == "__main__":
    main()
