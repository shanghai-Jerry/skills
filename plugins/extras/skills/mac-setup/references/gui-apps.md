# GUI Applications Reference

Recommended desktop applications for macOS, organized by category.

## Code Editors

| Tool | Install | Description |
|------|---------|-------------|
| Visual Studio Code | `brew install --cask visual-studio-code` | Most popular code editor, rich extension ecosystem |
| Cursor | `brew install --cask cursor` | AI-first code editor built on VS Code |

## Productivity

| Tool | Install | Description |
|------|---------|-------------|
| Raycast | `brew install --cask raycast` | Spotlight replacement with extensions, clipboard history, snippets |
| Rectangle | `brew install --cask rectangle` | Window manager — snap/resize windows with keyboard shortcuts |
| Bitwarden | `brew install --cask bitwarden` | Open-source password manager |
| Obsidian | `brew install --cask obsidian` | Local-first knowledge base and note-taking app |
| CleanShot X | `brew install --cask cleanshot-x` | Screen capture, recording, annotation, and scrolling capture |

## Networking & Proxy

| Tool | Install | Description |
|------|---------|-------------|
| Tailscale | `brew install --cask tailscale` | Zero-config VPN mesh network — securely access devices and networks |
| ClashX | Download from [GitHub Releases](https://github.com/yichengchen/clashX/releases) | Rule-based proxy client for macOS, commonly used for network access in China |
| SwitchHosts | `brew install --cask switchhosts` | Host file switcher — toggle between dev/staging/production host configurations |
| Postman | `brew install --cask postman` | API testing and development platform |

## Screenshot & Annotation

| Tool | Install | Description |
|------|---------|-------------|
| Snipaste | `brew install --cask snipaste` | Take screenshots and pin them to screen as floating windows. `F1` to capture and pin, `F3` to pin from clipboard |

## AI & LLM Tools

| Tool | Install | Description |
|------|---------|-------------|
| Ollama | `brew install --cask ollama` | Local LLM runtime — run Llama, Mistral, Qwen, DeepSeek and other models locally |
| LM Studio | `brew install --cask lm-studio` | GUI for browsing, downloading, and running local LLMs with in-app chat interface |
| QwenPaw | `curl -fsSL https://qwenpaw.agentscope.io/install.sh \| bash` or `pip install qwenpaw` | Personal AI agent framework from AgentScope — multi-model, IM integration (WeChat/Feishu/DingTalk), skill plugins |
| CC-Switch | `brew tap farion1231/ccswitch && brew install --cask cc-switch` | All-in-one config manager for Claude Code, Codex, Gemini CLI, OpenCode — switch providers, manage MCP/Skills from a GUI |

## Browser

| Tool | Install | Description |
|------|---------|-------------|
| Arc | `brew install --cask arc` | Modern Chromium-based browser with vertical tabs and spaces |
| Google Chrome | `brew install --cask google-chrome` | Standard web browser for development |

## Quick Install

```bash
# Essentials
brew install --cask visual-studio-code raycast rectangle

# Networking
brew install --cask tailscale switchhosts

# AI
brew install --cask ollama lm-studio
brew tap farion1231/ccswitch && brew install --cask cc-switch

# Screenshot
brew install --cask snipaste cleanshot-x
```
