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

class MyIter:
    def __init__(self, mylist):
        self.list = mylist
        self.pos = 0
    def __iter__(self):
        while True:
            yield self.list[self.pos]
            self.pos += 1
            if self.pos >= len(self.list):
                self.pos = 0


class Py3status:

    def __init__(self):
        self.enabled = True
        BUSES_LAB = {
            "3": {
                "stop_id": 36234798,
                "next": None
            },
            "33": {
                "stop_id": 36234798,
                "next": None
            },
            "N3": {
                "stop_id": 36234798,
                "next": None
            },
            "Place": {
                "stop_id": None,
                "next": None,
                "name" : "Hacklab",
                "logo" : ""
            }
        }

        BUSES_HOME = {
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
            },
            "Place": {
                "stop_id": None,
                "next": None,
                "name" : "Home",
                "logo" : ""
            }
        }
        
        self.bus_types = [BUSES_HOME, BUSES_LAB]
        self.bus_type = iter(MyIter(self.bus_types))
        self.BUSES = next(self.bus_type)



    def bustracker(self):
        MBT_API_KEY = parser.get('BusTracker', 'api_key')

        TPL = "{bus_n}:{time}"
        
        def get_new_api_key(api_key):
            new_api_key = api_key
            new_api_key = new_api_key + time.strftime("%Y%m%d%H")

            m = hashlib.md5()
            m.update(new_api_key.encode('utf-8'))

            return m.hexdigest()


        def get_times():
            endpoint = "http://ws.mybustracker.co.uk/?module=json"
            stop_ids = set([it['stop_id'] for it in self.BUSES.values() if it['stop_id'] is not None])

            params = {
                "key": get_new_api_key(MBT_API_KEY),
                "function": "getBusTimes",
            }

            for idx, stop_id in enumerate(stop_ids):
                param = "stopId{}".format(idx+1)
                params[param] = str(stop_id)

            response = requests.get(endpoint, params=params).json()

            if len(response) > 0:
                for item in response['busTimes']:
                    service = item['mnemoService']
                    if service in self.BUSES and self.BUSES[service]['stop_id'] == int(item['stopId']):
                        self.BUSES[service]['next'] = int(item['timeDatas'][0]['minutes'])

            return self.BUSES

        get_times()

        output = [
            TPL.format(bus_n=k, time=v['next']) for k, v in self.BUSES.items() if v['next'] < 120 and v['next'] is not None
        ]

        new_output = " ".join(map(str, output))
        new_output = self.BUSES["Place"]["logo"] + " " + new_output

        if self.enabled:
            return {'full_text': new_output, 'cached_until': self.py3.time_in(seconds=30)}
        else:
            return {'full_text': "", 'cached_until': self.py3.time_in(seconds=30)}

    def on_click(self, event):
        button = event['button']
        if button == 1:
            self.BUSES = next(self.bus_type)
            if self.enabled == False:
                self.enabled = True
        if button == 3:
            self.enabled = not self.enabled