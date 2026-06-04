---
name: mac-setup
description: "Configure a new Mac development environment from scratch. Covers Homebrew, Git, Zsh/Oh My Zsh, iTerm2, tmux, vim, ssh, and modern CLI tools. Use this skill whenever the user mentions setting up a new Mac, configuring their computer, installing dev tools, Mac environment setup, brew install, terminal configuration, dotfiles, or wants help with their macOS development environment. Also trigger for specific tool configs like 'configure iTerm2', 'set up tmux', 'configure git aliases', 'install Homebrew', 'configure zsh', or 'set up ssh keys'."
---

# Mac Setup

A skill for configuring a new Mac development environment. Guides the user through 5 stages of setup, from basic tools to system optimization.

## Architecture

```
mac-setup/
├── SKILL.md                          ← You are here. Core flow and interaction strategy.
└── references/
    ├── git-config.md                 ← Git alias system + ~/.gitconfig template
    ├── zsh-config.md                 ← Oh My Zsh + ~/.myzshrc template (proxy/k8s/bazel/protoc functions)
    ├── iterm2-config.md              ← iTerm2 full config (shortcuts/themes/triggers/Shell Integration)
    ├── vim-config.md                 ← ~/.vimrc complete template
    ├── tmux-config.md                ← ~/.tmux.conf complete template (C-a prefix/mouse/UI design)
    ├── ssh-config.md                 ← ~/.ssh/config format + port forwarding
    ├── cli-tools.md                  ← Modern CLI tools (ripgrep/fzf/lazygit/tldr/opencode/claude code/openskills)
    ├── gui-apps.md                   ← GUI applications by category (editors/networking/AI tools/productivity)
    ├── dev-languages.md              ← Language version managers (nvm/pyenv/sdkman/rustup)
    ├── brewfile-reference.md         ← Brewfile syntax + templates + recommended apps
    ├── macos-defaults.md             ← macOS defaults commands for system preferences
    └── mirrors-china.md              ← China mirror sources for Homebrew/npm/pip/Go/Docker
```

Read reference files on demand based on the user's needs at each stage.

## Interaction Strategy

This is a **guided, not automated** setup. Follow these principles:

- **Ask before acting.** Each stage starts by understanding what the user needs. Don't dump commands blindly.
- **One stage at a time.** Complete the current stage before moving to the next.
- **Adapt to expertise.** Experienced developer? Skip explanations, just give commands. Beginner? Explain what each tool does and why.
- **Idempotent and safe.** All `brew install` commands are safe to re-run. Before overwriting config files (~/.zshrc, ~/.vimrc, etc.), always suggest backing up first.
- **Offer choices.** For tools with alternatives (iTerm2 vs Warp vs Ghostty, zsh vs bash), present options and let the user decide.

## Stage 1: Environment Assessment

Before any installation, assess the current state. Run these checks silently:

```bash
# macOS version and architecture
sw_vers && uname -m

# Check existing tools
for cmd in brew git zsh vim tmux ssh node python3 go; do
  printf "%-10s " "$cmd"
  if command -v "$cmd" &>/dev/null; then
    echo "✓ installed"
  else
    echo "✗ not found"
  fi
done
```

Then ask the user:

1. Is this a brand new Mac or are you adding tools to an existing setup?
2. What's your primary development focus? (Web/Backend/Mobile/Data Science/DevOps/Generic)
3. Are you in mainland China? (Determines whether to configure mirror sources)

Based on their answers, decide which stages need full setup vs. incremental optimization.

## Stage 2: Foundation Tools

### Xcode Command Line Tools

Essential for many command-line tools to work:

```bash
xcode-select --install
```

### Homebrew (Package Manager)

Install Homebrew if not present:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

For Apple Silicon (M1/M2/M3/M4), add Homebrew to PATH:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

For China users, see `references/mirrors-china.md` for mirror source configuration.

### Git Configuration

Read `references/git-config.md` for the complete Git alias system and configuration. The core setup includes:

```bash
# Aliases
git config --global alias.cm commit
git config --global alias.co checkout
git config --global alias.st status
git config --global alias.br branch
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
git config --global alias.pl pull
git config --global alias.rb rebase
git config --global alias.ad add
git config --global alias.ps push

# Settings
git config --global pull.rebase true
git config --global core.excludesfile ~/.gitignore_global
git config --global core.editor vim
git config --global help.autocorrect 50

# User info (prompt the user for their name and email)
git config --global user.name "User Name"
git config --global user.email "user@email.com"
```

### Protobuf (Optional)

```bash
brew install protobuf
```

## Stage 3: Terminal Enhancement

This is the most important stage. Guide the user through Shell configuration, terminal app setup, and editor config.

### Zsh + Oh My Zsh

Read `references/zsh-config.md` for the complete Zsh setup including:
- Oh My Zsh installation
- zsh-autosuggestions plugin
- Custom ~/.myzshrc template (proxy functions, k8s aliases, bazel commands, protoc functions)
- Powerlevel10k theme (optional but recommended)

Quick install:

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### Terminal Application

Recommend one of these and read `references/iterm2-config.md` for iTerm2 setup:
- **iTerm2** — Most feature-rich, classic choice (`brew install --cask iterm2`)
- **Warp** — Modern, AI-powered terminal (`brew install --cask warp`)
- **Ghostty** — Fast, GPU-accelerated (`brew install --cask ghostty`)
- **WezTerm** — Cross-platform, GPU-accelerated (`brew install --cask wezterm`)

### Nerd Font

Required for proper icon display in themes:

```bash
brew install --cask font-hack-nerd-font
brew install --cask font-jetbrains-mono-nerd-font
```

### Vim Configuration

Read `references/vim-config.md` for the complete ~/.vimrc template with indentation, folding, status bar, and color scheme.

## Stage 4: Development Tools

### tmux (Terminal Multiplexer)

Read `references/tmux-config.md` for the complete ~/.tmux.conf template with C-a prefix, mouse support, split shortcuts, and status bar UI design.

Install:

```bash
brew install tmux
```

### SSH Configuration

Read `references/ssh-config.md` for ~/.ssh/config format, host aliases, port forwarding, and key management.

### Language Version Managers

Read `references/dev-languages.md` for complete setup. Quick recommendations by language:

| Language | Manager | Install |
|----------|---------|---------|
| Node.js | nvm | See dev-languages.md |
| Python | pyenv | `brew install pyenv` |
| Java | sdkman | See dev-languages.md |
| Go | (none needed) | `brew install go` |
| Rust | rustup | See dev-languages.md |

### Modern CLI Tools

Read `references/cli-tools.md` for the complete list. Essentials:

```bash
# File & search
brew install ripgrep fd bat fzf zoxide eza

# Git enhancement
brew install lazygit gh git-delta

# Utilities
brew install jq htop
```

### OpenSkills (Skills Manager)

Install the OpenSkills manager to discover and install agent skills:

```bash
npm install -g openskills

# Verify installation
openskills --version
```

### GUI Applications

Read `references/gui-apps.md` for recommended GUI applications by category (code editors, productivity, networking, AI tools, browsers). Tailor recommendations based on the user's development focus.

## Stage 5: System Optimization

### macOS System Preferences

Read `references/macos-defaults.md` for batch system optimization via `defaults` commands covering Dock, Finder, trackpad, keyboard, screenshots, etc.

### Utility Tools

Read `references/cli-tools.md` for CLI utilities like `tldr`, `rsync`, `unison`.

Read `references/gui-apps.md` for GUI applications including:
- **Networking & Proxy** — Tailscale, ClashX, SwitchHosts
- **Screenshot & Annotation** — Snipaste, CleanShot X
- **AI & LLM** — Ollama, LM Studio, QwenPaw, CC-Switch

### Brewfile Export (Future Migration)

Read `references/brewfile-reference.md` for Brewfile management. After all installations are complete:

```bash
# Export current environment
brew bundle dump --file=~/Brewfile --force

# On a new Mac, restore everything
brew bundle --file=~/Brewfile
```

### China Mirror Sources (Optional)

Read `references/mirrors-china.md` if the user is in mainland China. Covers Homebrew, npm, pip, Go, Docker, and Ruby mirror configurations.

## Quick Reference

When the user asks about a specific topic, read the corresponding reference file:

| Topic | File |
|-------|------|
| Git aliases & config | references/git-config.md |
| Zsh/Oh My Zsh/.myzshrc | references/zsh-config.md |
| iTerm2 configuration | references/iterm2-config.md |
| Vim ~/.vimrc | references/vim-config.md |
| Tmux ~/.tmux.conf | references/tmux-config.md |
| SSH ~/.ssh/config | references/ssh-config.md |
| CLI tools (ripgrep/fzf/opencode/claude code/openskills) | references/cli-tools.md |
| GUI apps (editors/networking/AI/productivity) | references/gui-apps.md |
| Language managers | references/dev-languages.md |
| Brewfile | references/brewfile-reference.md |
| macOS defaults | references/macos-defaults.md |
| China mirrors | references/mirrors-china.md |
