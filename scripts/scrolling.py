#!/usr/bin/env python
import re
import os

response = os.popen('xinput list | grep "touchpad" --ignore-case').read()
regex = re.compile('id=(?P<line>\d+)', re.IGNORECASE)
touchpad_id = regex.findall(response)[0]


scrolling_response = os.popen("xinput list-props {} | grep -v 'default' --ignore-case | grep 'libinput Natural Scrolling Enabled' --ignore-case ".format(touchpad_id)).read()
regex2 = re.compile('\(([^)]+)\)', re.IGNORECASE)
scrolling_prop_ids = regex2.findall(scrolling_response)

print(touchpad_id)
print(scrolling_prop_ids)

for prop in scrolling_prop_ids:
    os.system("xinput set-prop {} {} 1".format(touchpad_id, prop))