# RealMap3D

Create video game map as 3D object using real geographic data from open data sources.

**What was it made for ?**  
This project has a direct use for me for creating maps on
[Art of Rally](https://artofrally.com/).

This is a work in progress, you may have to make changes in the code to make it
work for you.

### TODO
* better road generation
  * use alti elevation instead of Z coordinate of the Shapefile
  * non flat road
* better fit between terrain and track
  * use points for elevation map
  * more points around track

*need improvement*
* better vegetation generation
* better fit between terrain and track
* building generation
  * use less polygon
* better interconnection between each section of road
* code refactoring to make it more readable

### Older versions
You might be interested in older versions, less complex or even more stable.
* [RealMap3D 1.0 (a1a0958419b69c5be5983db6398b5afa362e05d8)](https://github.com/Cyril-Meyer/RealMap3D/tree/a1a0958419b69c5be5983db6398b5afa362e05d8)

### How to use RealMap3D

#### 1. Prepare the data

Download the data for the area you want to process
(see [open data sources](#open-data-sources)).
* altitude / elevation map (GeoTIFF)
* roads map (Shapefile of lines)
* buildings map (Shapefile of polygons)
* vegetation map (Shapefile of polygons)

The altitude map must cover all the area of the infrastructure maps.

Using a geographic information system (like [QGis](https://www.qgis.org/)):
* remove the unwanted data from the infrastructure maps
* cut the altitude map to the infrastructure area (raster > extraction)
* use drape to assign the Z value for each point of the infrastructure maps
* For the vegetation
  * convert vegetation map into points (generate random points in polygons)
  * remove "on road" trees (select by distance)

#### 2. Convert the data to 3D object using RealMap3D

Example minimal
```
python realmap.py --elevation alti.tif --roads roads.shp --zmin 10
```
Example with more options
```
python realmap.py
--elevation data/TEST_03/ALTI.tif
--roads data/TEST_03/ROADS.shp
--buildings data/TEST_03/BUILDINGS.shp
--buildings-attr-height HAUTEUR
--vegetation data/TEST_03/VEGETATION_POINTS.shp
--zmin 220
--terrain-res 64
--terrain-flip-normals 1
--invert-x 1
```

### Open data sources

* [IGN](https://geoservices.ign.fr/)
  * [BD TOPO®](https://geoservices.ign.fr/bdtopo) (vector description of infrastructure)
  * [RGE ALTI®](https://geoservices.ign.fr/rgealti) (high resolution altitude map)  
  * [BD ALTI®](https://geoservices.ign.fr/bdalti) (medium resolution altitude map)

### FAQ

* The faces of the object are in the wrong direction
  * You may check the flip_normals() function

### Acknowledgment

If you like this project, you may be interested in one of the following:
* [RealMap](https://github.com/Yt-trium/RealMap)
* [ArtOfRallyTK](https://github.com/Cyril-Meyer/ArtOfRallyTK)
* [ArtOfRallyFFFMap](https://github.com/Cyril-Meyer/ArtOfRallyFFFMap)
* [ArtOfRallyCATransmission](https://github.com/Cyril-Meyer/ArtOfRallyCATransmission)
