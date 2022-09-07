# RealMap3D

Create video game map as 3D object using real geographic data from open data sources.

### TODO
* interconnection between each section of road
  * maybe use delaunay triangulation in thoses area
* building generation
* vegetation generation

*need improvement*
* better fit between terrain and track
  * maybe create a hole under the road to avoid slow down

### How to use RealMap3D

#### 1. Prepare the data

Download the data for the area you want to process
(see [open data sources](#open-data-sources)).
* altitude / elevation map (GeoTIFF)
* roads map (Shapefile)
* buildings map (Shapefile)

The altitude map must cover all the area of the infrastructure maps.

Using a geographic information system (like [QGis](https://www.qgis.org/)):
* remove the unwanted data from the infrastructure maps
* cut the altitude map to the infrastructure area (raster > extraction)
* use drape to assign the Z value for each point of the infrastructure maps


#### 2. Convert the data to 3D object using RealMap3D

Example
```
python realmap.py --roads roads.shp --elevation alti.tif --buildings buildings.shp --zmin 10
```

### Open data sources

* [IGN](https://geoservices.ign.fr/)
  * [BD TOPO®](https://geoservices.ign.fr/bdtopo) (vector description of infrastructure)
  * [RGE ALTI®](https://geoservices.ign.fr/rgealti) (high resolution altitude map)  
  * [BD ALTI®](https://geoservices.ign.fr/bdalti) (medium resolution altitude map)

### Acknowledgment

If you like this project, you may be interested in
[RealMap](https://github.com/Yt-trium/RealMap)
