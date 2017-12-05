# -*- coding: utf-8 -*-

#
#
#
# Add priority for show order
# Add ability to load in buses from config
#
#


import hashlib
import time
import requests

from configparser import ConfigParser

parser = ConfigParser()
parser.read('/home/cazagen/.config/i3/scripts/config.ini')


class Py3status:

    enabled = True

    def bustracker(self):
        MBT_API_KEY = parser.get('BusTracker', 'api_key')


        TPL = "{bus_n}:{time}"
        BUSES = {
            "3": {
                "stop_id": 64323494,
                "next": None
            },
            "33": {
                "stop_id": 64323494,
                "next": None
            },
            "N3": {
                "stop_id": 64323494,
                "next": None
            }
        }


        def get_new_api_key(api_key):
            new_api_key = api_key
            new_api_key = new_api_key + time.strftime("%Y%m%d%H")

            m = hashlib.md5()
            m.update(new_api_key.encode('utf-8'))

            return m.hexdigest()


        def get_times():
            endpoint = "http://ws.mybustracker.co.uk/?module=json"
            stop_ids = set([it['stop_id'] for it in BUSES.values()])

            params = {
                "key": get_new_api_key(MBT_API_KEY),
                "function": "getBusTimes",
            }

            for idx, stop_id in enumerate(stop_ids):
                param = "stopId{}".format(idx+1)
                params[param] = str(stop_id)

            response = requests.get(endpoint, params=params).json()

            for item in response['busTimes']:
                service = item['mnemoService']
                if service in BUSES and BUSES[service]['stop_id'] == int(item['stopId']):
                    BUSES[service]['next'] = int(item['timeDatas'][0]['minutes'])

            return BUSES

        get_times()

        output = [
            TPL.format(bus_n=k, time=v['next']) for k, v in BUSES.items() if v['next'] < 120 and v['next'] is not None
        ]

        if self.enabled:
            return {'full_text': " ".join(map(str, output)), 'cached_until': self.py3.time_in(seconds=30)}
        else:
            return {'full_text': "", 'cached_until': self.py3.time_in(seconds=30)}

    def on_click(self, event):
        self.enabled = not self.enabled
