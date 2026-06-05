# Tmux Configuration Reference

Complete tmux configuration based on the CSDN article's ~/.tmux.conf, including C-a prefix, custom split shortcuts, mouse support, and status bar UI design.

## Installation

```bash
# macOS
brew install tmux

# Linux (Debian/Ubuntu)
apt-get install tmux
```

## Quick Reference: Default Prefix

By default, tmux uses `Ctrl+b` as the prefix key. The configuration below changes it to `Ctrl+a`.

Common usage pattern: **Press Ctrl+a, release both keys, then press the command key.**

## Common Shortcuts (Before Custom Config)

| Shortcut | Action |
|----------|--------|
| `C-b ,` | Rename current window |
| `C-b z` | Toggle pane fullscreen |
| `C-b c` | Create new window |
| `C-b d` | Detach from session |
| `C-b p` | Previous window |
| `C-b n` | Next window |
| `C-b <number>` | Switch to window by number |
| `C-b %` | Split panes left/right |
| `C-b "` | Split panes top/bottom |
| `C-b Arrow` | Switch between panes |
| `C-b [` | Enter scroll/copy mode |
| `C-b ?` | List all keybindings |

## Complete ~/.tmux.conf Template

```bash
# ============================================
# ~/.tmux.conf - Tmux Configuration
# ============================================

# --- Prefix Key ---
# Change prefix from Ctrl-b to Ctrl-a
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# --- Split Panes ---
# Use | for vertical split, - for horizontal split
bind | split-window -h
bind - split-window -v
unbind '"'
unbind %

# --- Reload Config ---
bind r source-file ~/.tmux.conf \; display "Config reloaded!"

# --- Pane Navigation ---
# Switch panes using Alt+Arrow (no prefix needed)
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# --- Mouse Support ---
set -g mouse on

# --- Window Settings ---
set-option -g allow-rename off
set -g base-index 1          # Start window numbering at 1
setw -g pane-base-index 1    # Start pane numbering at 1

# --- Design Tweaks ---

# Disable bell sounds
set -g visual-activity off
set -g visual-bell off
set -g visual-silence off
setw -g monitor-activity off
set -g bell-action none

# Clock mode
setw -g clock-mode-colour colour1

# Copy mode
setw -g mode-style 'fg=colour1 bg=colour18 bold'

# Pane borders
set -g pane-border-style 'fg=colour1'
set -g pane-active-border-style 'fg=colour3'

# --- Status Bar ---
set -g status-position bottom
set -g status-justify left
set -g status-style 'fg=colour1'
set -g status-left ''
set -g status-right '%Y-%m-%d %H:%M '
set -g status-right-length 50
set -g status-left-length 10

# Current window style
setw -g window-status-current-style 'fg=colour0 bg=colour1 bold'
setw -g window-status-current-format ' #I #W #F '

# Other windows style
setw -g window-status-style 'fg=colour1 dim'
setw -g window-status-format ' #I #[fg=colour7]#W #[fg=colour1]#F '

# Bell window style
setw -g window-status-bell-style 'fg=colour2 bg=colour1 bold'

# --- Messages ---
set -g message-style 'fg=colour2 bg=colour0 bold'

# --- Increase history limit ---
set -g history-limit 10000
```

## Key Shortcuts with Custom Config

After applying the config above, these are the key shortcuts:

### Session Management

| Shortcut | Action |
|----------|--------|
| `C-a` | Prefix key (replaces Ctrl+b) |
| `C-a d` | Detach from session |
| `C-a r` | Reload tmux config |
| `tmux ls` | List sessions |
| `tmux attach -t <name>` | Reattach to session |
| `tmux new -s <name>` | New named session |

### Window Management

| Shortcut | Action |
|----------|--------|
| `C-a c` | Create new window |
| `C-a <number>` | Switch to window N |
| `C-a p` | Previous window |
| `C-a n` | Next window |
| `C-a ,` | Rename window |
| `C-a w` | List all windows |

### Pane Management

| Shortcut | Action |
|----------|--------|
| `C-a |` | Split vertical (left/right) |
| `C-a -` | Split horizontal (top/bottom) |
| `Alt + Arrow` | Switch panes (no prefix!) |
| `C-a z` | Toggle pane fullscreen |
| `C-a x` | Close current pane |

### Copy Mode

| Shortcut | Action |
|----------|--------|
| `C-a [` | Enter copy mode |
| `q` | Exit copy mode |
| `v` | Start selection (in copy mode) |
| `y` | Yank (copy) selection |

### Scroll

With mouse enabled (`set -g mouse on`), you can scroll with mouse wheel or trackpad. For keyboard scrolling:

| Shortcut | Action |
|----------|--------|
| `C-a [` then `Up/Down` | Scroll through history |
| `C-a [` then `PgUp/PgDn` | Page scroll |

## TPM (Tmux Plugin Manager)

Optional: install TPM for additional plugins:

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

Add to ~/.tmux.conf:

```bash
# Plugin manager
set -g @plugin 'tmux-plugins/tpm'

# Plugins
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'     # Save/restore sessions
set -g @plugin 'tmux-plugins/tmux-continuum'     # Auto-save sessions

# Initialize TPM (must be at the very bottom of tmux.conf)
run '~/.tmux/plugins/tpm/tpm'
```

Install plugins: press `C-a I` in tmux.
