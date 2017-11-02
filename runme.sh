#!/bin/bash

tmux new-session -d './fakinect.py'
tmux split-window -h './display.py'
tmux split-window -v 'htop -d 2'
tmux split-window -v 'top'
tmux select-pane -L
tmux split-window -v '~/Documents/OpenNI/OSCeleton/osceleton -a 192.168.1.132 -p 57120'
tmux resize-pane -D 15
tmux select-pane -R
tmux select-pane -U
tmux -2 attach-session -d
