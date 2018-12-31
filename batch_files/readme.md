# Data Processing Files
Polygon shapes are given attributes from data sets with spatial references. The polygon data is processed using scripts with their SQL and vrt file pointing to file names.  
For this example, spatial and tabular attribute data have been selected. The content is ABS SA1 2011 and 2016 shapefiles with associated demographic data items. The data was sourced from the the Australian Bureau of Statistics (ABS).

The hexagon or box shapes are created by the polygons.py python program. The features can be points, lines, polygons with or with attributes to be aggrregated into the hexagon or box shapes.

Run these ETL scripts in this order:

### Table Summary of processing files and components

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

The SQL code has been written to pruduce the final product and a descriptive presentation of the process.

### Table of processing files and their input and output files

| File             | Input                            | Output                           |
| ----------------:|---------------------------------:|---------------------------------:|
| polygons.py      | hex_57km_layer.json              | hex_57km_layer.shp               |
| aust_shape.sh    | hex_57km_layer.shp               | aust_hex_shape_57km.shp          |
|                  | AUS_2016_AUST.shp                | a                                |
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

### Table of feature counts and File sizes

| File                              | Feature count  | File size |
| ---------------------------------:|---------------:|----------:|
| hex_57km_layer.json               | 4,051          | 2.4 MB    |
| hex_57km_layer.shp                | 4,051          | 627 KB    |
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



![alt text](https://raw.githubusercontent.com/gisisfun/map_polygons/master/batch_files/processes.png "Logo Title Text 1")

