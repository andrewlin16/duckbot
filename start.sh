#!/usr/bin/env bash

source env/bin/activate

while true; do
    python3 app/duckbot.py "$@"
	echo "duckbot will restart in 5 seconds, ctrl-c to stop"
	sleep 5
done
