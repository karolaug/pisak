#!/bin/bash
xset -dpms
xset s off
xset s noblank
export PYTHONPATH=~/pisak

while :
do
    cd ~/pisak/brain_flippers/malpa
    python3 app.py
done
