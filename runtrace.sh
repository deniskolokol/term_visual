#!/bin/bash

tmux new-session -d './fakinect.py'
tmux split-window -h './display.py'
tmux split-window -v 'htop -d 2'
tmux split-window -v 'top'
tmux -2 attach-session -d
