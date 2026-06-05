# Zsh Configuration Reference

Complete Zsh terminal configuration including Oh My Zsh setup, plugins, custom functions, and the ~/.myzshrc template.

## Oh My Zsh Installation

Install Oh My Zsh (choose one method):

```bash
# Method 1: curl
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Method 2: wget
wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh && sh install.sh
```

## Plugins

### zsh-autosuggestions

Provides command suggestions based on history:

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

### zsh-syntax-highlighting

Real-time syntax highlighting for typed commands:

```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

### Configure plugins in ~/.zshrc

```bash
plugins=(git z zsh-autosuggestions zsh-syntax-highlighting)
```

## Powerlevel10k Theme (Recommended)

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

Set theme in ~/.zshrc:

```bash
ZSH_THEME="powerlevel10k/powerlevel10k"
```

Run the interactive configuration wizard:

```bash
p10k configure
```

## ~/.myzshrc Template

Create `~/.myzshrc` with the following content. This file should be sourced from `~/.zshrc` (see section below).

```bash
# ============================================
# ~/.myzshrc - Custom Zsh Configuration
# ============================================

# --- Proxy Functions ---

function proxy_off() {
    unset http_proxy
    unset https_proxy
    echo -e "已关闭代理"
}

function proxy_on() {
    export no_proxy="localhost,127.0.0.1,localaddress,.localdomain.com"
    export http_proxy="http://127.0.0.1:7890"
    export https_proxy=$http_proxy
    echo -e "已开启代理"
}

# --- Encoding ---

set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936
set termencoding=utf-8
set encoding=utf-8

# --- Aliases ---

## tmux
alias t='tmux'
alias ta='tmux attach -t '

## General
alias zsh='source ~/.zshrc'
alias gt='git'

## k8s
alias k8s='kubectl'
alias kubectx='change_kube_config'

change_kube_config() {
    para=$1
    cp ~/.kube/config_$para ~/.kube/config
}

## Bazel
alias blb='bazel build -c opt'
alias blt='bazel test -c opt --test_output=errors --keep_going'
alias blr='bazel run -c opt'

# --- Git Clone Function ---
# Usage: gclf github.com/org/repo
# Clones into $GOPATH/src/github.com/org/repo

alias gclf='clone_f'

clone_f() {
    para=$1
    prefix=${para%/*}
    url=${prefix%/*}
    group=${prefix##*/}
    echo "prefix:${prefix},url:${url}"

    repo=${GOPATH}/src/${prefix}
    cd ${repo}

    file=${para##*/}
    echo "file:$file"

    mkdir -p ${repo}
    cd ${repo}

    gitUrl=git@${url}:${group}/${file}.git
    dest=${GOPATH}/src/${url}/${group}/${file}

    echo "clone:${gitUrl}, into:${dest}"
    git clone ${gitUrl} ${dest}
}

# --- GitHub Download Function ---
# Usage: git_download github.com/org/repo <commit_hash>
# Downloads source tarball via HTTP

alias gdld='git_download'

git_download() {
    para=$1
    commit=$2

    prefix=${para%/*}
    url=${prefix%/*}
    group=${prefix##*/}
    echo "prefix:${prefix},url:${url}"

    repo=${GOPATH}/src/${prefix}
    cd ${repo}

    file=${para##*/}
    echo "file:$file"

    dest=${GOPATH}/src/${url}/${group}
    mkdir -p $dest
    cd $dest

    wget "https://github.com/${group}/${file}/archive/${commit}.tar.gz"
    tar -xzvf *.tar.gz
    rm *.tar.gz
    mv ${file}-${commit} ${file}
}

# --- Protobuf Generate Function ---
# Usage: pcf git.llsapp.com/common/protos path/to/proto/package
# Generates pb.go with protoc and moves to _go_proto subdirectory

alias pcf='protoc_pb_generate'

protoc_pb_generate() {
    echo "repo subdir..."

    repo=$1
    cd ${GOPATH}/src/$1

    para=$2
    prefix=${para%/*}
    echo "prefix:$prefix"

    file=${para##*/}
    echo "file:$file"

    temp_dir=${file}_go_proto
    target=${GOPATH}/src/${repo}/${prefix}/${temp_dir}

    mkdir $target

    protoc --go_out=plugins=grpc:. -I . ${prefix}/${file}.proto

    mv ${GOPATH}/src/${repo}/${prefix}/${file}.pb.go ${target}

    cd -
}
```

## ~/.zshrc Source Order

In `~/.zshrc`, add the source line **before** `source $ZSH/oh-my-zsh.sh`:

```bash
# Add custom config BEFORE oh-my-zsh
source ~/.myzshrc

# Source oh-my-zsh
source $ZSH/oh-my-zsh.sh
```

## Additional Zsh Configuration

Add these to `~/.zshrc` or `~/.zshprofile` as needed:

```bash
# Homebrew (Apple Silicon)
if [ -f /opt/homebrew/bin/brew ]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# nvm (Node.js version manager)
export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"

# pyenv (Python version manager)
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

# zoxide (smarter cd)
eval "$(zoxide init zsh)"

# fzf (fuzzy finder)
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
```

## Proxy Usage

The proxy_on/proxy_off functions in ~/.myzshrc enable quick proxy toggling. Default proxy port is 7890 (common for Clash):

```bash
# Enable proxy
proxy_on

# Disable proxy
proxy_off
```

If your proxy uses a different port, edit the `proxy_on()` function in ~/.myzshrc accordingly.
