# ⚡ Claude Code Free Models Harness

> **Run Anthropic's official Claude Code CLI completely free using NVIDIA NIM, OpenRouter, DeepSeek, or local LLMs — with 100% executable tool calls and no Anthropic API subscription required.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-purple.svg)](https://github.com/anthropics/claude-code)

---

## 🎯 What This Solves

### The "Just Making Conversations" Problem — Explained & Solved

When running open-weight or third-party models in Claude Code via generic proxies (like basic LiteLLM), users frequently experience this critical issue:
> *"I asked Claude Code to perform a task (like creating or editing a file), but it just chats about what it would do instead of actually doing it!"*

### Why this happens:
1. **Claude Code expects native Anthropic SSE tool events** (`content_block_start`, `tool_use`, `input_json_delta`, `content_block_stop`).
2. Open-weight models (Nemotron, Llama, Qwen, GLM, etc.) often receive 30+ Claude tool schemas with an extensive 40,000+ token internal system prompt. Under this load, many models output the tool invocation as plain text (e.g. `Write{file_path: "test.txt", content: "..."}` or `● <function=Write>...`) rather than structured OpenAI function call objects.
3. Generic proxies stream this text directly to Claude Code. Claude Code interprets it as normal conversational text, prints it out, and **never executes the tool or touches the disk**!

### How this Harness fixes it:
- 🛡️ **Full Anthropic SSE Streaming Adapter**: Converts streaming OpenAI `/chat/completions` directly into Anthropic's native message stream format.
- ⚙️ **Heuristic Tool Parser**: Built-in stateful parser that automatically intercepts text-based tool calls (`Write{...}`, `Bash{...}`, `Edit{...}`, `Glob{...}`, `● <function=...>`, etc.), extracts parameters (including unquoted pseudo-JSON keys), strips the command syntax from the conversational reply, and emits structured Anthropic `tool_use` events.
- ⚡ **Physical Tool Execution**: Claude Code receives genuine `tool_use` blocks and immediately executes the commands (`Write`, `Edit`, `Bash`, `View`, etc.) on your machine.
- 🚀 **Request Optimization**: Intercepts background non-essential Claude Code probes (title generation, prefix detection) locally, saving quota and latency.

---

## 🚀 Quick Start (Step-by-Step Setup)

### 1. Prerequisites
- **Python 3.11+** installed and available in PATH.
- **Node.js 18+** (required for official Claude Code CLI).
- **Claude Code CLI** installed:
  ```powershell
  npm install -g @anthropic-ai/claude-code
  ```
- **NVIDIA NIM API Key** (Free 1,000 credits, no credit card needed):
  - Grab your key from [build.nvidia.com/settings/api-keys](https://build.nvidia.com/settings/api-keys)

---

### 2. Installation from Git

Clone the repository to any folder (e.g., `E:\ClaudeCode` or `C:\ClaudeCode`):

```bash
git clone https://github.com/Ashwin312007/ClaudeCode.git
cd ClaudeCode
```

Run the automated installer:

#### On Windows (Command Prompt or PowerShell):
```cmd
install.bat
```
*Or using PowerShell:*
```powershell
.\install.ps1
```

The installer will:
1. Verify Python and automatically install `uv` package manager if missing.
2. Deploy the proxy engine to `%USERPROFILE%\.claude\proxy`.
3. Install all isolated proxy dependencies via `uv sync`.
4. Deploy launcher commands (`start-claude-gateway`, `claude-model`, `cm`, `set-nvidia-key`) to `%USERPROFILE%\.local\bin`.
5. Configure `~/.claude/settings.json` to route Claude Code to `http://127.0.0.1:8082`.
6. Add `%USERPROFILE%\.local\bin` to your User PATH.

> [!NOTE]
> Reopen your terminal after running `install.bat` so the PATH update takes effect.

---

### 3. Add Your API Key

Run the key configuration command:
```cmd
set-nvidia-key
```
Paste your `nvapi-...` key. It will validate against NVIDIA's API and update your configuration.

---

### 4. Start the Gateway & Launch Claude Code

In terminal 1, start the gateway:
```cmd
start-claude-gateway
```
*You will see: `Uvicorn running on http://127.0.0.1:8082`.*

In terminal 2, run Claude Code:
```cmd
claude
```
Now ask Claude Code to create files, run git commands, edit code, or build projects — all tool operations will execute directly on disk!

---

## 🎮 Switching & Adding Models

You can switch models interactively at any time:

```cmd
claude-model
```
*(or simply use the shortcut `cm`)*

### Interactive Selection Menu:
```text
? Select Active Model for Claude Code:
 > NVIDIA NIM: Nemotron 3.5 Lightning (30B MoE Flash - Fast & Executable Tools - Recommended)
   NVIDIA NIM: Mistral Large 4 (1 Trillion Param MoE - Frontier Architecture)
   NVIDIA NIM: Nemotron 3 Ultra (550B Frontier Model)
   NVIDIA NIM: Nemotron 3.5 Bolt (4B Ultra-Fast Flash)
   OpenRouter: Kimi K2.5 (Moonshot AI - Free on OpenRouter)
   OpenRouter: GLM 4.5 Air (Zhipu AI - Free on OpenRouter)
   OpenRouter: StepFun 3.5 Flash (Free on OpenRouter)
   OpenRouter: DeepSeek R1 Reasoning (Free on OpenRouter)
   DeepSeek: DeepSeek V3 (Chat & Coding Specialist)
   Local: LM Studio / llama.cpp
   [Custom Model ID...]
```

---

## 📖 How to Add ANY Free Model

All model routing is managed in `%USERPROFILE%\.claude\proxy\.env` (or `proxy/.env` in the repo).

You can route Claude Code's model tiers (`Opus`, `Sonnet`, `Haiku`) independently or set a single fallback model `MODEL`:

```dotenv
# ==============================================================================
# Model Routing Configuration
# Format: <provider_id>/<model_name>
# ==============================================================================

# Routes heavy architecting/reasoning (Opus requests)
MODEL_OPUS="nvidia_nim/mistralai/mistral-large-4-1t-a52b"

# Routes everyday coding and tool execution (Sonnet requests)
MODEL_SONNET="nvidia_nim/nvidia/nemotron-3.5-lightning-30b-a3b"

# Routes fast queries and small edits (Haiku requests)
MODEL_HAIKU="nvidia_nim/nvidia/nemotron-3.5-lightning-30b-a3b"

# Global fallback for any other model name
MODEL="nvidia_nim/nvidia/nemotron-3.5-lightning-30b-a3b"
```

---

### 1. Adding Free NVIDIA NIM Models
*(Requires `NVIDIA_NIM_API_KEY="nvapi-..."` in `.env`)*

| Model | Provider / Model ID | Notes |
| :--- | :--- | :--- |
| **Nemotron 3.5 Lightning** *(Default)* | `nvidia_nim/nvidia/nemotron-3.5-lightning-30b-a3b` | **Best All-Round Flash**: 30B MoE, ultra-fast 0.5s latency, native tool execution. |
| **Mistral Large 4** | `nvidia_nim/mistralai/mistral-large-4-1t-a52b` | **Frontier Powerhouse**: 1 Trillion parameter MoE (52B active), top reasoning & coding. |
| **Nemotron 3 Ultra** | `nvidia_nim/nvidia/nemotron-3-ultra-550b-a55b` | **550B Parameter**: Deep architectural planning. |
| **Nemotron 3.5 Bolt** | `nvidia_nim/nvidia/nemotron-3.5-bolt-e4b` | **Ultra-Fast 4B**: Lightweight flash model for simple code lookups. |
| **Poolside Laguna XS 2.1** | `nvidia_nim/poolside/laguna-xs-2.1` | **Fast Coding Specialist**: Optimized for code generation. |

To add any of these, set in `.env`:
```dotenv
MODEL_SONNET="nvidia_nim/nvidia/nemotron-3.5-lightning-30b-a3b"
```

---

### 2. Adding Free Models on OpenRouter (Kimi, GLM, StepFun, DeepSeek)
*(Requires free `OPENROUTER_API_KEY="sk-or-..."` in `.env`)*

OpenRouter hosts hundreds of free models with `:free` suffixes:

| Model | Provider / Model ID | Description |
| :--- | :--- | :--- |
| **Moonshot Kimi K2.5** | `open_router/moonshotai/kimi-k2.5:free` | Moonshot AI's flagship multimodal & agent model. |
| **Zhipu GLM 4.5 Air** | `open_router/z-ai/glm-4.5-air:free` | Ultra-fast Chinese/English bilingual coding model. |
| **StepFun 3.5 Flash** | `open_router/stepfun/step-3.5-flash:free` | Low-latency flash reasoning model. |
| **DeepSeek R1 Free** | `open_router/deepseek/deepseek-r1-0528:free` | Open-source reasoning model with thinking chains. |
| **OpenAI GPT-OSS 120B** | `open_router/openai/gpt-oss-120b:free` | Open-weight 120B model on OpenRouter. |

To use Kimi or GLM, update `.env`:
```dotenv
OPENROUTER_API_KEY="sk-or-v1-your-key-here"
MODEL_SONNET="open_router/moonshotai/kimi-k2.5:free"
MODEL_HAIKU="open_router/z-ai/glm-4.5-air:free"
```

---

### 3. Adding Direct DeepSeek API
*(Requires `DEEPSEEK_API_KEY="sk-..."` in `.env`)*

```dotenv
DEEPSEEK_API_KEY="sk-your-deepseek-key"
MODEL_OPUS="deepseek/deepseek-reasoner"
MODEL_SONNET="deepseek/deepseek-chat"
```

---

### 4. Running 100% Locally (LM Studio / llama.cpp)
*(Zero cost, no internet or API key required)*

Run LM Studio local server on `http://localhost:1234/v1`:
```dotenv
MODEL="lmstudio/unsloth/Qwen3.5-35B-A3B-GGUF"
```
Or with `llama-server` on `http://localhost:8080/v1`:
```dotenv
LLAMACPP_BASE_URL="http://localhost:8080/v1"
MODEL="llamacpp/local-model"
```

---

## 📁 Repository Structure & Included Files

```text
ClaudeCode/
├── .claude/
│   ├── settings.json          # Claude Code runtime environment & endpoints
│   ├── choose_model.py        # Dynamic interactive model selection script
│   └── set_nvidia_key.py      # Automated NVIDIA NIM key updater
├── bin/
│   ├── start-claude-gateway.cmd # Gateway launcher on port 8082
│   ├── claude-model.cmd         # Model switcher command
│   ├── cm.cmd                   # Shortcut for claude-model
│   └── set-nvidia-key.cmd       # API key updater command
├── proxy/                       # The core tool-enabled gateway engine
│   ├── api/                     # FastAPI Anthropic /v1/messages routes
│   ├── core/
│   │   └── anthropic/
│   │       ├── tools.py         # Advanced Heuristic Tool Parser (Solves chat-only issue)
│   │       ├── conversion.py    # Anthropic <-> OpenAI format translation
│   │       └── sse.py           # Anthropic Server-Sent Events stream generator
│   ├── providers/               # Upstream adapters (NVIDIA NIM, OpenRouter, DeepSeek, Local)
│   ├── server.py                # Gateway ASGI entrypoint
│   ├── pyproject.toml           # Package configuration & dependencies
│   ├── uv.lock                  # Deterministic dependency lockfile
│   └── .env.example             # Clean environment template (no raw secrets)
├── install.bat                  # One-click Windows CMD installer
├── install.ps1                  # One-click Windows PowerShell installer
├── .gitignore                   # Prevents secret & cache leakage
└── README.md                    # Complete documentation
```

---

## 🛠️ Verification & Testing

To test that tool calling is physically working on your machine:

```powershell
claude -p "Create a file named verify_agent.txt containing 'agent works'. Do not just talk, execute the tool." --dangerously-skip-permissions
```

If configured properly, Claude Code will:
1. Stream through the gateway on port 8082.
2. Translate the model output into an Anthropic `Write` tool block.
3. Physically write `verify_agent.txt` on your disk.
4. Report: `Done - I created verify_agent.txt with the content agent works.`

---

## 🔒 Security & Privacy Notice

- API keys (`NVIDIA_NIM_API_KEY`, `OPENROUTER_API_KEY`, `DEEPSEEK_API_KEY`) are stored **locally only** in `%USERPROFILE%\.claude\proxy\.env`.
- The repository `.gitignore` strictly excludes `.env` and `*.env` files to prevent accidental leakage to public GitHub repositories.
- Never commit active keys to git remotes.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
