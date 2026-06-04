# iTerm2 Configuration Reference

Complete iTerm2 setup guide including installation, keyboard shortcuts, themes, Shell Integration, triggers, and advanced features.

## Installation

```bash
brew install --cask iterm2
```

## Essential Keyboard Shortcuts

### Window & Tabs

| Shortcut | Action |
|----------|--------|
| `Cmd + N` | New window |
| `Cmd + T` | New tab |
| `Cmd + W` | Close current tab |
| `Cmd + 1-9` | Switch to tab N |
| `Cmd + Shift + I` | Broadcast input to all tabs |

### Split Panes

| Shortcut | Action |
|----------|--------|
| `Cmd + D` | Vertical split (left/right) |
| `Cmd + Shift + D` | Horizontal split (top/bottom) |
| `Cmd + [` / `Cmd + ]` | Switch between panes |
| `Cmd + Option + Arrow` | Resize panes |
| `Cmd + Shift + Enter` | Maximize/restore current pane |

### Text Operations

| Shortcut | Action |
|----------|--------|
| `Cmd + F` | Find in current output |
| Double-click | Select word |
| Triple-click | Select entire line |
| `Cmd + Drag` | Select rectangular area |
| `Cmd + Click` | Open link/file |

### Screen Control

| Shortcut | Action |
|----------|--------|
| `Cmd + K` | Clear screen (keep history) |
| `Cmd + R` | Clear screen & history |
| `Cmd + Up/Down` | Scroll to top/bottom |

### Command Line (works in all terminals)

| Shortcut | Action |
|----------|--------|
| `Ctrl + A` | Cursor to line start |
| `Ctrl + E` | Cursor to line end |
| `Ctrl + U` | Delete before cursor |
| `Ctrl + K` | Delete after cursor |
| `Ctrl + W` | Delete word before cursor |
| `Ctrl + R` | Reverse search history |

## Appearance Settings

### Color Scheme

**Set via:** `Preferences (Cmd+,) > Profiles > Colors > Color Presets`

Recommended themes:
- **Solarized Dark** — Classic, easy on eyes
- **Dracula** — Popular dark theme
- **Tokyo Night** — Modern dark theme
- **Catppuccin Mocha** — Soft pastel dark theme

**Import third-party themes:**

1. Download themes from https://iterm2colorschemes.com/
2. In iTerm2: `Preferences > Profiles > Colors > Color Presets > Import...`
3. Select downloaded `.itermcolors` file
4. Choose the imported theme from `Color Presets`

### Font

**Set via:** `Preferences > Profiles > Text > Font`

Recommended fonts (require Nerd Font for icons):

```bash
brew install --cask font-hack-nerd-font
brew install --cask font-jetbrains-mono-nerd-font
brew install --cask font-meslo-lg-nerd-font
```

Recommended settings:
- Font: `MesloLGS Nerd Font` or `JetBrainsMono Nerd Font`
- Size: 13-14pt
- Enable: `Use built-in Powerline glyphs`

### Window Appearance

**Set via:** `Preferences > Profiles > Window`

- **Transparency:** Set to 10-15%
- **Blur:** Enable for frosted glass effect
- **Columns:** 120
- **Rows:** 35

## Shell Integration

Shell Integration provides enhanced features like command history navigation, current directory in Finder, and more.

```bash
curl -L https://iterm2.com/shell_integration/zsh -o ~/.iterm2_shell_integration.zsh
echo "source ~/.iterm2_shell_integration.zsh" >> ~/.zshrc
```

## Triggers

**Set via:** `Preferences > Profiles > Advanced > Triggers`

Triggers automatically respond to terminal output with actions. Click "Edit" to add triggers.

### Useful Trigger Examples

**Error highlighting:**
- Regular Expression: `(?i)(error|fail|exception|fatal)`
- Action: `Highlight Text`
- Parameters: `Foreground: #ff0000`

**Warning highlighting:**
- Regular Expression: `(?i)(warn|warning)`
- Action: `Highlight Text`
- Parameters: `Foreground: #ffcc00`

**URL detection (enhanced):**
- Regular Expression: `(https?://[^\s]+)`
- Action: `Open URL`

## Hotkey Window (Global Terminal)

**Set via:** `Preferences > Keys > Hotkey`

1. Check "Show/hide all windows with a system-wide hotkey"
2. Set hotkey: `Option + Space` (recommended)
3. Select a profile to use for the hotkey window

This lets you toggle a terminal overlay from any application.

## Status Bar

**Set via:** `Preferences > Profiles > Session > Configure Status Bar`

Drag components to "Active Components":
- CPU usage
- Memory usage
- Current directory
- Git branch
- Battery level
- Clock

Enable `Auto-Rainbow` for colorful status bar segments.

## Advanced Features

### Instant Replay

- Shortcut: `Cmd + Option + B`
- Use arrow keys to browse through recent terminal output like a video

### Password Manager

- Shortcut: `Cmd + Option + F`
- Store and auto-fill frequently used passwords

### Automatic Session Logging

**Set via:** `Preferences > Profiles > Session`
- Check "Automatically log session input to files in"
- Choose a log directory (e.g., `~/Documents/iTerm2-Logs`)

### Working Directory Reuse

**Set via:** `Preferences > Profiles > General`
- Set "Working Directory" to "Reuse previous session's directory"

### Scrollback Buffer

**Set via:** `Preferences > Profiles > Terminal`
- Set "Scrollback lines" to `10000` (or higher for heavy usage)

### Left Option Key

**Set via:** `Preferences > Profiles > Keys`
- Set "Left Option Key" to `Esc+` (enables Alt key shortcuts in terminal)
