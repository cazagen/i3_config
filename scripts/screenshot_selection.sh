#!/bin/bash

FILENAME=$(date +"%Y-%m-%d_%H:%M:%S")

URL="https://i.cazagen.me/"$FILENAME.png
FILENAME=$HOME/Pictures/$FILENAME.png

scrot -s $FILENAME

scp -i /home/cazagen/.ssh/id_nopass $FILENAME do:/home/cazagen/img

echo $URL | xclip -selection c
