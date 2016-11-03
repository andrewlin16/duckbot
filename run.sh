#!/usr/bin/env bash

source env/bin/activate

until python3 app/duckbot.py "$@"; do
	echo "duckbot exited with code: $?" >&2
	sleep 1
done
