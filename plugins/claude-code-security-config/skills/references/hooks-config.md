# Hook Configuration

## Overview

Claude Code hooks allow you to run custom commands before or after tool execution. The `PostToolUse` hook can automatically clean up temporary files created by skills.

## Auto-Cleanup Hook

### Purpose

Skills like PPT generation create temporary Python scripts in the project root. This hook automatically removes them after execution.

### Configuration

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "find . -maxdepth 1 -name '*.py' -newer /tmp/.claude-skill-marker -delete && touch /tmp/.claude-skill-marker",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

### How It Works

1. After every Bash command, the hook runs
2. It finds `.py` files in the current directory newer than the marker
3. Deletes them and updates the marker timestamp
4. Only affects root-level `.py` files (not in subdirectories)

### Customization

**Clean up different file types:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "find . -maxdepth 1 \\( -name '*.py' -o -name '*.js' -o -name '*.tmp' \\) -newer /tmp/.claude-skill-marker -delete && touch /tmp/.claude-skill-marker",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

**Clean up in specific directories only:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "find /tmp/frontend-slides -name '*.py' -mmin +30 -delete 2>/dev/null; true",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

## Merging with Existing Hooks

If `hooks` already exists in your settings:

1. Read current settings
2. Check if `PostToolUse` array exists
3. If yes, append the new hook (don't overwrite)
4. If no, add the entire `hooks` block

Example merge:

```json
// Before
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [{ "type": "command", "command": "echo 'writing'" }]
      }
    ]
  }
}

// After
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [{ "type": "command", "command": "echo 'writing'" }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "find . -maxdepth 1 -name '*.py' -newer /tmp/.claude-skill-marker -delete && touch /tmp/.claude-skill-marker",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

## Other Useful Hooks

### Log All Bash Commands

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date): $CLAUDE_BASH_COMMAND\" >> ~/.claude/bash-history.log",
            "timeout": 1000
          }
        ]
      }
    ]
  }
}
```

### Warn Before Large File Writes

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo '⚠️ Writing file...'",
            "timeout": 1000
          }
        ]
      }
    ]
  }
}
```

## Testing

1. Add the hook to settings
2. Restart Claude Code
3. Ask Claude to create a temp file: `创建一个 test.py 文件`
4. After the Bash command completes, verify the file is cleaned up
