---
name: claude-code-security-config
description: "Configure Claude Code security to prevent sensitive file leaks and workspace pollution. Sets up deny rules for credentials, .claudeignore, sandbox mode, security instructions in CLAUDE.md, and auto-cleanup hooks. Use this skill when the user mentions security configuration, protecting sensitive files, preventing credential leaks, setting up .claudeignore, sandbox mode, Claude Code hardening, or wants to secure their Claude Code environment."
---

# Claude Code Security Configuration

A guided skill for hardening Claude Code's security posture — prevents reading sensitive files, avoids personal data leaks, and stops skills from polluting workspaces with temporary files.

## Architecture

```
claude-code-security-config/
├── SKILL.md                          ← You are here. Core flow and interaction strategy.
└── references/
    ├── permission-rules.md           ← Deny rules for ~/.claude/settings.json
    ├── claudeignore-templates.md     ← .claudeignore patterns by project type
    ├── sandbox-mode.md               ← Sandbox configuration and trade-offs
    ├── hooks-config.md               ← PostToolUse hooks for temp file cleanup
    └── security-checklist.md         ← Verification steps and rollback guide
```

Read reference files on demand based on the user's needs at each stage.

## Interaction Strategy

This is a **guided, not automated** configuration. Follow these principles:

- **Ask before acting.** Each stage starts by understanding the user's current setup. Don't overwrite configs blindly.
- **One stage at a time.** Complete the current stage before moving to the next.
- **Backup first.** Before modifying `~/.claude/settings.json`, always create a backup.
- **Idempotent.** All operations are safe to re-run. Check if a rule already exists before adding it.
- **Offer choices.** Some settings have trade-offs (e.g., sandbox mode limits functionality). Present options and let the user decide.

## Stage 1: Assessment

Before making changes, assess the current security state:

```bash
# Check if ~/.claude/settings.json exists
cat ~/.claude/settings.json 2>/dev/null || echo "No global settings found"

# Check if .claudeignore exists in current project
cat .claudeignore 2>/dev/null || echo "No .claudeignore found"

# Check if sandbox is enabled
echo "CLAUDE_CODE_SANDBOX=${CLAUDE_CODE_SANDBOX:-not set}"

# Check if CLAUDE.md has security rules
grep -q "安全规则\|security" CLAUDE.md 2>/dev/null && echo "Security rules found" || echo "No security rules in CLAUDE.md"
```

Then ask the user:

1. Which stages do you want to configure? (All / Specific stages)
2. Do you have sensitive files in your home directory that you want to protect? (SSH keys, AWS credentials, etc.)
3. Are you concerned about skills creating temporary files in your workspace?

## Stage 2: Permission Deny Rules

Read `references/permission-rules.md` for the complete deny rule set and customization options.

Core deny rules to add to `~/.claude/settings.json`:

```json
{
  "permissions": {
    "deny": [
      "Read(*/.ssh/*)",
      "Read(*/.aws/credentials)",
      "Read(*/.env*)",
      "Read(*/secrets/*)",
      "Read(*/.gnupg/*)",
      "Read(*/.npmrc)",
      "Read(*/.docker/config.json)",
      "Read(*/.pem)",
      "Read(*/.key)",
      "Bash(cat */.ssh/*)",
      "Bash(cat */.env*)",
      "Bash(cat */.aws/*)"
    ]
  }
}
```

**Before applying:**

1. Read the current `~/.claude/settings.json`
2. Create a backup: `cp ~/.claude/settings.json ~/.claude/settings.json.bak`
3. Merge the deny rules with existing permissions (don't overwrite other settings)
4. Show the user the diff before saving

## Stage 3: .claudeignore

Read `references/claudeignore-templates.md` for templates by project type.

Create a `.claudeignore` file in the project root:

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

**Customize based on project type:**

- **Node.js projects:** Add `node_modules/`, `.env.local`
- **Python projects:** Add `venv/`, `.env.local`, `__pycache__/`
- **Go projects:** Add `vendor/`
- **Docker projects:** Add `.docker/`

## Stage 4: Sandbox Mode

Read `references/sandbox-mode.md` for detailed trade-offs.

Enable sandbox to restrict Claude Code to the current working directory:

```bash
# Option A: Environment variable (persistent)
echo 'export CLAUDE_CODE_SANDBOX=1' >> ~/.zshrc
source ~/.zshrc

# Option B: Command line flag (per-session)
claude --sandbox
```

**Trade-off discussion:**

| Feature | Sandbox ON | Sandbox OFF |
|---------|-----------|-------------|
| Read project files | ✅ | ✅ |
| Read ~/.ssh, ~/.aws | ❌ | ✅ |
| Access files outside project | ❌ | ✅ |
| Run scripts in project | ✅ | ✅ |
| Install packages | ⚠️ Limited | ✅ |

Recommend sandbox ON for most users. Suggest OFF only if the user needs cross-project file access.

## Stage 5: CLAUDE.md Security Rules

Add security instructions to the project's `CLAUDE.md`:

```markdown
## 安全规则
- 绝对不要读取项目目录外的文件
- 绝对不要访问 ~/.ssh, ~/.aws, ~/.gnupg 等凭证目录
- 绝对不要读取 .env 文件或包含密钥的文件
- 只读取用户明确请求的文件
- 遵守 .claudeignore 中定义的排除规则
```

**Check first:** If `CLAUDE.md` already exists, append the security section rather than overwriting.

## Stage 6: Auto-Cleanup Hooks

Read `references/hooks-config.md` for the complete hook configuration.

Add PostToolUse hook to `~/.claude/settings.json` for automatic temp file cleanup:

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

**Important:** Merge this with existing hooks configuration. Don't overwrite other hooks.

## Stage 7: .gitignore for Temp Files

Add to project `.gitignore`:

```gitignore
# Claude temp files
*.py
!scripts/*.py
.claude/
```

**Customize:** If the project already has Python files in the root, use a more specific pattern:

```gitignore
# Claude temp files (only auto-generated ones)
/tmp/
```

## Quick Reference

When the user asks about a specific topic, read the corresponding reference file:

| Topic | File |
|-------|------|
| Deny rules for settings.json | references/permission-rules.md |
| .claudeignore templates | references/claudeignore-templates.md |
| Sandbox mode details | references/sandbox-mode.md |
| Hook configuration | references/hooks-config.md |
| Verification & rollback | references/security-checklist.md |

## Verification

After configuration, run through these checks (read `references/security-checklist.md`):

1. **Test sensitive file access:** Ask Claude to read `~/.ssh/id_rsa` — should be denied
2. **Test sandbox:** In sandbox mode, try accessing files outside the project — should fail
3. **Test .claudeignore:** Check that ignored files are not read by Claude
4. **Test hooks:** Create a temp `.py` file and verify it gets cleaned up
5. **Check workspace:** Confirm no temp files remain in the project root

## Rollback

If anything goes wrong:

1. Restore `~/.claude/settings.json` from backup
2. Remove `CLAUDE_CODE_SANDBOX` from shell config
3. Delete `.claudeignore` if unwanted
4. Remove security section from `CLAUDE.md`
5. Remove hooks from settings.json
