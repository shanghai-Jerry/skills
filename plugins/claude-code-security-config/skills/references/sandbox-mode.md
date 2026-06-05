# Sandbox Mode

## Overview

Sandbox mode restricts Claude Code to only access files within the current working directory. It prevents the AI from reading files outside the project, including sensitive system files.

## Enabling Sandbox

### Method 1: Environment Variable (Persistent)

Add to `~/.zshrc` or `~/.bashrc`:

```bash
export CLAUDE_CODE_SANDBOX=1
```

Then reload:

```bash
source ~/.zshrc
```

### Method 2: Command Line Flag (Per-Session)

```bash
claude --sandbox
```

### Method 3: Check Current Status

```bash
echo $CLAUDE_CODE_SANDBOX
# "1" = enabled, empty/unset = disabled
```

## Feature Comparison

| Feature | Sandbox ON | Sandbox OFF |
|---------|-----------|-------------|
| Read project files | ✅ | ✅ |
| Write project files | ✅ | ✅ |
| Run project scripts | ✅ | ✅ |
| Install packages | ⚠️ Limited | ✅ |
| Read ~/.ssh, ~/.aws | ❌ | ✅ |
| Access files outside project | ❌ | ✅ |
| Use system commands | ⚠️ Limited | ✅ |

## When to Use Sandbox

### Recommended (Sandbox ON)

- Personal projects with sensitive data
- Open-source contributions
- Shared development machines
- CI/CD environments
- When you don't need cross-project file access

### Consider Off (Sandbox OFF)

- Monorepo setups that reference other projects
- Building tools that need system-wide access
- Debugging issues that span multiple projects
- When you explicitly need to read files outside the project

## Limitations

1. **Package installation:** Some package managers need access to global directories. Use `--sandbox` flag temporarily if needed.

2. **System commands:** Commands like `systemctl`, `launchctl`, or system-wide `npm install -g` may be restricted.

3. **Docker:** Docker commands may need additional permissions outside the sandbox.

4. **Git hooks:** Git hooks that access files outside the project may fail.

## Workarounds

### Temporary Sandbox Disable

```bash
# Disable for current session
unset CLAUDE_CODE_SANDBOX

# Re-enable after task
export CLAUDE_CODE_SANDBOX=1
```

### Project-Specific Settings

Use `.claude/settings.local.json` for project-specific overrides:

```json
{
  "permissions": {
    "allow": [
      "Read(../shared-libs/*)"
    ]
  }
}
```

## Testing

1. Enable sandbox: `export CLAUDE_CODE_SANDBOX=1`
2. Ask Claude to read a file outside the project: `请读取 ~/.zshrc`
3. Expected: Should fail or be restricted
