#!/usr/bin/env python
import re
import os

os.system("xrandr --output VIRTUAL1 --off --output eDP1 --primary --mode 1366x768 --pos 0x0 --rotate normal --output DP1 --off --output DP2-1 --off --output DP2-2 --off --output DP2-3 --off --output HDMI2 --off --output HDMI1 --off --output DP2 --off")

response = os.popen('lsusb').read()
regex = re.compile('(lenovo)+', re.IGNORECASE)
print(regex.findall(response))
new_response = regex.findall(response)

if len(new_response) > 0:
    os.system("xrandr --output VIRTUAL1 --off --output eDP1 --primary --mode 1366x768 --pos 0x282 --rotate normal --output DP1 --off --output DP2-1 --off --output DP2-2 --off --output DP2-3 --mode 1680x1050 --pos 1366x0 --rotate normal --output HDMI2 --off --output HDMI1 --off --output DP2 --off")
