#!coding=utf-8

from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool


import requests
import json
import random
import time
import sys

from kml import KML

import logging


f=open("good_proxies.txt")
proxies=[]
for line in f:
    proxies.append(line[:-1])

def _frange(x, y, step):
  while x < y:
    yield x
    x += step


def _get_nearby_bikes_info((latitude,longitude)):
    while True:
        try:
            proxy=random.choice(proxies)
            r=requests.post("http://api.mobike.com/mobike-api/rent/nearbyBikesInfo.do",
                                    "latitude=%.6f&longitude=%.6f"%(latitude,longitude),
                                    headers={
                                            'User-Agent': 'Googlebot/2.1',
                                            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                            'Accept-Encoding': 'gzip'
                                            },
                                    proxies={"http": "http://"+proxy},timeout=5)
            if r.status_code>200:
                if proxy in proxies:
                    proxies.remove(proxy)
                continue
            json_text = r.text
            logging.debug(json_text)
            obj= json.loads(json_text)
            return obj
        except:
            pass


def _generate_task(lon_min,lon_max,lat_min,lat_max):
    task=[]
    for lat in _frange(lat_min,lat_max,0.012):
        for lon in _frange(lon_min,lon_max,0.015):
            task.append([lat,lon])
    random.shuffle(task)
    return task


def _process_task(task):
    dic = dict()
    pool = Pool(1024)
    map_results = pool.map(_get_nearby_bikes_info, task)
    for obj in map_results:
        if 'object' in obj:
            object = obj['object']
            for bike in object:
                dic[bike['distId']] = {'distId': bike['distId'],
                                       'distX': bike['distX'],
                                       'distY': bike['distY']}
    return dic.values()


def get_bikes_in_range(lon_min, lon_max, lat_min, lat_max, kml_path=None):

    task=_generate_task(lon_min,lon_max,lat_min,lat_max)
    logging.info("task count:%d"%len(task))

    start = time.time()

    bikes=_process_task(task)
    if kml_path != None:
        k = KML()
        for bike in bikes:
            k.add_bike((bike['distId'], bike['distX'], bike['distY']))
        f = open(kml_path, "w")
        f.write(k.get_kml())
        f.close()
    else:
        for bike in bikes:
            sys.stdout.write(str(bike['distId']) + "," + str(bike['distX']) + "," + str(bike['distY']) + "\n")
    logging.info("time: %fs"%(time.time()-start))


if __name__=="__main__":
    sys.stderr.write("start download\n")
    get_bikes_in_range(116, 116.8, 39.6, 40.3)  #北京六环以内的区域,3186块,可以涵盖95%以上的车
    #get_bikes_in_range(115.7, 117.4, 39.4, 41.6)  #地理书上的整个北京辖区,20976块,大约是六环内的7被面积
    sys.stderr.write("done")