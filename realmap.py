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
import vegetation as v

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--elevation', type=str, default=None)
parser.add_argument('--roads', type=str, default=None)
parser.add_argument('--buildings', type=str, default=None)
parser.add_argument('--buildings-attr-height', type=str, default=None)
parser.add_argument('--vegetation', type=str, default=None)
parser.add_argument('--terrain-res', type=int, default=128)
parser.add_argument('--terrain-flip-normals', type=int, default=0)
parser.add_argument('--zmin', type=int, default=0)
parser.add_argument('--invert-x', type=int, default=0)
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
terrain_res = args.terrain_res
terrain_flip_normals = bool(args.terrain_flip_normals)
invert_x = bool(args.invert_x)

# Read data
roads_gis = geopandas.read_file(args.roads)
elevation_gis = rasterio.open(args.elevation)
x_min, y_min, x_max, y_max = elevation_gis.bounds
p_min = np.array([x_min, y_min, z_min])

if invert_x:
    invert_x = x_max - x_min
else:
    invert_x = 0

if str(roads_gis.crs).upper() != str(elevation_gis.crs).upper():
    raise NotImplementedError

buildings_gis = None
if args.buildings is not None:
    buildings_gis = geopandas.read_file(args.buildings)
    if str(roads_gis.crs).upper() != str(buildings_gis.crs).upper():
        raise NotImplementedError

vegetation_gis = None
if args.vegetation is not None:
    vegetation_gis = geopandas.read_file(args.vegetation)
    if str(roads_gis.crs).upper() != str(vegetation_gis.crs).upper():
        raise NotImplementedError

track = obj.WavefrontOBJ(invert_x=invert_x)
terrain = obj.WavefrontOBJ(invert_x=invert_x)

# Track
print("generating track")
roads_object = r.Roads(p_min, track, terrain)
roads_object.add(roads_gis)
roads_object.export_track_connections('tracks_ends.obj', invert_x=invert_x)
track.write('track.obj')

# Terrain
print("generating terrain")
terrain_object = t.Terrain(p_min, terrain=terrain, resolution=terrain_res)
terrain_object.add(elevation_gis)
t.export(terrain, debug=bool(debug), flip_normals=terrain_flip_normals)

if buildings_gis is not None:
    # Buildings
    print("generating buildings")
    buildings = obj.WavefrontOBJ(invert_x=invert_x)
    buildings_roofs = obj.WavefrontOBJ(invert_x=invert_x)
    buildings_object = b.Buildings(p_min, buildings, buildings_roofs)
    buildings_object.add(buildings_gis, buildings_attr_height)
    buildings.write('buildings.obj')
    buildings_roofs.write('buildings_roofs.obj')

if vegetation_gis is not None:
    # Trees
    print("generating trees")
    tree_trunks = obj.WavefrontOBJ(invert_x=invert_x)
    tree_leaves = obj.WavefrontOBJ(invert_x=invert_x)
    trees_object = v.Tree(p_min, tree_trunks, tree_leaves)
    trees_object.add(vegetation_gis)
    tree_trunks.write('trees_trunks.obj')
    tree_leaves.write('trees_leaves.obj')

exit(0)
