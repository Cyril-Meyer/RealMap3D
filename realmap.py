import argparse
import math
import os
import numpy as np
import geopandas
import rasterio

import obj
import roads as r
import terrain as t
import buildings as b

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--roads', type=str, default=None)
parser.add_argument('--buildings', type=str, default=None)
parser.add_argument('--buildings-attr-height', type=str, default=None)
parser.add_argument('--elevation', type=str, default=None)
parser.add_argument('--zmin', type=int, default=0)
parser.add_argument('--debug', type=int, default=0)
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
buildings_attr_height = args.buildings_attr_height
z_min = args.zmin
debug = args.debug

# Read data
roads_gis = geopandas.read_file(args.roads)
elevation_gis = rasterio.open(args.elevation)
x_min, y_min, x_max, y_max = elevation_gis.bounds
p_min = np.array([x_min, y_min, z_min])

if str(roads_gis.crs).upper() != str(elevation_gis.crs).upper():
    raise NotImplementedError

buildings_gis = None
if args.buildings is not None:
    buildings_gis = geopandas.read_file(args.buildings)
    if str(roads_gis.crs).upper() != str(buildings_gis.crs).upper():
        raise NotImplementedError

track = obj.WavefrontOBJ()
terrain = obj.WavefrontOBJ()

# Track
print("generating track")
roads_object = r.Roads(p_min, track, terrain)
roads_object.add(roads_gis)
track.write('track.obj')

# Terrain
print("generating terrain")
terrain_object = t.Terrain(p_min, terrain)
terrain_object.add(elevation_gis)
t.export(terrain, debug=bool(debug), flip_normals=True)

if buildings_gis is None:
    exit(0)

# Props
print("generating props")
props_buildings = obj.WavefrontOBJ()
props_buildings_roofs = obj.WavefrontOBJ()
buildings_object = b.Buildings(p_min, props_buildings, props_buildings_roofs)
buildings_object.add(buildings_gis, buildings_attr_height)
props_buildings.write('props_buildings.obj')
props_buildings_roofs.write('props_buildings_roofs.obj')

exit(0)
