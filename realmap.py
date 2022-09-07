import argparse
import math
import os
import numpy as np
import matplotlib.pyplot as plt
import geopandas
import rasterio
import rasterio.plot

import obj

ROAD_WIDTH = 7.0

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--roads', type=str, default=None)
parser.add_argument('--buildings', type=str, default=None)
parser.add_argument('--elevation', type=str, default=None)
parser.add_argument('--zmin', type=int, default=0)
args = parser.parse_args()

# for now (temporarily), both arguments are required
if args.elevation is None or args.roads is None:
    raise NotImplementedError

# Check if file exist
if args.roads is not None and os.path.exists(args.roads):
    print(f'{"ROADS":12} :', args.roads)
elif args.roads is not None:
    raise FileNotFoundError
if args.elevation is not None and os.path.exists(args.elevation):
    print(f'{"ELEVATION":12} :', args.elevation)
elif args.elevation is not None:
    raise FileNotFoundError

# Read arguments
z_min = args.zmin

# Read data
roads = geopandas.read_file(args.roads)
elevation = rasterio.open(args.elevation)
x_min, y_min, x_max, y_max = elevation.bounds

if str(roads.crs).upper() != str(elevation.crs).upper():
    raise NotImplementedError

buildings = None
if args.buildings is not None:
    buildings = geopandas.read_file(args.buildings)
    if str(roads.crs).upper() != str(buildings.crs).upper():
        raise NotImplementedError

# Track
print("generating track")
track = obj.WavefrontOBJ()

for index, poi in roads.iterrows():
    road_coords = roads.loc[index, 'geometry'].coords
    for c in range(len(road_coords) - 1):
        # current point
        x1, y1, z1 = road_coords[c]
        x1, y1, z1 = x1 - x_min, y1 - y_min, z1 - z_min
        # next point
        x2, y2, z2 = road_coords[c + 1]
        x2, y2, z2 = x2 - x_min, y2 - y_min, z2 - z_min
        # direction
        x_dir, y_dir, z_dir = x2 - x1, y2 - y1, z2 - z1
        # normalized orthogonal vector to direction
        orthogonal = y_dir, -x_dir
        orthogonal /= np.linalg.norm(orthogonal)
        # track width
        orthogonal *= 5

        v0 = track.add_vertex(x1 - orthogonal[0], z1, y1 - orthogonal[1])
        v1 = track.add_vertex(x1 + orthogonal[0], z1, y1 + orthogonal[1])
        v2 = track.add_vertex(x2 + orthogonal[0], z2, y2 + orthogonal[1])
        v3 = track.add_vertex(x2 - orthogonal[0], z2, y2 - orthogonal[1])
        track.add_face(v3, v2, v1, v0)

track.write('track.obj')

# Terrain
print("generating terrain")
terrain = obj.WavefrontOBJ()

elevation_data = elevation.read(1)
y_shape, x_shape = elevation_data.shape
area = x_shape * y_shape
increment = int(math.sqrt(area) // 128)

for x in range(0, x_shape - increment, increment):
    for y in range(0, y_shape - increment, increment):
        vertex = elevation.xy(y, x)
        v0 = terrain.add_vertex(vertex[0] - x_min, max(0, elevation_data[y, x] - z_min), vertex[1] - y_min)
        vertex = elevation.xy(y, x+increment)
        v1 = terrain.add_vertex(vertex[0] - x_min, max(0, elevation_data[y, x+increment] - z_min), vertex[1] - y_min)
        vertex = elevation.xy(y+increment, x+increment)
        v2 = terrain.add_vertex(vertex[0] - x_min, max(0, elevation_data[y+increment, x+increment] - z_min), vertex[1] - y_min)
        vertex = elevation.xy(y+increment, x)
        v3 = terrain.add_vertex(vertex[0] - x_min, max(0, elevation_data[y+increment, x] - z_min), vertex[1] - y_min)
        terrain.add_face(v0, v1, v2, v3)

terrain.write('terrain.obj')

if buildings is None:
    exit(0)

# Props
print("generating props")
props = obj.WavefrontOBJ()

for index, poi in buildings.iterrows():
    building_coords = buildings.loc[index, 'geometry'].exterior.coords
    for c in range(1, len(building_coords) - 1):
        # previous point
        x0, y0, z0 = building_coords[c - 1]
        x0, y0, z0 = x0 - x_min, y0 - y_min, z0 - z_min
        # current point
        x1, y1, z1 = building_coords[c]
        x1, y1, z1 = x1 - x_min, y1 - y_min, z1 - z_min
        # next point
        x2, y2, z2 = building_coords[c + 1]
        x2, y2, z2 = x2 - x_min, y2 - y_min, z2 - z_min

        v0 = props.add_vertex(x1, z1 - 2, y1)
        v1 = props.add_vertex(x2, z1 - 2, y2)
        v2 = props.add_vertex(x2, z2 + 6, y2)
        v3 = props.add_vertex(x1, z2 + 6, y1)
        props.add_face(v3, v2, v1, v0)

        v0 = props.add_vertex(x1, z1 - 2, y1)
        v1 = props.add_vertex(x0, z1 - 2, y0)
        v2 = props.add_vertex(x0, z0 + 6, y0)
        v3 = props.add_vertex(x1, z0 + 6, y1)
        props.add_face(v3, v2, v1, v0)

props.write('props.obj')

exit(0)