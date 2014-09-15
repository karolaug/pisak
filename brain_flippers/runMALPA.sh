#!/bin/bash

xset s off
xset -dpms

export PYTHONPATH=~/pisak

while :
do
    cd ~/pisak/brain_flippers/malpa
    python3 app.py
done
