#!/usr/bin/env python
import re
import os

response = os.popen('lsusb').read()
regex = re.compile('(lenovo)+', re.IGNORECASE)
print(regex.findall(response))
new_response = regex.findall(response)

if len(new_response) > 0:
    os.system("sudo rfkill block wifi")
