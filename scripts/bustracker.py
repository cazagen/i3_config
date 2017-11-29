# -*- coding: utf-8 -*-

import hashlib
import time
import sys
import requests

from configparser import ConfigParser

from pprint import pprint

parser = ConfigParser()
parser.read('/home/cazagen/.config/i3/scripts/config.ini')


class Py3status:
    def bustracker(self):
        
        MBT_API_KEY = parser.get('BusTracker', 'api_key')
        ENABLED = True
        
        TPL = "{bus_n}:{time}"
        BUSES = {
            "3": {
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
        
            # return response['busTimes'][0]['timeDatas'][0]['minutes']
            return BUSES
        
        
        def pick_colour(time):
            if time < 8:
                return "FF0000"
            elif time < 12:
                return "FF8500"
        
            return "8CC4FF"
        
        if ENABLED:
            get_times()
        
        output = [
            TPL.format(bus_n=k, time=v['next']) for k, v in BUSES.items() if v['next'] < 120
        ]
        
        #print(" ".join(output))
        
        #output = ""

        #for k, v in BUSES.items():
        #    output += "{}:{} ".format(k, v['next'])


        return {'full_text': " ".join(map(str, output)), 'cached_until': self.py3.time_in(seconds=30)}

