#!/bin/bash

tmux new-session -d -s foo ./counter.py 10.0.11.3
tmux rename-window "Exploit: $1"

tmux select-window -t foo:0

own_ip=10.0.17.3

for ip in 10.0.{12..23}.3;
do
	if [ ${ip} != ${own_ip} ] 
	then tmux split-window -p 100 ./${1} ${ip}
	fi
done

tmux select-layout tiled

tmux -2 attach-session -t foo
