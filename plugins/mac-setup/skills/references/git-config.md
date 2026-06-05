# Git Configuration Reference

Complete Git configuration for a new Mac, including alias system, global settings, and the resulting ~/.gitconfig template.

## Quick Setup Commands

Run these commands to set up the complete Git configuration:

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

# Global settings
git config --global pull.rebase true
git config --global core.excludesfile ~/.gitignore_global
git config --global core.editor vim
git config --global help.autocorrect 50
git config --global core.autocrlf input

# User info (replace with your own)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

## Alias Reference

| Alias | Command | Description |
|-------|---------|-------------|
| `git cm` | `git commit` | Commit changes |
| `git co` | `git checkout` | Switch branches |
| `git st` | `git status` | Check repo status |
| `git br` | `git branch` | List/create branches |
| `git lg` | `git log --color --graph ...` | Pretty log with graph |
| `git pl` | `git pull` | Pull from remote |
| `git rb` | `git rebase` | Rebase current branch |
| `git ad` | `git add` | Stage files |
| `git ps` | `git push` | Push to remote |

## Global Settings Explained

| Setting | Value | Description |
|---------|-------|-------------|
| `pull.rebase` | `true` | Use rebase instead of merge on pull |
| `core.excludesfile` | `~/.gitignore_global` | Global gitignore file |
| `core.editor` | `vim` | Use vim for commit messages |
| `help.autocorrect` | `50` | Auto-correct mistyped commands |
| `core.autocrlf` | `input` | Handle line endings on macOS |

## Resulting ~/.gitconfig

After running the commands above, `~/.gitconfig` will contain:

```ini
[user]
    name = Your Name
    email = your@email.com

[alias]
    cm = commit
    co = checkout
    st = status
    br = branch
    lg = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
    pl = pull
    rb = rebase
    ad = add
    ps = push

[pull]
    rebase = true

[core]
    excludesfile = ~/.gitignore_global
    editor = vim
    autocrlf = input

[help]
    autocorrect = 50
```

## Global Gitignore

Create a `~/.gitignore_global` file for patterns you want to ignore across all repos:

```bash
cat > ~/.gitignore_global << 'EOF'
# macOS
.DS_Store
.AppleDouble
.LSOverride
._*
.Spotlight-V100
.Trashes

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.env.local
EOF
```

## GPG Signing (Optional)

For signed commits:

```bash
brew install gpg2

# Generate a key
gpg --full-generate-key

# List keys
gpg --list-secret-keys --keyid-format=long

# Configure Git to use GPG
git config --global gpg.program gpg
git config --global commit.gpgsign true
git config --global user.signingkey <YOUR_GPG_KEY_ID>
```
