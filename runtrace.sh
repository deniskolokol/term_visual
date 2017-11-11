#!/bin/bash

tmux new-session -d './profiler.py'
tmux split-window -h './waver2.py'
tmux split-window -h './waver1.py'
tmux split-window -v './waver1.py'
tmux select-pane -L
tmux select-pane -L
tmux set status-style "bg=black"
tmux -2 attach-session -d
