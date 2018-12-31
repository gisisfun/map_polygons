Polygon shapes are given attributes from data sets with spatial references. The polygon data is processed using scripts with their SQL and vrt file pointing to file names.  
For this example, spatial and tabular attribute data have been selected. The content is ABS SA1 2011 and 2016 shapefiles with associated demographic data items. The data was sourced from the the Australian Bureau of Statistics (ABS).
Run these ETL scripts in this order:

| Process               | Path          | File              |
| --------------------- |:-------------:| -----------------:|
| Create hexagons/boxes | python        | polygons.py       |
| Filter to Coastline   | batch_files   | aust_shape.sh     |
| Feature cut to shape  | batch_files   | feat_aust_11.sh   |
|                       |               | feat_aust_16.sh   |
| Attrib Data to shape  | batch_files   | donor_feat_11.sh  |
|                       |               | donor_feat_16.sh  |
| Agg data to shape     | batch_files   | shape_donor_11.sh |
|                       |               | shape_sonor_16.sh |
| Merge attrib data     | batch_files   | shape_11_16.sh    |

The SQL code has been written to pruduce the final product and a descriptive presentation of the process.
![alt text](https://raw.githubusercontent.com/gisisfun/map_polygons/master/batch_files/processes.png "Logo Title Text 1")

