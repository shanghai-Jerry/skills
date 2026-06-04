# CLI Tools Reference

Modern CLI tools and utilities for daily development workflow, plus the classic utility tools from the CSDN article.

## Modern CLI Essentials

### File Search & Navigation

| Tool | Replaces | Install | Description |
|------|----------|---------|-------------|
| `ripgrep` (rg) | grep | `brew install ripgrep` | Much faster text search |
| `fd` | find | `brew install fd` | Simpler file finding |
| `fzf` | Ctrl+R | `brew install fzf` | Fuzzy finder for files, history, git branches |
| `zoxide` | cd | `brew install zoxide` | Learns your habits, smart directory jumping |
| `eza` / `lsd` | ls | `brew install eza` or `brew install lsd` | Modern ls with icons, Git status, colors |

### File Viewing

| Tool | Replaces | Install | Description |
|------|----------|---------|-------------|
| `bat` | cat | `brew install bat` | File viewer with syntax highlighting and line numbers |
| `delta` | git diff | `brew install git-delta` | Beautiful, syntax-highlighted git diff |

### Git Enhancement

| Tool | Install | Description |
|------|---------|-------------|
| `lazygit` | `brew install lazygit` | Terminal UI for git operations |
| `gh` | `brew install gh` | GitHub CLI: manage PRs, Issues, Actions |
| `tig` | `brew install tig` | Interactive git viewer |

### AI Coding Assistants

| Tool | Install | Description |
|------|---------|-------------|
| opencode | `brew install opencode` | AI-powered CLI coding assistant with Skills/MCP/plugin support, multi-model |
| claude code | `npm install -g @anthropic-ai/claude-code` | Anthropic's official AI coding assistant in the terminal |

### Utilities

| Tool | Install | Description |
|------|---------|-------------|
| `jq` | `brew install jq` | Command-line JSON processor |
| `htop` / `btop` | `brew install htop btop` | System resource monitor |
| `tldr` | Multiple (see below) | Simplified man pages |
| `httpie` / `curlie` | `brew install httpie` | Human-friendly HTTP client |
| `ncdu` | `brew install ncdu` | Disk usage analyzer |
| `tree` | `brew install tree` | Directory tree display |
| `watchexec` | `brew install watchexec` | Run commands on file changes |
| `unison` | `brew install unison` | Bidirectional file/folder synchronization |

## Quick Install All Essentials

```bash
# File & search
brew install ripgrep fd fzf zoxide eza bat git-delta

# Git enhancement
brew install lazygit gh

# Utilities
brew install jq htop btop tree ncdu tldr
```

## Tool Configuration

### fzf (Fuzzy Finder)

```bash
# Install fzf key bindings and fuzzy completion
$(brew --prefix)/opt/fzf/install

# Or add to ~/.zshrc:
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
```

Useful shortcuts after setup:
- `Ctrl+R` — Fuzzy search through command history
- `Ctrl+T` — Fuzzy find and insert file path
- `Alt+C` — Fuzzy cd into subdirectory

### zoxide

Add to ~/.zshrc:

```bash
eval "$(zoxide init zsh)"
```

Usage: `z <partial-name>` jumps to the best matching directory.

### bat

```bash
# Set as default cat replacement (add to ~/.zshrc)
alias cat='bat --paging=auto'
```

### delta (Git Diff)

Add to ~/.gitconfig:

```ini
[core]
    pager = delta

[interactive]
    diffFilter = delta --color-only

[delta]
    navigate = true
    side-by-side = true
```

## Classic Utility Tools (from CSDN Article)

### tldr — Simplified Man Pages

Shows practical examples instead of full documentation:

```bash
# Install (choose one)
npm install -g tldr
pip3 install tldr
brew install tlrc

# Usage
tldr tar
tldr git log
```

### ydict — Command Line Dictionary

```bash
# Install
pip3 install ydict

# Usage
ydict hello
```

### rsync — File Synchronization

Usually pre-installed on macOS. Key usage:

```bash
# Copy local -> remote
rsync -avz --progress localdir/ user@host:/remote/path/

# Copy remote -> local
rsync -avz --progress user@host:/remote/path/ localdir/

# Preview changes (dry run)
rsync -avzn localdir/ user@host:/remote/path/

# Delete files on destination that don't exist on source
rsync -avz --delete localdir/ user@host:/remote/path/
```

### Unison — Bidirectional File Synchronization

Unison is a file-synchronization tool that allows two replicas of a collection of files and directories to be stored on different hosts (or different disks on the same host), modified separately, and then brought up to date by propagating the changes in each replica to the other.

Unlike rsync (which is unidirectional), Unison detects conflicts and handles bidirectional sync intelligently.

```bash
# Install
brew install unison

# Basic local sync (interactive — shows changes and asks for confirmation)
unison /path/to/source /path/to/destination

# Non-interactive batch mode (auto-propagate non-conflicting changes)
unison -batch /path/to/source /path/to/destination

# Remote sync (requires SSH access)
unison /local/path ssh://user@remotehost//remote/path

# Sync with specific SSH port
unison /local/path ssh://user@remotehost:2222//remote/path

# Prefer changes from source (auto-resolve conflicts in favor of source)
unison -prefer /path/to/source -batch /path/to/source /path/to/destination

# Sync with ignore patterns
unison -ignore='Path .git' -ignore='Name *.log' /source /destination

# Repeat sync every 30 seconds (useful for continuous backup)
unison -repeat 30 /source /destination

# Dry run — preview changes without applying them
unison -testserver /source /destination
```

Profile configuration (save to `~/.unison/default.prf`):

```
# Root directories to synchronize
root = /Users/edy/projects
root = /Volumes/backup/projects

# Paths to include (relative to root)
path = src
path = docs

# Paths to ignore
ignore = Path .git
ignore = Path node_modules
ignore = Path .DS_Store
ignore = Name *.tmp
ignore = Name .env*

# Auto-resolve conflicts
prefer = newer
auto = true
batch = true

# Logging
log = true
logfile = /var/log/unison.log
```

After creating the profile, simply run:

```bash
# Use default profile
unison

# Use a specific profile
unison work-sync
```

Key flags:

| Flag | Description |
|------|-------------|
| `-batch` | Run without user interaction (non-interactive) |
| `-auto` | Automatically accept non-conflicting changes |
| `-prefer newer` | Resolve conflicts by choosing the newer file |
| `-prefer <path>` | Resolve conflicts by preferring one replica |
| `-ignore 'Path ...'` | Exclude a directory or file path |
| `-ignore 'Name ...'` | Exclude by filename pattern |
| `-force <path>` | Force propagation from one side (use with caution) |
| `-repeat N` | Repeat sync every N seconds |
| `-testserver` | Verify connection without syncing |
| `-silent` | Suppress output |
| `-times` | Sync modification times (disabled by default on some systems) |

Typical use cases: keeping a laptop and desktop in sync, mirroring project directories to an external drive or NAS, maintaining identical dotfiles across machines, continuous backup of work in progress.

Important notes: both sides must have the same major version of Unison installed (e.g., 2.53.x on both). When using remote sync, Unison must be installed on both the local and remote machines. Unison stores synchronization state in `~/.unison/` on each host.

### colorls — Colorful ls

```bash
# Install (requires Ruby)
brew install ruby
gem install colorls

# Usage
colorls
colorls -la
colorls --tree
```


