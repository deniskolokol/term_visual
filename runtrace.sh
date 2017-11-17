#!/bin/bash

tmux new-session -d 'python profiler.py'
tmux resize-pane -L -15

tmux split-window -h 'top' # 'python switch.py --addres 192.168.1.132 --port 57120 --pin 18'

tmux split-window -h 'python switch.py --addres 192.168.1.132 --port 57120 --pin 18'
tmux select-pane -L

tmux split-window -v 'python waver2.py'
tmux split-window -h 'python waver1.py'
tmux split-window -v 'python waver1.py'

tmux select-pane -L
tmux select-pane -L
tmux split-window -v 'python display.py'
tmux resize-pane -D 15
tmux select-pane -L
tmux select-pane -L

tmux set status-style "bg=black"
tmux -2 attach-session -d


# tmux new-session -d 'python profiler.py'
# tmux split-window -h 'python waver2.py'
# tmux split-window -h 'python waver1.py'
# tmux split-window -v 'python waver1.py'
# tmux select-pane -L
# tmux select-pane -L
# tmux set status-style "bg=black"
# tmux -2 attach-session -d
