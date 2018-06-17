#!/bin/bash

# left panel: profiler (top)
tmux new-session -d 'python profiler.py'

# middle panel: running display (top)
tmux split-window -h 'python display.py'

# right panel: wavers
tmux split-window -h 'python waver2.py'
tmux split-window -v 'python waver1.py'
tmux split-window -v 'python waver1.py'

# middle panel: OSC module (bottom)
tmux select-pane -L
# eth0:
tmux split-window -v 'python switch.py --addres 192.168.1.132 --port 57120 --pin 18'
# wlan:
# tmux split-window -v 'python switch.py --addres 192.168.1.102 --port 57120 --pin 18'
tmux select-pane -U
tmux resize-pane -D 15
tmux resize-pane -R 15

# left panel: monitoring (bottom. but `top`)
tmux select-pane -L
tmux split-window -v 'top'
tmux resize-pane -D 15
tmux resize-pane -L 20
tmux select-pane -R

# cosmetics
tmux set pane-active-border-style "fg=black"
tmux set pane-border-style "fg=black"
tmux set status-style "bg=black"
tmux -2 attach-session -d

# in case osceleton is run from here:
# tmux split-window -v '~/Documents/OpenNI/OSCeleton/osceleton -a 192.168.1.132 -p 57120 -r'
