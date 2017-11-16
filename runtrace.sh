#!/bin/bash

tmux new-session -d 'python profiler.py'
tmux split-window -h 'python waver2.py'
tmux split-window -h 'python waver1.py'
tmux split-window -v 'python waver1.py'
tmux select-pane -L
tmux select-pane -L
tmux set status-style "bg=black"
tmux -2 attach-session -d
