#!/bin/bash

# remove possible leftover locks that would block opening new vnc sessions
find /tmp -name ".X*-lock" -exec rm -rf {} \;

Xvfb $DISPLAY -screen 0 1024x768x16 &
x11vnc -display $DISPLAY -N -bg -shared -forever -passwd nextroll

wait
