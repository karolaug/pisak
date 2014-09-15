#!/bin/bash

xset s off
xset -dpms

export PYTHONPATH=~/pisak

while :
do
    cd ~/pisak
    python3 brain_flippers/stroop/app.py
done
