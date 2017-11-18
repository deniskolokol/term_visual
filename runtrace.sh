#!/bin/bash

tmux new-session -d 'python profiler.py'

tmux split-window -h 'top'

# wlan
tmux split-window -h 'python switch.py --addres 192.168.1.102 --port 57120 --pin 18'
# eth0
# tmux split-window -h 'python switch.py --addres 192.168.1.132 --port 57120 --pin 18'
tmux select-pane -L

tmux split-window -v 'python waver2.py'
tmux split-window -h 'python waver1.py'
tmux split-window -v 'python waver1.py'

tmux select-pane -L
tmux select-pane -L
tmux split-window -v 'python display.py'
tmux resize-pane -D 15
tmux resize-pane -L 25

tmux select-pane -R
tmux resize-pane -U 20
tmux select-pane -L
tmux select-pane -U

tmux set pane-active-border-style "fg=black"
tmux set pane-border-style "fg=black"
tmux set status-style "bg=black"
tmux -2 attach-session -d
