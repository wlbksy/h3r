# usage

1. Choose a coordinate C (lat, lng) for your application in which C is the centroid of your area of interest.
2. Choose an angle (noted as z) by which the generated grids rotate around your selected corrdinate C. This angle could be selected through trials.
3. Apply rotation and begin your search.

# example

Suppose we have choosen C (lat, lng) and z, both in degree.
Your goal is to search for hexagon Id for target coordinate T (lat_target, lng_target) in resolution r

```python
import h3r
import numpy as np

h = h3r.hexagon()

C_lat = 32.1285602329
C_lng = 114.0831041336
z = 30

h.remapping_by_latlng_and_azimuth(C_lat, C_lng, np.deg2rad(z))

# search for "The Oriental Pearl Radio & TV Tower"
lat_target = 31.2398112159
lng_target = 121.4996910095
r = 8

hex_id = h.amap_latlng_to_hex(lat_target, lng_target, r)

# 8865188599fffff

hex_center_coordinate = h.hex_center(hex_id)

# [121.50208930490493, 31.23756012616091]

hex_boundary_points = h.hex_boundary(hex_id)

# 6 points for a hex

# [[121.50808483610177, 31.236618599882398],
#  [121.50604840128445, 31.241549774930185],
#  [121.5000524889904, 31.24249125542705],
#  [121.49609354705748, 31.238501391068542],
#  [121.49813051127545, 31.233570324196652],
#  [121.50412588807572, 31.23262901349188]]

hex_polygon_points = h.hex_polygon(hex_id)

# 7 points for a hex with the 7th equals the 1st.

# [[121.50808483610177, 31.236618599882398],
#  [121.50604840128445, 31.241549774930185],
#  [121.5000524889904, 31.24249125542705],
#  [121.49609354705748, 31.238501391068542],
#  [121.49813051127545, 31.233570324196652],
#  [121.50412588807572, 31.23262901349188],
#  [121.50808483610177, 31.236618599882398]]


hex_distance = 2

# return indices for all hexagons within the range of `ring_size` hexagon from hex_id
hex_set = h.k_ring(hex_id, 2)

# {'88651884a1fffff',
#  '88651884a5fffff',
#  '88651884a7fffff',
#  '88651884adfffff',
#  '8865188583fffff',
#  '886518858bfffff',
#  '8865188591fffff',
#  '8865188593fffff',
#  '8865188595fffff',
#  '8865188597fffff',
#  '8865188599fffff',
#  '886518859bfffff',
#  '886518859dfffff',
#  '88651885d1fffff',
#  '88651885d3fffff',
#  '88651885d5fffff',
#  '88651885d7fffff',
#  '88651885dbfffff',
#  '886518ba4dfffff'}

# return indices for all hexagons within the range of 2 hexagon from hex_id,
# hexagons are grouped by the distance.
hex_set_list = h.k_ring_distances(hex_id, hex_distance)

# [{'8865188599fffff'},
#  {'88651884a5fffff',
#   '8865188591fffff',
#   '886518859bfffff',
#   '886518859dfffff',
#   '88651885d3fffff',
#   '88651885d7fffff'},
#  {'88651884a1fffff',
#   '88651884a7fffff',
#   '88651884adfffff',
#   '8865188583fffff',
#   '886518858bfffff',
#   '8865188593fffff',
#   '8865188595fffff',
#   '8865188597fffff',
#   '88651885d1fffff',
#   '88651885d5fffff',
#   '88651885dbfffff',
#   '886518ba4dfffff'}]


# return distance from two hexagons, which are of the same resolution.
d = h.hex_distance('8865188599fffff', '88651884a5fffff')

# d = 1

geo = {'coordinates': [[[40, 100], [35, 120], [30, 100], [40, 100]]],
                'type': 'Polygon'}
h.polyfill(geo, 1)

# {'8164fffffffffff'}
```

hex_id is of type string and its content is a long int expressed in hex format.
