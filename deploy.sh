#!/bin/bash

command=$1
pid=`ps -U $USER -o pid,cmd | sed -nr 's/([0-9]+) python api.py/\1/p'"`

if [ -n "${pid}" && ("$command" -eq "restart" || "$command" -eq "kill") ]; then
    kill -TERM `pid`
fi

if [ "$command" -eq "restart" || "$command" -eq "start" ]; then
    nohup python api.py > /dev/null &
fi
