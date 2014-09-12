#!/bin/bash
xset -dpms
xset s off
xset s noblank
PYTHONPATH=~/pisak

while :
do
    cd ~/pisak/brain_flippers/puzzle
    python3 app.py
done
