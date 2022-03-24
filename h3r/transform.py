from typing import List

import numpy as np
from h3 import h3

from .geopoint import GeoLatLng, GeoXYZ, get_closest_face_center
from .rotation import rotation3D_x, rotation3D_z, rotation_axis_angle


class hexagon:
    def __init__(self):
        self.R_h3_to_amap = np.eye(3)
        self.R_amap_to_h3 = self.R_h3_to_amap.T

    def remapping_by_latlng_and_azimuth(self, lat: float, lng: float, azimuth: float):
        """remapping h3 indexing system by chosing face centroid and azimuth
        """
        centroid = GeoLatLng(lat, lng, using_rad=False)

        self.__reset_by_centroid_and_azimuth(centroid, azimuth)

    def amap_latlng_to_hex(self, lat: float, lng: float, resolution: int) -> str:
        """return the corresponding hex index for specified amap point
        """
        g = GeoLatLng(lat, lng, using_rad=False)
        return self.__amapGeo_to_hex(g, resolution)

    def hex_center(self, hex_id: str) -> GeoLatLng:
        """return the center point for specified hex index
        """
        h3_array = h3.h3_to_geo(hex_id)
        h3_geo = GeoLatLng(h3_array[0], h3_array[1], using_rad=False)
        return self.__h3Geo_to_amapGeo(h3_geo)

    def hex_boundary(self, hex_id: str) -> List[List[float]]:
        """return non duplicate boundary points for specified hex index
        """
        amap_boundary = self.__hex_boundary(hex_id)
        boundary_lnglat = [g.toList() for g in amap_boundary]
        return boundary_lnglat

    def hex_polygon(self, hex_id: str) -> List[List[float]]:
        """return polygon points for specified hex index, first and last points are the same.
        """
        amap_boundary = self.__hex_boundary(hex_id)
        boundary_lnglat = [g.toList() for g in amap_boundary]
        boundary_lnglat.append(boundary_lnglat[0])
        return boundary_lnglat

    def k_ring_distances(self, hex_id: str, ring_size: int) -> set:
        """return indices for all hexagons within the range of `ring_size` hexagon from hex_id, hexagons are grouped by the distance.
        """
        return h3.k_ring_distances(hex_id, ring_size)

    def k_ring(self, hex_id: str, ring_size: int) -> set:
        """return indices for all hexagons within the range of `ring_size` hexagon from hex_id
        """
        return h3.k_ring(hex_id, ring_size)

    def hex_distance(self, src_hex_id: str, dst_hex_id: str) -> int:
        """return distance from two hexagons, which are of the same resolution.
        """
        return h3.h3_distance(src_hex_id, dst_hex_id)

    def polyfill(self, geo_json, res, geo_json_conformant=False):
        """Get hexagons for a given GeoJSON region

        :param geo_json dict: A GeoJSON dictionary
        :param res int: The hexagon resolution to use (0-15)
        :param geo_json_conformant bool: Determines (lat, lng) vs (lng, lat)
            ordering Default is false, which is (lat, lng) ordering, violating
            the spec http://geojson.org/geojson-spec.html#id2 which is (lng, lat)

        :returns: Set of hex addresses

        eg:

        >>>  geo = {'coordinates': [[[40, 100], [35, 120], [30, 100], [40, 100]]],
                'type': 'Polygon'}
        >>>  polyfill(geo, 1)
        {'8164fffffffffff'}

        """
        new_geo = {"type": "Polygon"}
        coordinates = [[]]
        for p in geo_json["coordinates"][0]:
            lat, lng = p
            if geo_json_conformant:
                lng, lat = p
            g = GeoLatLng(lat, lng, using_rad=False)
            h3_geo = self.__amapGeo_to_h3Geo(g)
            new_lat = h3_geo.lat
            new_lng = h3_geo.lng
            if geo_json_conformant:
                coordinates[0].append([new_lng, new_lat])
            else:
                coordinates[0].append([new_lat, new_lng])
        new_geo["coordinates"] = coordinates

        return h3.polyfill(new_geo, res, geo_json_conformant)

    # def polyfill(self, geojson: str, resolution: int) -> set:
    #     return h3.polyfill(geojson, resolution)

    def __reset_h3_to_amap_rotation(self, R: np.array):
        if not np.isclose(np.linalg.det(R), 1) or not np.isclose(np.linalg.det(R @ R.T), 1):
            raise ValueError("parameter is not a rotation array")
        self.R_h3_to_amap = R
        self.R_amap_to_h3 = R.T

    def __reset_by_centroid_and_azimuth(self, centroid: GeoLatLng, azimuth: float):
        closest_face_center = get_closest_face_center(centroid)

        x_angle = centroid.lat_rad - closest_face_center.lat_rad
        z_angle = centroid.lng_rad - closest_face_center.lng_rad

        R = rotation_axis_angle(centroid, azimuth) @ rotation3D_z(z_angle) @ rotation3D_x(x_angle)

        self.__reset_h3_to_amap_rotation(R)

    def __h3Geo_to_amapGeo(self, g: GeoLatLng) -> GeoLatLng:
        h3_xyz = g.toXYZ()
        amap_xyz = self.R_h3_to_amap @ h3_xyz
        amap_GeoXYZ = GeoXYZ(amap_xyz[0], amap_xyz[1], amap_xyz[2])
        return amap_GeoXYZ.toGeoLatLng()

    def __amapGeo_to_h3Geo(self, g: GeoLatLng) -> GeoLatLng:
        amap_xyz = g.toXYZ()
        h3_xyz = self.R_amap_to_h3 @ amap_xyz
        h3_GeoXYZ = GeoXYZ(h3_xyz[0], h3_xyz[1], h3_xyz[2])
        return h3_GeoXYZ.toGeoLatLng()

    def __amapGeo_to_hex(self, g: GeoLatLng, resolution: int) -> str:
        h3_geo = self.__amapGeo_to_h3Geo(g)
        return h3.geo_to_h3(h3_geo.lat, h3_geo.lng, resolution)

    def __hex_boundary(self, hex_id: str) -> List[GeoLatLng]:
        h3_boundary = h3.h3_to_geo_boundary(hex_id)
        amap_boundary = []
        for lat, lng in h3_boundary:
            h3_geo = GeoLatLng(lat, lng, using_rad=False)
            amap_geo = self.__h3Geo_to_amapGeo(h3_geo)
            amap_boundary.append(amap_geo)
        return amap_boundary
