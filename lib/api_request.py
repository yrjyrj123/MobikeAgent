from gevent import monkey

monkey.patch_all()

import requests
import json
import os
import random
import time

API_URL = "https://api.mobike.com/mobike-api/rent/nearbyBikesInfo.do"
PROXY_FILE_PATH = "good_proxies.txt"
MAX_REQUEST_RETRY = 5
MAX_PROXY_RETRY = 5
TYPE_MAP = {1: "classical",
            2: "lite",
            999: "red_packet"}

proxy_map = {}
if os.path.exists(PROXY_FILE_PATH):
    f = open(PROXY_FILE_PATH)
    for line in f:
        line = line.strip()
        if len(line) > 0:
            proxy_map[line] = 0


def _get_proxy():
    if len(proxy_map.keys())==0:
        return None
    proxy = random.choice(proxy_map.keys())
    if proxy_map[proxy] > MAX_PROXY_RETRY:
        return None
    return proxy


def get_bike(tile):
    retry_count = 0
    results = None
    while retry_count < MAX_REQUEST_RETRY:
        proxy = _get_proxy()
        proxies = None
        if proxy is not None:
            proxies = {"https": "http://" + proxy}
        try:
            r = requests.post(API_URL,
                              "longitude=%.6f&latitude=%.6f" % tile.center(),
                              headers={
                                  'User-Agent': None,
                                  'Content-Type': 'application/x-www-form-urlencoded',
                                  'Accept-Encoding': 'gzip'
                              },
                              proxies=proxies, timeout=5)
        except:
            if proxy is not None:
                proxy_map[proxy] += 1
            retry_count += 1
            continue

        if r.status_code == 200:
            json_text = r.text
            json_obj = json.loads(json_text)
            results = []
            if 'object' in json_obj:
                obj = json_obj['object']
                for bike in obj:
                    bike_type = TYPE_MAP[bike['biketype']] if bike['biketype'] in TYPE_MAP else str(bike['biketype'])
                    results.append({'bikeid': bike['distId'],
                                    'biketype': bike_type,
                                    'lon': bike['distX'],
                                    'lat': bike['distY'],
                                    'distance':float(bike['distance'])})
            break
        else:
            retry_count += 1
            continue
    return results
