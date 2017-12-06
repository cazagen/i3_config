#!/bin/bash
scrot /tmp/i3lock.png
convert /tmp/i3lock.png -resize 25% /tmp/i3lock.png
convert /tmp/i3lock.png -blur 0x2 /tmp/i3lock.png
convert /tmp/i3lock.png -resize 400% /tmp/i3lock.png
i3lock -i /tmp/i3lock.png
