# Permission Deny Rules

## Overview

Claude Code's `permissions.deny` in `~/.claude/settings.json` prevents the AI from reading sensitive files or executing dangerous commands. Deny rules take precedence over allow rules.

## Default Deny Rules

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

## Rule Patterns Explained

| Pattern | Blocks | Notes |
|---------|--------|-------|
| `Read(*/.ssh/*)` | Reading any SSH key | Covers id_rsa, authorized_keys, etc. |
| `Read(*/.aws/credentials)` | AWS credential file | Only the credentials file |
| `Read(*/.env*)` | All .env files | .env, .env.local, .env.production |
| `Read(*/secrets/*)` | Anything in secrets/ dirs | Common in Rails, Django projects |
| `Read(*/.gnupg/*)` | GPG keys | Private key material |
| `Read(*/.npmrc)` | npm auth tokens | Often contains registry tokens |
| `Read(*/.docker/config.json)` | Docker auth | Registry credentials |
| `Read(*/.pem)` | PEM certificate files | SSL certs with private keys |
| `Read(*/.key)` | Key files | Generic private key extension |
| `Bash(cat */.ssh/*)` | cat via Bash | Prevents indirect reading |
| `Bash(cat */.env*)` | cat .env via Bash | Same for env files |
| `Bash(cat */.aws/*)` | cat AWS files | Same for AWS creds |

## Customization

### Add More Sensitive Patterns

```json
{
  "permissions": {
    "deny": [
      "...existing rules...",
      "Read(*/.kube/config)",
      "Read(*/.azure/accessTokens)",
      "Read(*/.config/gcloud/*)",
      "Read(*/.credentials/*)",
      "Read(*/.netrc)",
      "Read(*/.htpasswd)"
    ]
  }
}
```

### Allow Specific Files in Otherwise-Denied Directories

If you need Claude to read specific files in sensitive directories:

```json
{
  "permissions": {
    "deny": [
      "Read(*/.ssh/*)"
    ],
    "allow": [
      "Read(*/.ssh/config)"
    ]
  }
}
```

Note: Deny rules still take precedence. To truly allow, remove the deny rule and be more specific.

## Merging with Existing Settings

When adding deny rules to an existing `settings.json`:

1. Read the current file
2. Check if `permissions` already exists
3. If yes, merge `deny` arrays (don't overwrite)
4. If no, add the entire `permissions` block

Example merge:

```json
// Before
{
  "permissions": {
    "allow": ["Read(./src/*)"]
  }
}

// After
{
  "permissions": {
    "allow": ["Read(./src/*)"],
    "deny": [
      "Read(*/.ssh/*)",
      "Read(*/.aws/credentials)"
    ]
  }
}
```

## Testing

After configuring, test with:

```
请读取 ~/.ssh/id_rsa
```

Expected: Claude should refuse with a permission error.
