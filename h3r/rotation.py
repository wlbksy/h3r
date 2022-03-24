import numpy as np

from .geopoint import GeoLatLng


def skew(geolatlng: GeoLatLng) -> np.array:
    g = geolatlng.toGeoXYZ()
    return np.array([
        [0, -g.z, g.y],
        [g.z, 0, -g.x],
        [-g.y, g.x, 0]
    ])


def rotation_axis_angle(g: GeoLatLng, angle: float) -> np.array:
    K = skew(g)
    s = np.sin(angle)
    c = np.cos(angle)
    return np.eye(3) + s * K + (1-c) * K @ K


def rotation3D_x(angle: float) -> np.array:
    """Generate the SO(3) rotation matrix about the x axis.
    """
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([
        [1.0, 0.0, 0.0],
        [0.0, c, -s],
        [0.0, s, c]
    ])


def rotation3D_z(angle: float) -> np.array:
    """Generate the SO(3) rotation matrix about the z axis.
    """
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([
        [c, -s, 0.0],
        [s, c, 0.0],
        [0.0, 0.0, 1.0]
    ])
