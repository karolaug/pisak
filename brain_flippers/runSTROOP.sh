#!/bin/bash
xset -dpms
xset s off
xset s noblank
PYTHONPATH='~/pisak'

while :
do
    cd ~/pisak
    python3 brain_flippers/stroop/app.py
done
