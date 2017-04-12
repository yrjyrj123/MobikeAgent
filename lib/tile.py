from haversine import haversine


class Tile:
    def __init__(self, lon_min, lon_max, lat_min, lat_max):
        self.lon_min = lon_min
        self.lon_max = lon_max
        self.lat_min = lat_min
        self.lat_max = lat_max

    def next_level(self):
        lon_middle, lat_middle = self.center()
        return [Tile(self.lon_min, lon_middle, self.lat_min, lat_middle),
                Tile(lon_middle, self.lon_max, self.lat_min, lat_middle),
                Tile(self.lon_min, lon_middle, lat_middle, self.lat_max),
                Tile(lon_middle, self.lon_max, lat_middle, self.lat_max)]

    def covered_by_circle(self, radius):
        return True if radius > 0.7 * self.max_side() else False

    def max_side(self):  # unit: m
        return max(haversine((self.lon_min, self.lat_min), (self.lon_min, self.lat_max)),
                   haversine((self.lon_min, self.lat_min), (self.lon_max, self.lat_min)),
                   haversine((self.lon_min, self.lat_max), (self.lon_max, self.lat_max))) * 1000

    def center(self):
        lon_middle = (self.lon_min + self.lon_max) / 2
        lat_middle = (self.lat_min + self.lat_max) / 2
        return lon_middle, lat_middle

    def __str__(self):
        return "(%.6f - %.6f , %.6f - %.6f) %f" % (self.lon_min, self.lon_max, self.lat_min, self.lat_max, self.max_side())
