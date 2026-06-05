# Development Language Environment Reference

Language version managers and runtime configurations for Mac development.

## Node.js

### nvm (Node Version Manager)

```bash
# Install nvm via Homebrew
brew install nvm

# Add to ~/.zshrc
export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"
[ -s "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm" ] && \. "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm"
```

Usage:
```bash
nvm install 20          # Install Node.js 20 LTS
nvm install --lts       # Install latest LTS
nvm use 20              # Switch to Node.js 20
nvm alias default 20    # Set default version
nvm ls                  # List installed versions
```

### fnm (Fast Node Manager)

```bash
brew install fnm

# Add to ~/.zshrc
eval "$(fnm env --use-on-cd)"
```

Usage:
```bash
fnm install 20
fnm use 20
fnm default 20
```

### pnpm (Package Manager)

```bash
brew install pnpm
# Or via corepack (comes with Node.js 16+)
corepack enable
```

## Python

### pyenv

```bash
brew install pyenv

# Add to ~/.zshrc
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Usage:
```bash
pyenv install 3.12        # Install Python 3.12
pyenv global 3.12         # Set global default
pyenv local 3.11          # Set project-specific version
pyenv versions            # List installed versions
```

### uv (Modern Python Package Manager)

```bash
brew install uv
```

Usage:
```bash
uv init myproject         # Create new project
uv add requests           # Add dependency
uv run python main.py     # Run with virtual env
uv sync                   # Sync dependencies
```

### pip Mirror (China)

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## Java

### sdkman

```bash
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Add to ~/.zshrc
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
```

Usage:
```bash
sdk list java                # List available Java versions
sdk install java 21.0.2-tem # Install Temurin JDK 21
sdk use java 21.0.2-tem      # Use specific version
sdk default java 21.0.2-tem  # Set default
```

### jenv (Java Version Switcher)

```bash
brew install jenv

# Add to ~/.zshrc
export PATH="$HOME/.jenv/bin:$PATH"
eval "$(jenv init -)"
```

Usage:
```bash
jenv add /path/to/jdk/home   # Register a JDK
jenv versions                 # List registered versions
jenv global 21                # Set global version
jenv local 17                 # Set project version
```

## Go

Go doesn't need a version manager for most use cases. Install directly:

```bash
brew install go
```

Verify:
```bash
go version
go env GOPATH
```

Set up workspace (traditional):
```bash
mkdir -p ~/go/{bin,src,pkg}
```

Go module proxy (China):
```bash
go env -w GOPROXY=https://goproxy.cn,direct
```

## Rust

### rustup

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
```

Usage:
```bash
rustup update               # Update Rust
rustup default stable       # Set default toolchain
rustup component add clippy # Add clippy linter
rustup component add rustfmt # Add formatter
cargo new myproject         # Create new project
cargo build --release       # Build optimized binary
```

## Docker

### OrbStack (Recommended, lightweight Docker alternative)

```bash
brew install --cask orbstack
```

OrbStack is significantly lighter than Docker Desktop and works seamlessly on Apple Silicon.

### Docker Desktop

```bash
brew install --cask docker
```

### China Mirror (Docker)

Edit or create `~/.docker/daemon.json`:

```json
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://registry.docker-cn.com"
  ]
}
```

## Database Tools

```bash
# PostgreSQL
brew install postgresql@17

# MySQL
brew install mysql

# Redis
brew install redis

# MongoDB
brew install mongodb-community

# SQLite browser
brew install --cask db-browser-for-sqlite
```

## Quick Setup by Language

| Language | Manager | Install Command | Shell Config |
|----------|---------|----------------|--------------|
| Node.js | nvm | `brew install nvm` | See above |
| Python | pyenv | `brew install pyenv` | See above |
| Java | sdkman | `curl -s "https://get.sdkman.io" \| bash` | See above |
| Go | (none) | `brew install go` | (none needed) |
| Rust | rustup | `curl ...sh.rustup.rs \| sh` | `source ~/.cargo/env` |
| Docker | OrbStack | `brew install --cask orbstack` | (none needed) |
