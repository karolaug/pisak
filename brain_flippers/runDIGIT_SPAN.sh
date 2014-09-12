#!/bin/bash
xset -dpms
xset s off
xset s noblank
export PYTHONPATH=~/pisak

while :
do
    cd ~/pisak/brain_flippers/digit_span
    python3 app.py
done
