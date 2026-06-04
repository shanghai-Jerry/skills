# SSH Configuration Reference

Complete SSH configuration guide including ~/.ssh/config format, host aliases, port forwarding, wildcard hosts, and key management.

## Generate SSH Key

```bash
# Generate a new key pair (Ed25519 recommended)
ssh-keygen -t ed25519 -C "your@email.com"

# Or RSA (legacy compatibility)
ssh-keygen -t rsa -b 4096 -C "your@email.com"
```

## Copy Public Key to Remote

```bash
# Standard method
ssh-copy-id user@hostname

# Manual method
cat ~/.ssh/id_ed25519.pub | ssh user@hostname "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

## ~/.ssh/config Template

```bash
# Create config if it doesn't exist
mkdir -p ~/.ssh && chmod 700 ~/.ssh
touch ~/.ssh/config && chmod 600 ~/.ssh/config
```

### Basic Host Configuration

```ssh-config
# Simple host alias
Host myserver
    User username
    HostName 192.168.1.100
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

### Complete Example with Port Forwarding

```ssh-config
# VM with port forwarding
Host vm
    User foobar
    HostName 172.16.174.141
    Port 2222
    IdentityFile ~/.ssh/id_rsa
    # Forward local port 9999 to remote port 8888
    LocalForward 9999 localhost:8888

# GitHub
Host github.com
    User git
    HostName github.com
    IdentityFile ~/.ssh/id_ed25519

# Production server
Host prod
    User deploy
    HostName prod.example.com
    Port 22
    IdentityFile ~/.ssh/work_key
    # Keep connection alive
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

### Wildcard Hosts

```ssh-config
# Apply settings to all hosts matching pattern
Host *.mit.edu
    User foobaz
    ForwardAgent yes

# All internal servers
Host 10.* 192.168.*
    User admin
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
```

## SSH Config Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `HostName` | Remote server address | `192.168.1.100` |
| `Port` | SSH port number | `2222` |
| `User` | Default username | `deploy` |
| `IdentityFile` | SSH private key path | `~/.ssh/id_ed25519` |
| `LocalForward` | Forward local port to remote | `9999 localhost:8888` |
| `RemoteForward` | Forward remote port to local | `3000 localhost:3000` |
| `ForwardAgent` | Forward SSH agent | `yes` |
| `ServerAliveInterval` | Keepalive interval (seconds) | `60` |
| `ServerAliveCountMax` | Max keepalive misses | `3` |
| `ProxyCommand` | Connect through proxy/bastion | `ssh -W %h:%p bastion` |
| `StrictHostKeyChecking` | Verify host key | `no` (for dynamic hosts) |
| `UserKnownHostsFile` | Known hosts file | `/dev/null` (ignore) |

## Port Forwarding

### Local Port Forwarding

Access remote service through local port:

```bash
# Access remote MySQL (port 3306) via local port 3307
ssh -L 3307:localhost:3306 user@remote

# Or in ~/.ssh/config
LocalForward 3307 localhost:3306
```

### Remote Port Forwarding

Expose local service to remote network:

```bash
# Allow remote to access local port 8080
ssh -R 8080:localhost:8080 user@remote
```

### Dynamic Port Forwarding (SOCKS Proxy)

```bash
# Create SOCKS proxy on local port 1080
ssh -D 1080 user@remote

# Use with: export https_proxy=socks5://localhost:1080
```

## Jump Host / Bastion

Connect to a server through a bastion host:

```ssh-config
# Bastion server
Host bastion
    User jump
    HostName jump.example.com
    IdentityFile ~/.ssh/bastion_key

# Internal server via bastion
Host internal
    User admin
    HostName 10.0.0.50
    ProxyCommand ssh -W %h:%p bastion
    IdentityFile ~/.ssh/internal_key
```

## Useful SSH Commands

```bash
# List loaded keys
ssh-add -l

# Add key to agent
ssh-add ~/.ssh/id_ed25519

# Debug connection
ssh -vvv user@hostname

# Run command on remote without interactive shell
ssh user@hostname "command here"

# Copy file to remote
scp localfile user@hostname:/remote/path/

# Recursive copy
scp -r localdir/ user@hostname:/remote/path/

# Sync directory (rsync over SSH)
rsync -avz --progress localdir/ user@hostname:/remote/path/
```
