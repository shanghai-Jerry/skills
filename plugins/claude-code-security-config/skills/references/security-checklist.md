# Security Checklist & Verification

## Verification Steps

After configuring security settings, run through these checks:

### 1. Test Deny Rules

Ask Claude:

```
请读取 ~/.ssh/id_rsa
```

**Expected:** Claude should refuse with a permission error.

Also test:

```
请读取 ~/.aws/credentials
请读取 .env 文件
```

### 2. Test Sandbox Mode

With sandbox enabled (`export CLAUDE_CODE_SANDBOX=1`):

```
请读取 ~/.zshrc
```

**Expected:** Should fail or be restricted to project directory.

### 3. Test .claudeignore

If you have a `.env` file in your project:

```
请读取 .env 文件的内容
```

**Expected:** Claude should not be able to read it (if .env is in .claudeignore).

### 4. Test Hooks

Create a test:

```bash
# Ask Claude to create a temp file
echo "print('test')" > test.py

# Check if it gets cleaned up after the next Bash command
ls -la test.py
```

**Expected:** The file should be removed after the hook runs.

### 5. Check Workspace

Look for any temp files:

```bash
ls -la *.py *.js *.tmp 2>/dev/null
```

**Expected:** No auto-generated temp files should remain.

## Rollback Guide

If something goes wrong, here's how to undo each change:

### 1. Restore settings.json

```bash
# If you made a backup
cp ~/.claude/settings.json.bak ~/.claude/settings.json

# Or manually remove deny rules and hooks
```

### 2. Remove Sandbox

```bash
# Remove from ~/.zshrc or ~/.bashrc
# Find and delete: export CLAUDE_CODE_SANDBOX=1

# Or just unset for current session
unset CLAUDE_CODE_SANDBOX
```

### 3. Remove .claudeignore

```bash
rm .claudeignore
```

### 4. Remove Security Rules from CLAUDE.md

Open `CLAUDE.md` and delete the `## 安全规则` section.

### 5. Remove Hooks

Edit `~/.claude/settings.json` and remove the `hooks` block.

## Common Issues

### "Permission denied" for legitimate files

**Problem:** Claude can't read a file you need.

**Solution:** Add an allow rule in `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": ["Read(./specific-file.txt)"]
  }
}
```

### Sandbox blocks package installation

**Problem:** `npm install` or `pip install` fails in sandbox mode.

**Solution:** Temporarily disable sandbox:

```bash
unset CLAUDE_CODE_SANDBOX
npm install
export CLAUDE_CODE_SANDBOX=1
```

### Hook deletes files you want to keep

**Problem:** The cleanup hook removes Python files you created manually.

**Solution:** Use a more specific pattern or disable the hook:

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

## Security Best Practices

1. **Layered defense:** Use multiple methods (deny rules + sandbox + .claudeignore)
2. **Least privilege:** Only allow what's needed, deny everything else
3. **Regular audits:** Check settings periodically
4. **Backup configs:** Always backup before changes
5. **Test changes:** Verify each security measure works as expected
