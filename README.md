# map_polygons
This program is designed to demonstrate what is possible to achieve with a polyhedral, equal area mapping frameworks. 
The Python program creates a custom mapping layer in geojson format. 
The mapping layer can be made up of boxes or hexagons.

default options are:
- shape - hex or box: hex
- bounding north: -8
- bounding south: -45
- bounding east: 168
- bounding west: 96
- radius in km: 46
- filename for output: hex_46km

command line arguments are: 
- shape - hex or box 
- bounding north
- bounding south
- bounding east
- bounding west
- radius in km
- filename for output

for hexagon:
python3 polygons.py hex -8 -45 96 168 212

for boxes:
python3 polygons.py box -8 -45 96 168 212
