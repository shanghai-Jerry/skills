# Vim Configuration Reference

Complete Vim configuration template based on the CSDN article's ~/.vimrc setup, with indentation, folding, status bar, and color scheme.

## Setup

Copy the default Vim config and customize:

```bash
cp /etc/vim/vimrc ~/.vimrc
```

Then replace with the template below.

## Complete ~/.vimrc Template

```vim
" ============================================
" ~/.vimrc - Vim Configuration
" ============================================

" --- File Settings ---
setlocal noswapfile       " Don't generate swap files
set bufhidden=hide        " Hide buffer instead of abandoning when discarded
set nobackup              " Don't create backup files
set backupcopy=yes        " Overwrite original file when backing up
set autochdir             " Auto-switch directory to current file's directory

" --- Display ---
set number                " Show line numbers
set cursorline            " Highlight current line
set ruler                 " Show ruler in status bar
set cmdheight=1           " Command line height

" --- Indentation ---
set shiftwidth=4          " Indent width for << and >> commands
set softtabstop=4         " Backspace deletes 4 spaces at once
set tabstop=4             " Tab width = 4 spaces
set smartindent           " Smart auto-indent on new lines
set expandtab             " Use spaces instead of tabs

" --- Search ---
set hlsearch              " Highlight search results
set incsearch             " Incremental search (show results while typing)
set ignorecase            " Case-insensitive search
set smartcase             " Case-sensitive when search contains uppercase

" --- Folding ---
set foldenable            " Enable folding
set foldmethod=syntax     " Syntax-based folding
set foldcolumn=0          " No fold column
setlocal foldlevel=1      " Default fold level = 1

" Space bar toggles fold
nnoremap <space> @=((foldclosed(line('.')) < 0) ? 'zc' : 'zo')<CR>

" --- Interface ---
colorscheme evening       " Color scheme
set laststatus=2          " Always show status bar (1 = hide)
set statusline=\ %<%F[%1*%M%*%n%R%H]%=\ %y\ %0(%{&fileformat}\ %{&encoding}\ Ln\ %l,\ Col\ %c/%L%)

" --- Bells ---
set noerrorbells          " Disable error bell sound
set novisualbell          " Disable visual bell
set t_vb=                 " Clear terminal bell code

" --- Misc ---
set magic                 " Enable magic patterns for regex
set matchtime=2           " Time (in tenths of a second) to show matching bracket
set backspace=indent,eol,start  " Allow backspace over everything in insert mode
set encoding=utf-8        " UTF-8 encoding
set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936  " File encoding detection
```

## Key Configuration Explained

### Folding

Vim folding allows you to collapse code blocks (functions, classes, etc.):

- `za` — Toggle fold under cursor
- `zc` — Close fold
- `zo` — Open fold
- `zM` — Close all folds
- `zR` — Open all folds
- `Space` — Toggle fold (custom mapping from config above)

The `foldmethod=syntax` setting means folding follows language syntax (if/else blocks, functions, classes).

### Status Bar

The custom status line shows:
- File path and name
- Modified flag `[+]`
- Read-only flag `[RO]`
- File format (unix/dos)
- Encoding (utf-8)
- Current line/column position

### Color Scheme

`evening` is a built-in dark color scheme that works well in terminals. Other recommended schemes:
- `desert` — Warm dark theme
- `industry` — Blue-toned dark theme
- `slate` — Gray-toned theme

### Indentation

The 4-space configuration is standard for many languages. For Go development, you may want to use tabs instead:

```vim
" Go-specific: use tabs
autocmd FileType go setlocal noexpandtab tabstop=4 shiftwidth=4 softtabstop=4
```

## Plugin Recommendations (Optional)

For a more powerful Vim setup, consider these plugins:

```bash
# Install vim-plug (plugin manager)
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```

Add to ~/.vimrc:

```vim
call plug#begin('~/.vim/plugged')

" File navigation
Plug 'preservim/nerdtree'
Plug 'kien/ctrlp.vim'

" Code features
Plug 'preservim/nerdcommenter'   " Toggle comments
Plug 'tpope/vim-surround'        " Surround with brackets/quotes

" Git integration
Plug 'tpope/vim-fugitive'

" Appearance
Plug 'vim-airline/vim-airline'   " Status bar enhancement
Plug 'ryanoasis/vim-devicons'    " File type icons

call plug#end()
```

After adding plugins, run in Vim:

```vim
:PlugInstall
```
