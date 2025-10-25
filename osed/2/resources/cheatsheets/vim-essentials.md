# Vim Essentials Cheat Sheet

## Quick Reference for OSED Section 2

---

## 🚀 Getting Started

### Launch & Exit
```bash
vim <file>                    # Open file
vim +<line> <file>            # Open at specific line
vim +/<pattern> <file>        # Open at pattern
vim -R <file>                 # Read-only mode
vim -M <file>                 # Modifiable mode

:q                             # Quit
:q!                            # Quit without saving
:w                             # Save
:wq                            # Save and quit
:x                             # Save and quit (same as :wq)
ZZ                             # Save and quit (normal mode)
ZQ                             # Quit without saving (normal mode)
```

### Help & Information
```vim
:help                          # Open help
:help <topic>                  # Help for specific topic
:version                       # Vim version
:set all                       # Show all settings
```

---

## 🎯 Modes

### Mode Switching
```
i                             # Insert mode (before cursor)
I                             # Insert mode (beginning of line)
a                             # Insert mode (after cursor)
A                             # Insert mode (end of line)
o                             # Insert mode (new line below)
O                             # Insert mode (new line above)
R                             # Replace mode
v                             # Visual mode (character)
V                             # Visual mode (line)
Ctrl+v                        # Visual mode (block)
Esc                           # Normal mode
```

---

## 🏃 Movement

### Basic Movement
```
h, j, k, l                    # Left, Down, Up, Right
w                             # Next word
W                             # Next WORD (space-separated)
b                             # Previous word
B                             # Previous WORD
e                             # End of word
E                             # End of WORD
0                             # Beginning of line
$                             # End of line
^                             # First non-blank character
```

### Line Movement
```
gg                            # First line
G                             # Last line
<number>G                      # Go to line number
:<number>                      # Go to line number
+                             # Next line (first char)
-                             # Previous line (first char)
Enter                         # Next line (first char)
```

### Screen Movement
```
Ctrl+f                        # Page down
Ctrl+b                        # Page up
Ctrl+d                        # Half page down
Ctrl+u                        # Half page up
H                             # Top of screen
M                             # Middle of screen
L                             # Bottom of screen
zt                            # Current line to top
zz                            # Current line to middle
zb                            # Current line to bottom
```

### Search Movement
```
f<char>                       # Find next char on line
F<char>                       # Find previous char on line
t<char>                       # Find next char (before)
T<char>                       # Find previous char (before)
;                             # Repeat last f/F/t/T
,                             # Repeat last f/F/t/T (reverse)
```

---

## 🔍 Search & Replace

### Search
```
/<pattern>                    # Search forward
?<pattern>                    # Search backward
n                             # Next match
N                             # Previous match
*                             # Search word under cursor (forward)
#                             # Search word under cursor (backward)
```

### Replace
```
:s/old/new/                   # Replace first occurrence in line
:s/old/new/g                  # Replace all occurrences in line
:%s/old/new/g                 # Replace all occurrences in file
:%s/old/new/gc                # Replace with confirmation
:.,$s/old/new/g               # Replace from current line to end
```

---

## ✂️ Editing

### Delete
```
x                             # Delete character under cursor
X                             # Delete character before cursor
dd                            # Delete line
D                             # Delete to end of line
d<movement>                   # Delete to movement
dw                            # Delete word
d$                            # Delete to end of line
d0                            # Delete to beginning of line
```

### Copy & Paste
```
yy                            # Yank (copy) line
Y                             # Yank line
y<movement>                   # Yank to movement
yw                            # Yank word
y$                            # Yank to end of line
p                             # Paste after cursor
P                             # Paste before cursor
```

### Undo & Redo
```
u                             # Undo
Ctrl+r                       # Redo
U                             # Undo all changes in line
```

### Change
```
cc                            # Change line
C                             # Change to end of line
c<movement>                   # Change to movement
cw                            # Change word
c$                            # Change to end of line
```

---

## 📝 Insert & Replace

### Insert Commands
```
i                             # Insert before cursor
I                             # Insert at beginning of line
a                             # Insert after cursor
A                             # Insert at end of line
o                             # Insert new line below
O                             # Insert new line above
```

### Replace Commands
```
r<char>                       # Replace character
R                             # Replace mode
s                             # Substitute character
S                             # Substitute line
```

---

## 📋 Visual Mode

### Visual Selection
```
v                             # Character visual mode
V                             # Line visual mode
Ctrl+v                        # Block visual mode
```

### Visual Commands
```
d                             # Delete selection
y                             # Yank selection
c                             # Change selection
>                             # Indent right
<                             # Indent left
=                             # Auto-indent
```

---

## 🔧 Advanced Editing

### Macros
```
q<letter>                     # Start recording macro
q                             # Stop recording macro
@<letter>                     # Execute macro
@@                            # Repeat last macro
```

### Marks
```
m<letter>                     # Set mark
`<letter>                     # Go to mark
'<letter>                     # Go to mark (beginning of line)
``                            # Go to previous position
''                            # Go to previous position (beginning of line)
```

### Folding
```
zf<movement>                  # Create fold
zo                            # Open fold
zc                            # Close fold
za                            # Toggle fold
zR                            # Open all folds
zM                            # Close all folds
```

---

## ⚙️ Settings & Configuration

### Essential Settings
```
:set number                   # Show line numbers
:set nonumber                 # Hide line numbers
:set relativenumber           # Relative line numbers
:set autoindent               # Auto-indent
:set smartindent              # Smart indent
:set tabstop=4                # Tab width
:set shiftwidth=4             # Indent width
:set expandtab                # Use spaces for tabs
:set hlsearch                 # Highlight search
:nohlsearch                   # Clear search highlight
:set syntax=on                # Syntax highlighting
:set wrap                     # Wrap lines
:set nowrap                    # No wrap
```

### File Operations
```
:e <file>                     # Edit file
:e!                           # Reload current file
:r <file>                     # Read file into buffer
:w <file>                     # Save as file
:saveas <file>                # Save as file
:cd <dir>                     # Change directory
:pwd                          # Print working directory
```

---

## 🎬 Buffers & Windows

### Buffer Management
```
:ls                           # List buffers
:b<number>                    # Switch to buffer
:bn                           # Next buffer
:bp                           # Previous buffer
:bd                           # Delete buffer
:bd!                          # Force delete buffer
```

### Window Management
```
:split                        # Split horizontally
:vsplit                        # Split vertically
:new                          # New horizontal window
:vnew                         # New vertical window
Ctrl+w w                      # Switch windows
Ctrl+w h                      # Move to left window
Ctrl+w j                      # Move to down window
Ctrl+w k                      # Move to up window
Ctrl+w l                      # Move to right window
Ctrl+w q                      # Close window
Ctrl+w o                      # Close other windows
```

---

## 🔍 Advanced Search

### Search Patterns
```
^                             # Beginning of line
$                             # End of line
.                             # Any character
*                             # Zero or more
\+                            # One or more
\?                            # Zero or one
\{n,m\}                       # Between n and m occurrences
\[abc\]                       # Character class
\[^abc\]                      # Negated character class
```

### Search Options
```
:set ignorecase               # Case insensitive
:set smartcase                # Smart case
:set incsearch                # Incremental search
:set wrapscan                 # Wrap around
```

---

## 🎯 Practical Examples

### Common Tasks
```
# Find and replace
:%s/old/new/gc

# Delete empty lines
:g/^$/d

# Sort lines
:sort

# Remove trailing whitespace
:%s/\s\+$//

# Comment/uncomment lines
# Visual select lines, then:
:s/^/# /                      # Comment
:s/^# //                      # Uncomment
```

### File Navigation
```
# Open file at specific line
vim +25 file.txt

# Open file at pattern
vim +/function file.c

# Open multiple files
vim file1.txt file2.txt
:next                         # Next file
:prev                         # Previous file
```

---

## 🔑 Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Esc | Normal mode |
| i | Insert mode |
| v | Visual mode |
| : | Command mode |
| / | Search forward |
| ? | Search backward |
| n | Next search result |
| N | Previous search result |
| u | Undo |
| Ctrl+r | Redo |
| gg | Go to first line |
| G | Go to last line |
| :w | Save |
| :q | Quit |
| :wq | Save and quit |

---

## 💡 Pro Tips

1. **Use hjkl**: More efficient than arrow keys
2. **Combine commands**: d + movement deletes to destination
3. **Repeat commands**: Use . to repeat last command
4. **Visual feedback**: Use visual mode to see selections
5. **Marks**: Use marks to jump between locations
6. **Macros**: Record repetitive tasks
7. **Search**: Use * and # to search current word
8. **Undo**: u undoes, Ctrl+r redoes
9. **Line numbers**: :set number for navigation
10. **Syntax**: :syntax on for highlighting

---

## 🔧 Troubleshooting

### Common Issues
- **Stuck in insert mode**: Press Esc
- **Can't save**: Check file permissions
- **Search not working**: Check pattern syntax
- **Undo not working**: Use u, not Ctrl+z

### Getting Help
```
:help                          # General help
:help <command>                # Help for command
:help <topic>                  # Help for topic
:help user-manual              # User manual
```

---

## 📚 Additional Resources

- **Vim Tutor**: Run `vimtutor` command
- **Official Docs**: https://vimdoc.sourceforge.net/
- **Vim Tips**: https://vim.fandom.com/wiki/Vim_Tips_Wiki
- **Vim Cheat Sheet**: https://vim.rtorr.com/

---

**Version**: 1.0 | **Last Updated**: December 2024
**For**: OSED Section 2 - Text Editing and Code Analysis

*Print this cheat sheet for quick reference during labs!*
