Polygon shapes are given attributes from data sets with spatial references. The polygon data is processed using scripts with their SQL and vrt file pointing to file names.  
For this example, spatial and tabular attribute data have been selected. The content is ABS SA1 2011 and 2016 shapefiles with associated demographic data items. The data was sourced from the the Australian Bureau of Statistics (ABS).
Run these ETL scripts in this order:
- 1 python/polygons.py
- 2 batch_files/aust_shape.sh
- 3 batch_files/feat_aust.sh

- 4 batch_files/donor_feat.sh
- 5 batch_files/shape_aust.sh
The SQL code has been written to pruduce the final product and a descriptive presentation of the process.
![alt text](https://raw.githubusercontent.com/gisisfun/map_polygons/master/batch_files/processes.png "Logo Title Text 1")

