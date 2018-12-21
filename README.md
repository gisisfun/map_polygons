# map_polygons
![alt text](https://raw.githubusercontent.com/gisisfun/map_polygons/master/SA1 neefor assistance 2011.png)
This program is designed to demonstrate what is possible to achieve with a polyhedral, equal area mapping frameworks. 
The Python program creates a custom mapping layer in geojson format. 
The mapping layer can be made up of boxes or hexagons.

for a 46 km radial hexagon values are:
- shape: hex
- bounding north: -8
- bounding south: -45
- bounding east: 168
- bounding west: 96
- radial in km: 46
- filename for output: hex_46km

at the WGS-84 Projection values for default values are:
- 46 km from -8,96 offset is -7.999789221838243,96.41725883231395
- At latitude of -8 latitude, radial distance is 46 km 
- At latitude of -22.5 , radial distance is rounded to 43 km 
- At latitude of -45 , radial distance is rounded to 33 km 


command line arguments are: 
- shape - hex or box 
- bounding north
- bounding south
- bounding east
- bounding west
- radial in km
- filename for output

for hexagon:
python3 polygons.py hex -8 -45 96 168 212

for boxes:
python3 polygons.py box -8 -45 96 168 212
