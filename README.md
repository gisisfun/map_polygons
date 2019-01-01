# Map Polygons for Data Visualisation (Hexagons and Boxes)
![alt text](https://raw.githubusercontent.com/gisisfun/map_polygons/master/SA1_need_for_assistance_2011.png)
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

## Data Processing Files for area weighted output
Polygon shapes are given attributes from data sets with spatial references. The polygon data is processed using scripts with their SQL and vrt file pointing to file names.  
For this example, spatial and tabular attribute data have been selected. The content is ABS SA1 2011 and 2016 shapefiles with associated demographic data items. The data was sourced from the the Australian Bureau of Statistics (ABS).

The hexagon or box shapes are created by the polygons.py python program. The features can be points, lines, polygons with or with attributes to be aggrregated into the hexagon or box shapes.

Run these ETL scripts in this order:

### Table Summary of processing files and components for area weighted output

| Process               | Path        | File              | VRT File           | SQL File           |
| --------------------- |:-----------:| -----------------:|-------------------:|-------------------:|
| Create hexagons/boxes | python      | polygons.py       |                    |
| Filter to Coastline   | batch_files | aust_shape.sh     | aust_shape.vrt     | aust_shape.sql     |
| Feature cut to shape  | batch_files | feat_aust_11.sh   | feat_aust_11.vrt   | feat_aust_11.sql   |
|                       |             | feat_aust_16.sh   | feat_aust_16.vrt   | feat_aust_16.sql   |
| Attrib Data to shape  | batch_files | donor_feat_11.sh  | donor_feat_11.vrt  | donor_feat_11.sql  |
|                       |             | donor_feat_16.sh  | donor_feat_16.vrt  | donor_feat_16.sql  |
| Agg data to shape     | batch_files | shape_donor_11.sh | shape_donor_11.vrt | shape_donor_11.sql |
|                       |             | shape_sonor_16.sh | shape_donor_16.vrt | shape_donor_16.sql |
| Merge attrib data     | batch_files | shape_11_16.sh    | shape_11_16.vrt    | shape_11_16.sql    |

The SQL code has been written to render the final product and a descriptive presentation of the process.

### Table of area weighted processing files and their input and output files

| File             | Input                            | Output                           |
| ----------------:|---------------------------------:|---------------------------------:|
| polygons.py      | hex_57km_layer.json              | hex_57km_layer.shp               |
| aust_shape.sh    | hex_57km_layer.shp               | aust_hex_shape_57km.shp          |
|                  | AUS_2016_AUST.shp                |                                  |
| feat_aust_11.sh  | aust_hex_shape_57km.shp          | feat_aust_57km_sa1_11.shp        | 
|                  | SA1_2011_AUST.shp                |                                  | 
| feat_aust_16.sh  | aust_hex_shape_57km.shp          | feat_aust_57km_sa1_11.shp        |
|                  | SA1_2016_AUST.shp                |                                  |
| donor_feat_11.sh | feat_aust_57km_sa1_11.shp        | donor_feat_57km_aust_11.shp      |
|                  | 2011Census_B18_AUST_SA1_long.csv |                                  |
| donor_feat_16.sh | feat_aust_57km_sa1_16.shp        | donor_feat_57km_aust_16.shp      |
|                  | 2016Census_G18_AUS_SA1.shp       |                                  |
| shape_donor_11.sh| donor_feat_57km_aust_11.shp      |shape_donor_feat_57km_aust_11.shp |
|                  | aust_hex_shape_57km.shp          |                                  |
| shape_sonor_16.sh| donor_feat_57km_aust_16.shp      |shape_donor_feat_57km_aust_16.shp |
|                  | aust_hex_shape_57km.shp          |                                  |
| shape_11_16.sh   |shape_donor_feat_57km_aust_11.shp | shape_75km_11_16.shp             |
|                  |shape_donor_feat_57km_aust_16.shp |                                  |

### Table of feature data set counts and file sizes for area weighted output

| File                              | Feature count  | File size |
| ---------------------------------:|---------------:|----------:|
| hex_57km_layer.json               | 4,051          | 2.4 MB    |
| hex_57km_layer.shp                | 4,051          | 627 KB    |
| AUS_2016_AUST.shp                 | 1              | 26.6 MB   |
| aust_hex_shape_57km.shp           | 1,262          | 627 KB    |
| SA1_2011_AUST.shp                 | 54,806         | 174 MB    |
| feat_aust_57km_sa1_11.shp         | 59,986         | 170 MB    |
| SA1_2016_AUST.shp                 | 57,523         | 185.5 MB  |
| feat_aust_57km_sa1_16.shp         | 62,756         | 186.6 MB  |
| 2011Census_B18_AUST_SA1_long.csv  | 54,806         | 19M       |
| donor_feat_57km_sa1_11.shp        | 20,017         | 15.2 MB   |
| 2016Census_G18_AUS_SA1.csv        | 57,523         | 20M       |
| donor_feat_57km_sa1_16.shp        | 18,923         | 14.1 MB   |
| shape_donor_feat_57km_aust_11.shp | 1,262          | 315 KB    |
| shape_donor_feat_57km_aust_16.shp | 1,262          | 303 KB    |
| shape_75km_11_16.shp              | 1,262          | 377 KB    |

### Table of data sources

| File                              | Download      | Feature count  | File size |
| ---------------------------------:|--------------:|---------------:|----------:|
| AUS_2016_AUST.shp                 |[download link](http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_aus_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&5503B37F8055BFFECA2581640014462C&0&July%202016&24.07.2017&Latest)| 1              |           |
| SA1_2011_AUST.shp                 |[download link](http://www.abs.gov.au/ausstats/subscriber.nsf/log?openagent&1270055001_sa1_2011_aust_shape.zip&1270.0.55.001&Data%20Cubes&24A18E7B88E716BDCA257801000D0AF1&0&July%202011&23.12.2010&Latest)| 54,806         | 174 MB    |
| SA1_2016_AUST.shp                 |[download link](http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa1_2016_aust_tab.zip&1270.0.55.001&Data%20Cubes&39A556A0197D8C02CA257FED00140567&0&July%202016&12.07.2016&Latest)| 57,523         | 185.5 MB  |
| 2011Census_B18_AUST_SA1_long.csv  |[download link](https://datapacks.censusdata.abs.gov.au/datapacks/)| 54,806         | 19M       |
| 2016Census_G18_AUS_SA1.csv        |[download link](https://datapacks.censusdata.abs.gov.au/datapacks/)| 57,523         | 20M       |
