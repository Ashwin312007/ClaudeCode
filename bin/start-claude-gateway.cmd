@echo off
echo Starting Claude Code Multi-Provider Gateway on port 4000...
echo Providers enabled:
echo   - NVIDIA NIM Bolt:  nemotron-bolt (0.5s ultra-fast Flash - Default)
echo   - NVIDIA NIM MoE:   nemotron-lightning (30B reasoning), mistral-large-4
echo   - Google Gemini:    gemini-2.5-pro, gemini-2.5-flash
echo   - OpenRouter:       openrouter/claude-3-7-sonnet
echo.
python -m litellm.proxy.proxy_cli --config "C:\Users\teash\.claude\litellm-config.yaml" --port 4000 --drop_params --request_timeout 180
