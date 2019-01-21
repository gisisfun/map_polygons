# Map Polygons for Data Visualisation (Hexagons and Boxes)
*Knowledge is acquired long after the data is created.*
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

## Data Processing Files 
Polygon shapes are given attributes from data sets with spatial references. The polygon data is processed using scripts with their SQL and vrt file pointing to file names.  
For this example, spatial and tabular attribute data have been selected. The content is ABS SA1 2011 and 2016 shapefiles with associated demographic data items. The data was sourced from the the Australian Bureau of Statistics (ABS).

The hexagon or box shapes are created by the polygons.py python program. The features can be points, lines, polygons with or with attributes to be aggrregated into the hexagon or box shapes.

Run these ETL scripts in this order:

### Table Summary of processing files and components

| Process              | Process Type | Folder      | File |
|:-------------|:-------------|:-----------|:--------|
| **Create hexagons/ boxes**|              | python      | polygons.py |
| **Filter to coastline**  |Polygon Select| batch_files | aust_shape.sh |
| **Feature cut to shape** | area weight  | batch_files | feat_aust_11.sh |
|                      |              |             | feat_aust_16.sh |
| **Attrib Data to shape** | table join   | batch_files | donor_feat_11.sh |
|                      |              |             | donor_feat_16.sh  |
| **Agg data to shape**    | aggregation & table join| batch_files | shape_donor_11.sh |
|                      |    |             | shape_donor_16.sh |
| **Merge attrib data**    | table join   | batch_files | shape_11_16.sh    |
| **Make towns and cities**|point in polygon| batch_files| shape_place_count.sh|
| **Add towns and cities** | table join   | batch_files | shape_11_16_place.sh|
| **Make AGIL counts** |point in polygon| batch_files| shape_agil_count.sh|
| **Update with AGIL** | table join   | batch_files | shape_11_16_place_agil.sh|
| **Make services count** |point in polygon| batch_files| shape_service_count.sh|
| **Update with services** | table join   | batch_files | shape_11_16_place_agil.sh|
| **Make base station count** |point in polygon| batch_files| shape_bstation_count.sh|
| **Update with base stations** | table join   | batch_files | shape_11_16_place_agil_bstation.sh|
| **Make road links count** |line in polygon| batch_files| shape_road_count.sh|
| **Update with road links** | table join   | batch_files | shape_11_16_place_agil_bstation_road.sh|
| **Make mobile black spot count** |line in polygon| batch_files| shape_mbsp_count.sh|
| **Update with mobile black spots** | table join   | batch_files | shape_11_16_place_agil_bstation_road_mbsp.sh|

| File | VRT File | SQL File |
|:-------------|:----------|:-------|
| **polygons.py**       |                    |                    |
| **aust_shape.sh**     |aust_shape.vrt|aust_shape.sql |
| **feat_aust_11.sh**   |feat_aust_11.vrt|feat_aust_11.sql |
| **feat_aust_16.sh**   |feat_aust_16.vrt|feat_aust_16.sql |
| **donor_feat_11.sh**  |donor_feat_11.vrt|donor_feat_11.sql |
| **donor_feat_16.sh**  |donor_feat_16.vrt|donor_feat_16.sql |
| **shape_donor_11.sh** |shape_donor_11.vrt|shape_donor_11.sql |
| **shape_donor_16.sh** |shape_donor_16.vrt| shape_donor_16.sql|
| **shape_11_16.sh**    |shape_11_16.vrt|shape_11_16.sql|
| **shape_11_16_place.sh**|shape_11_16.vrt|shape_place_count.sql|
| **shape_11_16_place.sh**|shape_11_16.vrt|shape_11_16_place.sql|
| **shape_agil_count.sh**|shape_11_16.vrt|shape_agil_count.sql|
| **shape_11_16_place_agil.sh**|shape_11_16.vrt|shape_11_16_place_agil.sql |
| **shape_service_count.sh**|shape_11_16.vrt|shape_service_count.sql |
| **shape_11_16_place_agil.sh**|shape_11_16.vrt|shape_11_16_place_agil_services.sql |
| **shape_service_count.sh**|shape_11_16.vrt|shape_service_count.sql |
| **shape_11_16_place_agil.sh**|shape_11_16.vrt|shape_11_16_place_agil_services.sql|
| **shape_bstation_count.sh**|shape_11_16.vrt|shape_service_count.sql|
| **shape_11_16_place_agil_bstation.sh**|shape_11_16.vrt|shape_11_16_place_agil_services_ bstation.sql|
| **shape_road_count.sh**|shape_11_16.vrt|shape_road_count.sql|
| **shape_11_16_place_agil_bstation_road.sh**|shape_11_16.vrt|shape_11_16_place_agil_services_ bstation_road.sql|
| **shape_mbsp_count.sh**|shape_11_16.vrt|shape_mbsp_count.sql|
| **shape_11_16_place_agil_bstation_road_mbsp.sh**|shape_11_16.vrt|shape_11_16_place_agil_services_ bstation_road_mbsp.sql|

The SQL code has been written to render the final product and a descriptive presentation of the process.

### Table of processing files and their input and output files

| File             | Input                            | Output                           |
| :----------------|:---------------------------------|:---------------------------------|
| **polygons.py**      | hex_57km_layer.json              | hex_57km_layer.shp               |
| **aust_shape.sh**    | hex_57km_layer.shp               | aust_hex_shape_57km.shp          |
|                  | AUS_2016_AUST.shp                |                                  |
| **feat_aust_11.sh**  | aust_hex_shape_57km.shp          | feat_aust_57km_sa1_11.shp        | 
|                  | SA1_2011_AUST.shp                |                                  | 
| **feat_aust_16.sh**  | aust_hex_shape_57km.shp          | feat_aust_57km_sa1_11.shp        |
|                  | SA1_2016_AUST.shp                |                                  |
| **donor_feat_11.sh** | feat_aust_57km_sa1_11.shp        | donor_feat_57km_aust_11.shp      |
|                  | 2011Census_B18_AUST_SA1_long.csv |                                  |
| **donor_feat_16.sh** | feat_aust_57km_sa1_16.shp        | donor_feat_57km_aust_16.shp      |
|                  | 2016Census_G18_AUS_SA1.shp       |                                  |
| **shape_donor_11.sh**| donor_feat_57km_aust_11.shp      |shape_donor_feat_57km_aust_11.shp |
|                  | aust_hex_shape_57km.shp          |                                  |
| **shape_donor_16.sh**| donor_feat_57km_aust_16.shp      |shape_donor_feat_57km_aust_16.shp |
|                  | aust_hex_shape_57km.shp          |                                  |
| **shape_11_16.sh**   |shape_donor_feat_57km_aust_11.shp | shape_75km_11_16.shp             |
|                  |shape_donor_feat_57km_aust_16.shp |                                  |
|                  |aust_hex_shape_57km.shp |                                  |
| **shape_place_count.sh**   |aust_hex_shape_57km.shp  | shape_57km_place_count.shp |
| | gis_osm_places_free_1.shp | |
| **shape_11_16_place.sh**   |shape_57km_11_16.shp | shape_57km_11_16_place.shp             |
| |shape_75km_place_count.shp | |
| **shape_agil_count.sh**   |aust_hex_shape_57km.shp  | shape_57km_agil_count.shp             |
| | AGIL.json | |
| **shape_11_16_place_agil.sh**   |shape_57km_place_count.shp | shape_57km_11_16_place _agil.shp |
| |shape_57km_agil_count.shp | |
| **shape_service_count.sh** | aust_hex_shape_57km.shp  | shape_57km_service_count.shp |
| | gis_osm_places_free_1.shp ||
| **shape_11_16_place_agil_service.sh**   |shape_57km_service_count.shp | shape_57km_11_16_place _agil_service.shp             |
| |shape_57km_service_count.shp | |
| **shape_bstation_count.sh** | aust_hex_shape_57km.shp  |shape_57km_service_bstation.shp |
| | gis_osm_pois_free_1.shp ||
| **shape_11_16_place _agil_service_bstation.sh** |shape_57km_11_16_place _agil_service.shp | shape_57km_11_16_place _agil_service_bstation.shp |
| |shape_57km_bstation_count.shp | |
| **shape_road_count.sh** | aust_hex_shape_57km.shp  |shape_57km_road_count.shp |
| | gis_osm_roads_free_1.shp ||
| **shape_11_16_place_agil _service_bstation_road.sh** | shape_57km_11_16_place _agil_service_bstation.shp |shape_57km_11_16_place _agil_service_bstation_road.shp |
| |shape_57km_road_count.shp | |
| **shape_mbsp_count.sh** | aust_hex_shape_57km.shp  |shape_57km_mbsp_count.shp |
| | mbsp_database.csv ||
| **shape_11_16_place_agil _service_bstation_road_mbsp.sh** | shape_57km_11_16_place _agil_service_bstation_road.shp |shape_57km_11_16_place _agil_service_bstation_road_mbsp.shp |
| |shape_57km_mbsp_count.shp | |

### Table of feature data set counts and file sizes 

| File                              | Feature count  | File size | Projection (EPSG) |
| :---------------------------------|---------------:|----------:|:-----------------|
| **hex_57km_layer.json**               | 4,051          | 2.4 MB    | 4326 |
| **hex_57km_layer.shp**                | 4,051          | 627 KB    | 4283 |
| **AUS_2016_AUST.shp**                 | 1              | 26.6 MB   | 4283 |
| **aust_hex_shape_57km.shp**           | 1,262          | 627 KB    | 4283 |
| **SA1_2011_AUST.shp**                 | 54,806         | 174 MB    | 4283 |
| **feat_aust_57km_sa1_11.shp**         | 59,986         | 170 MB    | 4283 |
| **SA1_2016_AUST.shp**                 | 57,523         | 185.5 MB  | 4283 |
| **feat_aust_57km_sa1_16.shp**         | 62,756         | 186.6 MB  | 4283 |
| **2011Census_B18_AUST_SA1_long.csv**  | 54,806         | 19M       | |
| **donor_feat_57km_sa1_11.shp**        | 20,017         | 15.2 MB   | 4283 |
| **2016Census_G18_AUS_SA1.csv**        | 57,523         | 20M       | |
| **donor_feat_57km_sa1_16.shp**        | 18,923         | 14.1 MB   | 4283 |
| **shape_donor_feat_57km_aust_11.shp** | 1,262          | 315 KB    | 4283 |
| **shape_donor_feat_57km_aust_16.shp** | 1,262          | 303 KB    | 4283 |
| **shape_57km_11_16.shp**              | 1,262          | 377 KB    | 4283 |
| **gis_osm_places_free_1.shp**         | | | 4326 |
| **shape_57km_place_count.shp** | 1,262          | | 4283 |
| **shape_57km_11_16_place.shp**  | 1,262          | | 4283 |
| **AGIL.json**         | | | 4326 |
| **shape_57km_agil_count.shp** |           | | 4283 |
| **shape_57km_11_16_place_agil.shp**  | 1,262          | | 4283 |
| **gis_osm_pois_free_1.shp**         | | | 4326 |
| **shape_57km_service_count.shp** |           | | 4283 |
| **shape_57km_11_16_place_agil_service.shp**  | 1,262          | | 4283 |
| **gis_osm_pois_free_1.shp**         | | | 4283 |
| **shape_57km_bstation_count.shp** |           | | 4283 |
| **shape_57km_11_16_place_agil_service_bstation.shp**  | 1,262          | | 4283 |
| **gis_osm_roads_free_1.shp**         | | | 4326 |
| **shape_57km_road_count.shp** |           | | 4283 |
| **shape_57km_11_16_place_agil_service_bstation_road.shp**  | 1,262          | | 4283 |
| **mbsp_database.csv** ||| |
| **shape_57km_mbsp_count.shp** |           | | 4283 |
| **shape_57km_11_16_place_agil_service_bstation_road_mbsp.shp**  | 1,262          | | 4283 |

### Table of data sources

| Website Source    | File              | Download      | Feature count  | File size |
| :-----------------|:------------------|:--------------|:-------------- |:----------|
| *Australian Bureau of Statistics*| AUS_2016_AUST.shp                                                           |[download link](http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_aus_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&5503B37F8055BFFECA2581640014462C&0&July%202016&24.07.2017&Latest)| 1              |           |
|                                  | SA1_2011_AUST.shp                                                           |[download link](http://www.abs.gov.au/ausstats/subscriber.nsf/log?openagent&1270055001_sa1_2011_aust_shape.zip&1270.0.55.001&Data%20Cubes&24A18E7B88E716BDCA257801000D0AF1&0&July%202011&23.12.2010&Latest)| 54,806         | 174 MB    |
|                                  | SA1_2016_AUST.shp                                                           |[download link](http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa1_2016_aust_tab.zip&1270.0.55.001&Data%20Cubes&39A556A0197D8C02CA257FED00140567&0&July%202016&12.07.2016&Latest)| 57,523         | 185.5 MB  |
| | 2011Census_B18_AUST_SA1_long.csv |[download link](https://datapacks.censusdata.abs.gov.au/datapacks/)| 54,806         | 19 MB |
| | 2011Census_B21_AUST_SA1_long.csv |[download link](https://datapacks.censusdata.abs.gov.au/datapacks/)| 54,806         |  |
| | 2011Census_B22_AUST_SA1_long.csv |[download link](https://datapacks.censusdata.abs.gov.au/datapacks/)| 54,806         |  |
| | 2016Census_G18_AUS_SA1.csv |[download link](https://datapacks.censusdata.abs.gov.au/datapacks/)| 57,523         | 20 MB       |
| | 2016Census_G21_AUS_SA1.csv |[download link](https://datapacks.censusdata.abs.gov.au/datapacks/)| 57,523         | 20 MB       |
| | 2016Census_G22_AUS_SA1.csv |[download link](https://datapacks.censusdata.abs.gov.au/datapacks/)| 57,523         | 20 MB       |
| *OSMStreetMap (Australia) from  geofabrik.de* | gis_osm_places_free_1.shp                                                   |[download_link](https://download.geofabrik.de/australia-oceania/australia-latest-free.shp.zip)|         |          |
|  | gis_osm_roads_free_1.shp                                                   |[download_link](https://download.geofabrik.de/australia-oceania/australia-latest-free.shp.zip)|         |          |
|  | gis_osm_pois_free_1.shp                                                   |[download_link](https://download.geofabrik.de/australia-oceania/australia-latest-free.shp.zip)|         |          |
| *data.gov.au* | Australian Government Indigenous Programs & Policy Locations (AGIL) dataset |[download_link](https://data.gov.au/geoserver/agil-dataset/wfs?request=GetFeature&typeName=ckan_34b1c164_fbe8_44a0_84fd_467dba645aa7&outputFormat=json)|          |
| | Mobile Black Spot Program Round 4 | [download_link](https://data.gov.au/dataset/7be6e3ee-043a-4c47-a6eb-a97702419ccd/resource/c6b211ad-3aa2-4f53-8427-01b52a6433a7/download/mbsp_database.csv)|   |  |


|Year|Profile table|DataPack file|Short       |Long      |Column heading description in profile|Type|
|:---|:-----------|:---------|:-----------------------|:-------------------------------------|:----------|:------|
|2011|B18|B18|P_Tot_Need_for_assistance|Persons_Total_Has_need_for_assistance|Need for assistance|PERSONS|
| | | |P_Tot_No_need_for_assistance|Persons_Total_Does_not_have_need_for_assistance|No need for assistance|PERSONS|
| | | |P_Tot_Need_for_assistance_ns	Persons_Total_Need_for_assistance_not_stated|Need for assistance not stated|PERSONS|
| | | |P_Tot_Tot|Persons_Total_Total|Total|PERSONS|
| |B21|B21|P_Tot_prvided_unpaid_assist|Persons_Total_Provided_unpaid_assistance|Provided unpaid assistance|PERSONS|
| | | |P_Tot_No_unpaid_asst_prvided|Persons_Total_No_unpaid_assistance_provided|No unpaid assistance provided|PERSONS|
| | | |P_Tot_Unpaid_assist_ns	Persons_Total_Unpaid_assistance_not_stated|Unpaid assistance not stated|PERSONS
| | | |P_Tot_Tot	Persons_Total_Total	B21	B21	Total|PERSONS|
| |B22B|B22|P_Tot_CF_Total	Persons_Total_Cared_for_Total|Cared for: Total|PERSONS|
| | | |P_Tot_DNPCC|Persons_Total_Did_not_provide_child_care|Did not provide child care|PERSONS|
| | | |P_Tot_UCC_NS|Persons_Total_Unpaid_child_care_not_stated|Unpaid child care not stated|PERSONS|
| | | |P_Tot_Total|Persons_Total_Total|Total|PERSONS|
|2016|G18|G18|P_Tot_Need_for_assistance|Persons_Total_Has_need_for_assistance|Need for assistance|PERSONS|
| |||P_Tot_No_need_for_assistance|Persons_Total_Does_not_have_need_for_assistance|No need for assistance|PERSONS|
| |||P_Tot_Need_for_assistance_ns|Persons_Total_Need_for_assistance_not_stated|Need for assistance not stated|PERSONS|
| |||P_Tot_Tot|Persons_Total_Total|Total|PERSONS|
| |G21|G21|P_Tot_prvided_unpaid_assist|Persons_Total_Provided_unpaid_assistance|Provided unpaid assistance|PERSONS|
| |||P_Tot_No_unpaid_asst_prvided	Persons_Total_No_unpaid_assistance_provided	G21	G21	No unpaid assistance provided|PERSONS
| |||P_Tot_Unpaid_assist_ns	Persons_Total_Unpaid_assistance_not_stated	G21	G21	Unpaid assistance not stated|PERSONS
| |||P_Tot_Tot|Persons_Total_Total|Total|PERSONS|
| |G22B|G22|P_Tot_CF_Total|Persons_Total_Cared_for_Total|Cared for: Total|PERSONS|
| |||P_Tot_DNPCC|Persons_Total_Did_not_provide_child_care|Did not provide child care|PERSONS|
| |||P_Tot_UCC_NS|Persons_Total_Unpaid_child_care_not_stated|Unpaid child care not stated|PERSONS|
| |||P_Tot_Total|Persons_Total_Total|Total|PERSONS|



