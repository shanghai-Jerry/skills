# .claudeignore Templates

## Overview

`.claudeignore` works like `.gitignore` — it tells Claude Code which files and directories to skip when reading the project. Place it in the project root.

## Universal Template

```gitignore
# Sensitive config files
.env
.env.*
*.pem
*.key
*.secret
.secrets/
credentials/
config/secrets.yml

# System sensitive directories
~/.ssh/
~/.aws/
~/.gnupg/
~/.docker/
~/.npmrc
```

## Project-Type Templates

### Node.js / TypeScript

```gitignore
# Sensitive config files
.env
.env.*
*.pem
*.key
*.secret
.secrets/
credentials/

# Dependencies
node_modules/

# Build artifacts
dist/
build/
.next/
.nuxt/

# IDE
.vscode/settings.json
.idea/

# OS
.DS_Store
Thumbs.db
```

### Python

```gitignore
# Sensitive config files
.env
.env.*
*.pem
*.key
*.secret
.secrets/
credentials/

# Virtual environments
venv/
.venv/
env/

# Python cache
__pycache__/
*.pyc
*.pyo

# Jupyter
.ipynb_checkpoints/

# Distribution
dist/
build/
*.egg-info/
```

### Go

```gitignore
# Sensitive config files
.env
.env.*
*.pem
*.key
*.secret
.secrets/
credentials/

# Dependencies
vendor/

# Build artifacts
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary
*.test

# Output
*.out
```

### Rust

```gitignore
# Sensitive config files
.env
.env.*
*.pem
*.key
*.secret
.secrets/
credentials/

# Build
target/

# Cargo lock (for libraries)
Cargo.lock
```

### Docker / Kubernetes

```gitignore
# Sensitive config files
.env
.env.*
*.pem
*.key
*.secret
.secrets/
credentials/

# Docker
.docker/

# Kubernetes
kubeconfig
*.kubeconfig

# Helm
charts/*.tgz
```

## Syntax Reference

| Pattern | Meaning |
|---------|---------|
| `*.ext` | All files with extension |
| `filename` | Exact filename |
| `dir/` | Directory and contents |
| `**/pattern` | Pattern anywhere in path |
| `!pattern` | Negation (include despite earlier rule) |
| `# comment` | Comment (ignored) |

## Adding to a Project

1. Check if `.claudeignore` already exists
2. If yes, merge new patterns (don't overwrite)
3. If no, create with the appropriate template
4. Verify: `cat .claudeignore`
