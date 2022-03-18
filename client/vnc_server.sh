#!/bin/bash

#For some reason this command exits even with -forever. So run it in an infinite loop :shrug:
trap "exit 0" SIGINT SIGTERM
while true
do
    x11vnc -create -env FD_PROG="/usr/bin/chromium-browser --no-sandbox --disable-gpu --no-first-run --disable-sync --disable-dev-shm-usage $FLEDGE_FLAGS $ARAPI_FLAGS" -bg -forever -shared -passwd nextroll
done
