#!/bin/bash

tmux new-session -d '/users/deniskolokol/Documents/OpenNI/OSCeleton/osceleton -a 192.168.1.132 -p 57120 | ./listener.py'
tmux split-window -h './display.py'
tmux split-window -v 'htop -d 2'
tmux split-window -v 'top'
tmux -2 attach-session -d
