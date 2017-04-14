#!coding=utf-8
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool

import random
import sys
from tqdm import tqdm
import time

import lib.api_request
from lib.tile import Tile
from lib.kml import KML
from lib.coordTransform import gcj02_to_wgs84

t = None

MAX_SEARCH_DISTANCE = 2000
MAX_RESULT_COUNT = 30
MIN_TILE_SIDE = 50
INIT_STEP = 0.02


def _frange(x, y, step):
    while x < y:
        yield x
        x += step


def _generate_task(lon_min, lon_max, lat_min, lat_max, step):
    tiles = []
    for lat in _frange(lat_min, lat_max, step):
        for lon in _frange(lon_min, lon_max, step):
            tiles.append(Tile(lon, lon + step, lat, lat + step))
    random.shuffle(tiles)
    return tiles


def _get_max_distance(bikes):
    max_distance = -1
    for bike in bikes:
        max_distance = max(max_distance, bike["distance"])
    return MAX_SEARCH_DISTANCE if max_distance == -1 else max_distance


def _get_bike(tile):
    temp = lib.api_request.get_bike(tile)
    t.update(1)
    return temp


def _after_processing(dic):
    bikes = []
    for k in dic.keys():
        del dic[k]['distance']
        bikes.append(dic[k])
    return bikes


def _scan_bikes(lon_min, lon_max, lat_min, lat_max):
    global t
    pool = Pool(64)
    temp_dic = dict()
    epoch = 1
    tasks = _generate_task(lon_min, lon_max, lat_min, lat_max, INIT_STEP)
    while len(tasks) > 0:
        temp_task = []
        t = tqdm(total=len(tasks), desc="Epoch %d" % epoch)
        map_results = pool.map(_get_bike, tasks)
        task_result_pairs = zip(tasks, map_results)
        for tile, map_result in task_result_pairs:
            if map_result is not None:
                for item in map_result:
                    temp_dic[item['bikeid']] = item
                max_dis = _get_max_distance(map_result)
                if (not tile.covered_by_circle(max_dis)) and tile.max_side() > MIN_TILE_SIDE:
                    temp_task += tile.next_level()
            else:
                temp_task.append(tile)
        random.shuffle(temp_task)
        tasks = temp_task
        t.close()
        epoch += 1
    bikes = _after_processing(temp_dic)
    return bikes


def _output_csv(bikes, csv_path):
    f = open(csv_path, "w")
    f.write(",".join(["bikeid", "biketype", "lon", "lat"]) + "\n")
    for bike in bikes:
        f.write(",".join([bike['bikeid'], bike["biketype"], str(bike['lon']), str(bike['lat'])]) + "\n")
    f.close()


def _output_kml(bikes, kml_path):
    k = KML()
    for bike in bikes:
        k.add_bike(bike)
    f = open(kml_path, "w")
    f.write(k.get_kml())
    f.close()


def _output_stdout(bikes):
    sys.stdout.write(",".join(["bikeid", "biketype", "lon", "lat"]) + "\n")
    for bike in bikes:
        sys.stdout.write(",".join([bike['bikeid'], bike["biketype"], str(bike['lon']), str(bike['lat'])]) + "\n")


def get_bikes_in_range(lon_min, lon_max, lat_min, lat_max, kml_path=None, csv_path=None):
    bikes = _scan_bikes(lon_min, lon_max, lat_min, lat_max)
    for bike in bikes:
        lon, lat = gcj02_to_wgs84(bike['lon'], bike['lat'])
        bike['lon'] = lon
        bike['lat'] = lat
    time.sleep(1)
    print """
    -----------------------
    Total find %d bike(s)
    -----------------------
    """ % len(bikes)
    if csv_path is not None:
        _output_csv(bikes, csv_path)

    if csv_path is None and kml_path is None:
        _output_stdout(bikes)

    if kml_path is not None:
        _output_kml(bikes, kml_path)


if __name__ == "__main__":
    # get_bikes_in_range(116.4, 116.41, 39.9, 39.91, kml_path="test.kml", csv_path="test.csv")  # 测试用的小范围
    get_bikes_in_range(116, 116.8, 39.6, 40.3, kml_path="beijing.kml", csv_path="beijing.csv")  # 北京六环以内的区域,可以涵盖95%以上的车
    # get_bikes_in_range(115.7, 117.4, 39.4, 41.6,kml_path="beijing_all.kml")  #地理书上的整个北京辖区,大约是六环内的7倍面积
    # get_bikes_in_range(120.85,122.2,30.6,31.9,kml_path="shanghai.kml")  #上海范围
