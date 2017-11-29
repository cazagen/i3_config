#!/usr/bin/env python
import re
import os

response = os.popen('xinput list | grep "touchpad" --ignore-case').read()
regex = re.compile('id=(?P<line>\d+)', re.IGNORECASE)
touchpad_id = regex.findall(response)[0]


tapping_response = os.popen("xinput list-props {} | grep -v 'default' --ignore-case | grep 'libinput Tapping Enabled' --ignore-case ".format(touchpad_id)).read()
regex2 = re.compile('\(([^)]+)\)', re.IGNORECASE)
tapping_prop_id = regex2.findall(tapping_response)

print(touchpad_id)
print(tapping_prop_id)

for prop in tapping_prop_id:
    os.system("xinput set-prop {} {} 1".format(touchpad_id, prop))