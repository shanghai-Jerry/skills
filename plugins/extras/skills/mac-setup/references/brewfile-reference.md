# Brewfile Reference

Brewfile is the declarative configuration file for Homebrew that lets you batch install and manage packages.

## Basics

### Export Current Environment

After setting up your Mac with all desired packages:

```bash
# Export all installed packages and casks
brew bundle dump --file=~/Brewfile --force

# Export with descriptions
brew bundle dump --file=~/Brewfile --force --describe
```

### Restore on New Mac

```bash
# Install everything from Brewfile
brew bundle --file=~/Brewfile

# Check what would be installed (dry run)
brew bundle check --file=~/Brewfile --verbose
```

### Clean Up

```bash
# Uninstall packages not in Brewfile
brew bundle cleanup --file=~/Brewfile --force
```

## Brewfile Syntax

```ruby
# Command line tools (brew)
brew "git"
brew "ripgrep"
brew "fd"
brew "bat"

# Tap (third-party repositories)
tap "homebrew/cask-fonts"
tap "oven-sh/bun/brew"

# Cask (GUI applications)
cask "visual-studio-code"
cask "iterm2"

# Install with specific options
brew "python@3.12"

# Install from tap
brew "oven-sh/bun/bun"
```

## Recommended Brewfile Template

```ruby
# ============================================
# Brewfile - Mac Development Environment
# ============================================

# --- Taps ---
tap "homebrew/cask-fonts"
tap "homebrew/services"

# --- Command Line Tools ---
brew "git"
brew "ripgrep"
brew "fd"
brew "bat"
brew "fzf"
brew "zoxide"
brew "eza"
brew "jq"
brew "lazygit"
brew "gh"
brew "git-delta"
brew "htop"
brew "btop"
brew "tree"
brew "ncdu"
brew "tmux"
brew "vim"
brew "neovim"
brew "tldr"
brew "rsync"
brew "wget"
brew "protobuf"

# --- Languages & Runtimes ---
brew "node"
brew "python@3.12"
brew "go"
brew "nvm"
brew "pyenv"
brew "pnpm"

# --- Fonts ---
cask "font-hack-nerd-font"
cask "font-jetbrains-mono-nerd-font"
cask "font-meslo-lg-nerd-font"

# --- Terminal ---
cask "iterm2"

# --- Development Tools ---
cask "visual-studio-code"
cask "postman"
cask "docker"     # Or: cask "orbstack"

# --- Productivity ---
cask "raycast"
cask "rectangle"
cask "snipaste"
cask "switchhosts"
cask "bitwarden"
cask "obsidian"
cask "notion"

# --- Browsers ---
cask "google-chrome"
cask "arc"

# --- Communication ---
cask "discord"
cask "wechat"
cask "zoom"

# --- Media ---
cask "vlc"
cask "iina"        # Modern video player for macOS

# --- Database ---
brew "postgresql@17"
brew "redis"
```

## 2026 Recommended New Tools

These are newer tools worth considering:

```ruby
# Terminal alternatives
cask "warp"        # AI-powered modern terminal
cask "ghostty"     # GPU-accelerated terminal by Mitchell Hashimoto

# Code editors
cask "zed"         # High-performance editor
cask "cursor"      # AI-enhanced code editor

# Modern runtimes
brew "uv"          # Modern Python package manager
brew "bun"         # Fast JavaScript runtime

# Local AI
cask "ollama"      # Run LLMs locally

# Container tools
cask "orbstack"    # Lightweight Docker/Desktop alternative
```

## Usage Tips

### Keeping Brewfile in Sync

Add Brewfile to your dotfiles repository:

```bash
# Add to your dotfiles
cp ~/Brewfile ~/dotfiles/Brewfile
cd ~/dotfiles
git add Brewfile
git commit -m "Update Brewfile"
```

### Selective Installation

You don't need to install everything. Comment out categories you don't need, or create separate Brewfiles:

```bash
# Minimal dev setup
brew bundle --file=~/Brewfile.minimal

# Full setup
brew bundle --file=~/Brewfile.full
```

### Brewfile Health Check

```bash
# See what's missing from Brewfile
brew bundle check --file=~/Brewfile

# See what's installed but not in Brewfile
brew bundle cleanup --file=~/Brewfile --dry-run
```
