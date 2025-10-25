# Tmux Essentials Cheat Sheet

## Quick Reference for OSED Section 2

---

## 🚀 Getting Started

### Launch & Exit
```bash
tmux                           # Start new session
tmux new -s <name>            # Start named session
tmux attach -t <name>         # Attach to session
tmux list-sessions            # List sessions
tmux kill-session -t <name>   # Kill session

exit                           # Exit session
Ctrl+b d                       # Detach from session
```

### Help & Information
```bash
tmux list-commands            # List all commands
tmux show-options             # Show options
tmux show-key-bindings        # Show key bindings
```

---

## 🎯 Sessions

### Session Management
```
Ctrl+b :new                   # New session
Ctrl+b :new-session -s <name> # New named session
Ctrl+b :kill-session           # Kill current session
Ctrl+b :list-sessions          # List sessions
Ctrl+b :attach-session -t <name> # Attach to session
Ctrl+b s                       # Choose session
Ctrl+b $                       # Rename session
```

### Session Commands
```bash
tmux new -s debug             # Create debug session
tmux attach -t debug          # Attach to debug session
tmux kill-session -t debug   # Kill debug session
tmux list-sessions            # List all sessions
```

---

## 🪟 Windows

### Window Management
```
Ctrl+b c                       # New window
Ctrl+b ,                       # Rename window
Ctrl+b n                       # Next window
Ctrl+b p                       # Previous window
Ctrl+b 0-9                     # Switch to window number
Ctrl+b w                       # Choose window
Ctrl+b &                       # Kill window
Ctrl+b f                       # Find window
```

### Window Commands
```
Ctrl+b :new-window             # New window
Ctrl+b :kill-window            # Kill current window
Ctrl+b :next-window            # Next window
Ctrl+b :previous-window         # Previous window
Ctrl+b :swap-window -t <num>   # Swap windows
```

---

## 📱 Panes

### Pane Management
```
Ctrl+b %                       # Split vertically
Ctrl+b "                       # Split horizontally
Ctrl+b x                       # Kill pane
Ctrl+b z                       # Toggle pane zoom
Ctrl+b {                       # Swap pane left
Ctrl+b }                       # Swap pane right
Ctrl+b o                       # Switch to next pane
Ctrl+b ;                       # Switch to last pane
Ctrl+b q                       # Show pane numbers
```

### Pane Resizing
```
Ctrl+b :resize-pane -U <num>   # Resize up
Ctrl+b :resize-pane -D <num>   # Resize down
Ctrl+b :resize-pane -L <num>   # Resize left
Ctrl+b :resize-pane -R <num>   # Resize right
Ctrl+b Ctrl+Up                 # Resize up
Ctrl+b Ctrl+Down               # Resize down
Ctrl+b Ctrl+Left               # Resize left
Ctrl+b Ctrl+Right              # Resize right
```

### Pane Movement
```
Ctrl+b Up                      # Move to pane above
Ctrl+b Down                    # Move to pane below
Ctrl+b Left                    # Move to pane left
Ctrl+b Right                   # Move to pane right
```

---

## 🎬 Copy Mode

### Enter Copy Mode
```
Ctrl+b [                       # Enter copy mode
```

### Navigation in Copy Mode
```
h, j, k, l                     # Move cursor
w, b                           # Word forward/backward
0, $                           # Beginning/end of line
g, G                           # Beginning/end of buffer
/pattern                       # Search forward
?pattern                       # Search backward
n, N                           # Next/previous match
```

### Selection & Copy
```
Space                          # Start selection
Enter                          # Copy selection
Ctrl+b ]                       # Paste
```

### Exit Copy Mode
```
Esc                            # Exit copy mode
q                              # Exit copy mode
```

---

## ⚙️ Configuration

### Configuration File
```bash
~/.tmux.conf                   # User config file
/etc/tmux.conf                 # System config file
```

### Essential Settings
```
# Set prefix key
set -g prefix C-b

# Enable mouse support
set -g mouse on

# Set default terminal
set -g default-terminal "screen-256color"

# Enable UTF-8
set -g utf8 on

# Set window/pane numbering
set -g base-index 1
setw -g pane-base-index 1

# Renumber windows when one is closed
set -g renumber-windows on

# Increase scrollback buffer
set -g history-limit 10000

# Enable focus events
set -g focus-events on

# Set window title
set -g set-titles on
set -g set-titles-string "#T"

# Set status bar
set -g status-bg black
set -g status-fg white
set -g status-left "[#S] "
set -g status-right " %Y-%m-%d %H:%M "
```

---

## 🎯 Status Bar

### Status Bar Configuration
```
set -g status-bg <color>       # Background color
set -g status-fg <color>       # Foreground color
set -g status-left "<string>"  # Left status
set -g status-right "<string>" # Right status
set -g status-interval <sec>   # Update interval
```

### Status Bar Variables
```
#S                             # Session name
#W                             # Window name
#T                             # Window title
#D                             # Date
#H                             # Hostname
#h                             # Hostname (short)
#I                             # Window index
#P                             # Pane index
```

---

## 🔧 Advanced Features

### Synchronized Panes
```
Ctrl+b :set synchronize-panes  # Toggle synchronized panes
Ctrl+b :set synchronize-panes on  # Enable synchronized panes
Ctrl+b :set synchronize-panes off # Disable synchronized panes
```

### Mouse Support
```
set -g mouse on                # Enable mouse
set -g mouse off               # Disable mouse
```

### Automatic Renumbering
```
set -g renumber-windows on     # Renumber windows
set -g renumber-windows off    # Don't renumber windows
```

---

## 🎬 Scripting & Automation

### Command Mode
```
Ctrl+b :                       # Enter command mode
Ctrl+b :help                    # Show help
Ctrl+b :list-keys               # List key bindings
Ctrl+b :list-commands           # List commands
```

### Send Keys
```
Ctrl+b :send-keys "command"     # Send keys to pane
Ctrl+b :send-keys -t <target> "command" # Send to specific target
```

### Capture Pane
```
Ctrl+b :capture-pane           # Capture current pane
Ctrl+b :save-buffer <file>     # Save buffer to file
Ctrl+b :delete-buffer          # Delete buffer
```

---

## 🎯 Practical Examples

### Development Setup
```bash
# Create development session
tmux new -s dev

# Split into multiple panes
Ctrl+b "                       # Split horizontally
Ctrl+b %                       # Split vertically

# Run different commands in each pane
# Pane 1: vim file.c
# Pane 2: gcc -g file.c
# Pane 3: gdb ./a.out
```

### Debugging Session
```bash
# Create debugging session
tmux new -s debug

# Setup panes for debugging
Ctrl+b "                       # Split horizontally
Ctrl+b %                       # Split vertically

# Pane 1: Source code (vim)
# Pane 2: Compilation (gcc)
# Pane 3: Debugger (gdb)
# Pane 4: Documentation (man pages)
```

### Multi-Server Management
```bash
# Create server management session
tmux new -s servers

# Split for different servers
Ctrl+b "                       # Split horizontally
Ctrl+b %                       # Split vertically

# Pane 1: SSH to server1
# Pane 2: SSH to server2
# Pane 3: Local monitoring
# Pane 4: Log analysis
```

---

## 🔑 Key Bindings

### Essential Keys
| Key | Action |
|-----|--------|
| Ctrl+b | Prefix key |
| Ctrl+b d | Detach session |
| Ctrl+b c | New window |
| Ctrl+b n | Next window |
| Ctrl+b p | Previous window |
| Ctrl+b % | Split vertically |
| Ctrl+b " | Split horizontally |
| Ctrl+b x | Kill pane |
| Ctrl+b z | Toggle zoom |
| Ctrl+b [ | Copy mode |
| Ctrl+b ] | Paste |
| Ctrl+b s | Choose session |
| Ctrl+b w | Choose window |

### Movement Keys
| Key | Action |
|-----|--------|
| Ctrl+b Up | Move to pane above |
| Ctrl+b Down | Move to pane below |
| Ctrl+b Left | Move to pane left |
| Ctrl+b Right | Move to pane right |
| Ctrl+b o | Switch to next pane |
| Ctrl+b ; | Switch to last pane |

---

## 💡 Pro Tips

1. **Use meaningful session names**: `tmux new -s debug`
2. **Enable mouse support**: `set -g mouse on`
3. **Use zoom for focus**: `Ctrl+b z`
4. **Synchronize panes**: `Ctrl+b :set synchronize-panes`
5. **Use copy mode**: `Ctrl+b [` for scrolling
6. **Save sessions**: Use session names for persistence
7. **Use window numbers**: `Ctrl+b 0-9`
8. **Resize panes**: `Ctrl+b Ctrl+Arrow`
9. **Use status bar**: Customize with session info
10. **Script automation**: Use `tmux` commands in scripts

---

## 🔧 Troubleshooting

### Common Issues
- **Can't detach**: Use `Ctrl+b d`
- **Lost session**: Use `tmux list-sessions`
- **Pane not responding**: Check if pane is active
- **Keys not working**: Check prefix key (Ctrl+b)

### Recovery
```bash
# List sessions
tmux list-sessions

# Attach to session
tmux attach -t <session-name>

# Kill unresponsive session
tmux kill-session -t <session-name>
```

---

## 📚 Additional Resources

- **Official Docs**: https://github.com/tmux/tmux/wiki
- **Tmux Manual**: `man tmux`
- **Tmux Cheat Sheet**: https://tmuxcheatsheet.com/
- **Tmux Configuration**: https://github.com/tmux/tmux/wiki/Getting-Started

---

**Version**: 1.0 | **Last Updated**: December 2024
**For**: OSED Section 2 - Terminal Multiplexing and Session Management

*Print this cheat sheet for quick reference during labs!*
