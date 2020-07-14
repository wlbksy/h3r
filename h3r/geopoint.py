import numpy as np


class GeoLatLng:
    def __init__(self, lat, lng, using_rad=False):
        if using_rad:
            self.lat_rad = lat
            self.lng_rad = lng
            self.lat = np.rad2deg(lat)
            self.lng = np.rad2deg(lng)
        else:
            self.lat = lat
            self.lng = lng
            self.lat_rad = np.deg2rad(lat)
            self.lng_rad = np.deg2rad(lng)

    def toXYZ(self):
        r = np.cos(self.lat_rad)
        z = np.sin(self.lat_rad)
        x = np.cos(self.lng_rad) * r
        y = np.sin(self.lng_rad) * r
        return np.array([x, y, z])

    def toGeoXYZ(self):
        d = self.toXYZ()
        return GeoXYZ(d[0], d[1], d[2])

    def __repr__(self):
        return '[{}, {}]'.format(self.lng, self.lat)

    def toList(self):
        return [self.lng, self.lat]


class GeoXYZ:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def toGeoLatLng(self):
        lat_rad = np.arcsin(self.z)
        lng_rad = np.arctan2(self.y, self.x)
        return GeoLatLng(lat_rad, lng_rad, using_rad=True)
