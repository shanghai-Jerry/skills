# China Mirror Sources Reference

Mirror source configurations for faster downloads in mainland China. Add to corresponding config files as needed.

## Homebrew

### Tsinghua University Mirror (Recommended)

Add to `~/.zshrc` or `~/.zshprofile`:

```bash
# Homebrew Tsinghua Mirror
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"
export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"
export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
```

### USTC Mirror (Alternative)

```bash
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.ustc.edu.cn/brew.git"
export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.ustc.edu.cn/homebrew-core.git"
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.ustc.edu.cn/homebrew-bottles"
```

### Existing Homebrew Fix

If Homebrew is already installed, update the remote:

```bash
# Update brew.git remote
git -C $(brew --repo) remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git

# Update homebrew-core.git remote
git -C $(brew --repo homebrew/core) remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git

# Update homebrew-cask.git remote
git -C $(brew --repo homebrew/cask) remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-cask.git
```

## npm

### Taobao Mirror (npmmirror)

```bash
npm config set registry https://registry.npmmirror.com
```

### Verify

```bash
npm config get registry
# Should output: https://registry.npmmirror.com/
```

### yarn

```bash
yarn config set registry https://registry.npmmirror.com
```

### pnpm

```bash
pnpm config set registry https://registry.npmmirror.com
```

## pip

### Tsinghua Mirror

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn
```

### Aliyun Mirror (Alternative)

```bash
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip config set global.trusted-host mirrors.aliyun.com
```

### Per-project Configuration

Create `pip.conf` in project root or `~/.pip/pip.conf`:

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
```

## Go

### GOPROXY

```bash
# Official China proxy (recommended by Go team)
go env -w GOPROXY=https://goproxy.cn,direct

# Aliyun proxy
go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct

# Multiple proxies with fallback
go env -w GOPROXY=https://goproxy.cn,https://mirrors.aliyun.com/goproxy/,direct
```

### Verify

```bash
go env GOPROXY
```

## Docker

### Registry Mirrors

Edit or create `~/.docker/daemon.json`：

```json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.xuanyuan.me"
  ]
}
```

Then restart Docker：

```bash
# Docker Desktop：点击菜单栏 Docker 图标 → Restart

# Or via command line（OrbStack / Colima 等基于 Lima 的运行时）：
# OrbStack
orbctl restart

# Colima
colima stop && colima start
```

> **Tip**：如果 `~/.docker/daemon.json` 已存在，只修改 `registry-mirrors` 字段即可，保留其他配置。验证镜像是否生效：
> ```bash
> docker info | grep -A 5 "Registry Mirrors"
> ```

## Ruby

### RubyChina Mirror

```bash
# Remove default source
gem sources --remove https://rubygems.org/

# Add RubyChina mirror
gem sources --add https://gems.ruby-china.com/

# Verify
gem sources -l
```

## Maven (Java)

### Aliyun Mirror

Edit `~/.m2/settings.xml`:

```xml
<mirrors>
    <mirror>
        <id>aliyunmaven</id>
        <mirrorOf>*</mirrorOf>
        <name>Aliyun Maven Mirror</name>
        <url>https://maven.aliyun.com/repository/public</url>
    </mirror>
</mirrors>
```

## Gradle (Java/Android)

### Aliyun Mirror

Edit or create `~/.gradle/init.gradle`:

```groovy
allprojects {
    repositories {
        maven { url 'https://maven.aliyun.com/repository/public' }
        maven { url 'https://maven.aliyun.com/repository/google' }
        maven { url 'https://maven.aliyun.com/repository/gradle-plugin' }
        maven { url 'https://maven.aliyun.com/repository/spring' }
        mavenCentral()
    }
}
```

## Homebrew Proxy Configuration

If you need to use a proxy for Homebrew instead of mirrors:

```bash
# Set proxy for Homebrew
export ALL_PROXY=socks5://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890

# Or configure in ~/.gitconfig (for git operations behind proxy)
[http]
    proxy = http://127.0.0.1:7890
[https]
    proxy = http://127.0.0.1:7890
```

## Quick Reference

| Tool | Mirror | Config Command |
|------|--------|---------------|
| Homebrew | Tsinghua | See HOMEBREW_ env vars |
| npm | Taobao | `npm config set registry https://registry.npmmirror.com` |
| pip | Tsinghua | `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple` |
| Go | goproxy.cn | `go env -w GOPROXY=https://goproxy.cn,direct` |
| Docker | 1ms.run/xuanyuan.me | Edit daemon.json |
| Ruby | RubyChina | `gem sources --add https://gems.ruby-china.com/` |
| Maven | Aliyun | Edit settings.xml |
| Gradle | Aliyun | Edit init.gradle |
