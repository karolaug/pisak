#!/bin/bash
xset -dpms
xset s off
xset s noblank

while :
do
    cd ~/pisak/brain_flippers/bomba
    python3 app.py
done
