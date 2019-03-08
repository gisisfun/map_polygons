# Map Polygons for Data Visualisation (Hexagons and Boxes)
*A good visualisation is worth the wait(weight).*
![alt text](https://raw.githubusercontent.com/gisisfun/map_polygons/master/SA1_need_for_assistance_2011.png)

## See for yourself ##

In the *shapefiles* subdirectory you wll find two shapefiles: *shape_57km_area_11_16.shp* and *shape_57km_place_11_16.shp*.
Open one or both of these files in your preferred GIS tool of choice and have a look at the end product for yourself.

## How does it work ##

- **CPython 3.7** for list creation/management and construction of geometric shapes.
- **Pandas** for csv file outputs.
- **Python3 modules** for downloading and unzipping content from the ABS website.
- **Geopy** for projection based point calculations for list.
- **GeoJSON** for encoding of the geometric shapes.
- **GDAL/ogr2ogr** for shapefile conversion, simple geometry SQL queries.
- **PROJ** for reprojection.
- **Sqlite3** for generation of SQL definitions for **spatialite**.
- **Spatialite** for more complex SQL queries.
- Shell - **Bash** and **Sed** for moving files to **sqlite** and **spatialite** databases and nit to mention automation of the above. 
- **QGIS** or your favourite GIS Package.
- **You** can contribute or make something better
- Have a look in the shapefiles directory for the processed shape files for area weighted and place point of interest weeighted files.

**polygons.py**

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
| | 2016Census_G21_AUS_SA1.csv |[download link](https://datapacks.censusdata.abs.gov.au/datapacks/)| 57,523         |      |
| | 2016Census_G22_AUS_SA1.csv |[download link](https://datapacks.censusdata.abs.gov.au/datapacks/)| 57,523         |     |
| *OSMStreetMap (Australia) from  geofabrik.de* | gis_osm_places_free_1.shp                                                   |[download_link](https://download.geofabrik.de/australia-oceania/australia-latest-free.shp.zip)|         |          |
|  | gis_osm_roads_free_1.shp                                                   |[download_link](https://download.geofabrik.de/australia-oceania/australia-latest-free.shp.zip)|         |          |
|  | gis_osm_pois_free_1.shp                                                   |[download_link](https://download.geofabrik.de/australia-oceania/australia-latest-free.shp.zip)|         |          |
| *data.gov.au* | Australian Government Indigenous Programs & Policy Locations (AGIL) dataset |[download_link](https://data.gov.au/geoserver/agil-dataset/wfs?request=GetFeature&typeName=ckan_34b1c164_fbe8_44a0_84fd_467dba645aa7&outputFormat=json)|          |
| | Mobile Black Spot Program Round 4 | [download_link](https://data.gov.au/dataset/7be6e3ee-043a-4c47-a6eb-a97702419ccd/resource/c6b211ad-3aa2-4f53-8427-01b52a6433a7/download/mbsp_database.csv)|   |  |

## Data Processing Files 
Polygon shapes are given attributes from data sets with spatial references. The polygon data is processed using scripts with their SQL and vrt file pointing to file names.  
For this example, spatial and tabular attribute data have been selected. The content is ABS SA1 2011 and 2016 shapefiles with associated demographic data items. The data was sourced from the the Australian Bureau of Statistics (ABS).

The hexagon or box shapes are created by the polygons.py python program. The features can be points, lines, polygons with or with attributes to be aggrregated into the hexagon or box shapes.

## Populate shapes with data (Python)

After you have download the files in the table above add data using file_to_db.py:
python3.py file_todb.py or the following bash shell scripts:

(only works with hexagons of 57km at this point time)

**Create hexagons/ boxes**
**Filter to coastline**  
**Feature cut to shape and area weight** 
**Attrib Data to shape** 
**Calculate place weight** 
**Attrib Data to shape**
**Make non ABS counts**
**Merge attrib data** 

### Table Summary of processing files and components

| File | VRT File | SQL File |
|:-------------|:----------|:-------|
| **polygons.py**       |                    |                    |
| **file_to_db.py**     |all.vrt|aust_shape.sql |
|  |all.vrt|feat_aust_11.sql |
|   |all.vrt|feat_aust_16.sql |
|   | |donor_feat_area_11_B18_B21_B22_csv.txt |
|   | |donor_feat_area_16_G18_G21_G22_csv.txt |
|  | |donor_feat_place_11_B18_B21_B22_csv.txt |
|  | |donor_feat_place_16_G18_G21_G22_csv.txt |
| | |shape_nonabs_counts.txt|
|    |shape_11_16.vrt|shape_11_16_area.sql|
|  |shape_11_16.vrt|shape_11_16_place.sql|

### Table of processing files and their input and output files

| File             | Input                            | Output                           |
| :----------------|:---------------------------------|:---------------------------------|
| **polygons.py**      | hex_57km_layer.json              | hex_57km_layer.shp               |
| **file_to_db.py**     | hex_57km_layer.shp               | aust_hex_shape_57km.shp          |
|                  | AUS_2016_AUST.shp                |                                  |
|  | aust_hex_shape_57km.shp          | feat_aust_57km_sa1_11.shp        | 
|                  | SA1_2011_AUST.shp                |                                  | 
|   | aust_hex_shape_57km.shp          | feat_aust_57km_sa1_16.shp        |
|                  | SA1_2016_AUST.shp                |                                  |
|  | feat_aust_57km_sa1_11.shp        | donor_feat_area_57km_11_B18_B21_B22.csv     |
|                  | 2011Census_B18_AUST_SA1_long.csv |                                  |
|                  | 2011Census_B21_AUST_SA1_long.csv |                                  |
|                  | 2011Census_B22_AUST_SA1_long.csv |                                  |
|  | feat_aust_57km_sa1_16.shp        | donor_feat_area_57km_16_G18_G21_G22.csv      |
|                  | 2016Census_G18_AUS_SA1.shp       |                                  |                               |
|                  | 2016Census_G21_AUS_SA1.shp       |                                  |                               |
|                  | 2016Census_G22_AUS_SA1.shp       |                                  |                               |
|  | feat_aust_57km_sa1_11.shp        | donor_feat_place_57km_11_B18_B21_B22.csv     |
|                  | 2011Census_B18_AUST_SA1_long.csv |                                  |
|                  | 2011Census_B21_AUST_SA1_long.csv |                                  |
|                  | 2011Census_B22B_AUST_SA1_long.csv |                                  |
|                  | gis_osm_places_free_1   |                                  |
|                  | feat_aust_57km_sa1_16 |                                  |
|  | feat_aust_57km_sa1_16.shp        | donor_feat_place_57km_16_G18_G21_G22.csv      |
|                  | 2016Census_G18_AUS_SA1.shp       |                                  |                             
|                  | 2016Census_G21_AUS_SA1.shp       |                                  |                              
|                  | 2016Census_G22_AUS_SA1.shp       |                                  |        
|                  | gis_osm_places_free_1   |                                  |
|                  | feat_aust_57km_sa1_11 |                                  |
|  |aust_hex_shape_57km.shp  | shape_57km_place_count.shp |
| | gis_osm_places_free_1.shp | |
|   |aust_hex_shape_57km.shp  | shape_57km_agil_count.shp             |
| | agil.shp | |
|  | gis_osm_places_free_1.shp | shape_57km_service_count.shp |
|  | gis_osm_pois_free_1.shp  |shape_57km_service_bstation.shp |
|  | gis_osm_roads_free_1.shp  |shape_57km_road_count.shp |
|  | mbsp_database.csv  |shape_57km_mbsp_count.shp |
| | mbsp.shp ||
|   | donor_feat_57km_11_B18_B21_B22.csv  | shape_57km_area_11_16.shp             |
|                  | donor_feat_57km_16_G18_G21_G22.csv |    |
|                  | shape_57km_place_count.shp | |
|                  | shape_57km_service_count.shp   |   |
|                  | shape_57km_agil_count.shp | |
|                  | shape_57km_mbsp_count.shp |  |
|                  | shape_57km_road_count.shp |  |
|                  | aust_hex_shape_57km.shp |   |
|   | donor_feat_57km_11_B18_B21_B22.csv  | shape_57km_place_11_16.shp             |
|                  | donor_feat_57km_16_G18_G21_G22.csv |    |
|                  | shape_57km_place_count.shp | |
|                  | shape_57km_service_count.shp   |   |
|                  | shape_57km_agil_count.shp | |
|                  | shape_57km_mbsp_count.shp |  |
|                  | shape_57km_road_count.shp |  |
|                  | aust_hex_shape_57km.shp |   |


### Table of feature data set counts and file sizes 

| File                              | Feature count  | File size | Projection (EPSG) |
| :---------------------------------|---------------:|----------:|:-----------------|
| **hex_57km_layer.json**               | 4,051          | 2.4 MB    | 4326 |
| **hex_57km_layer.shp**                | 4,051          | 627 KB    | 4283 |
| **AUS_2016_AUST.shp**                 | 1              | 26.6 MB   | 4283 |
| **aust_hex_shape_57km.shp**           | 1,262          | 627 KB    | 4283 |
| **SA1_2011_AUST.shp**                 | 54,806         | 174 MB    | 4283 |
| **feat_aust_57km_sa1_11.csv**         | 59,986         |    |  |
| **SA1_2016_AUST.shp**                 | 57,523         | 185.5 MB  | 4283 |
| **feat_aust_57km_sa1_11.csv**         | 62,756         |  |  |
| **2011Census_B18_AUST_SA1_long.csv**  | 54,806         |        | |
| **2011Census_B21_AUST_SA1_long.csv**  | 54,806         |      | |
| **2011Census_B22B_AUST_SA1_long.csv**  | 54,806         |      | |
| **2016Census_G18_AUS_SA1.csv**        | 57,523         |       | |
| **2016Census_G21_AUS_SA1.csv**        | 57,523         |       | |
| **2016Census_G22B_AUS_SA1.csv**        | 57,523         |       | |
| **donor_feat_11_area_B18_B21_B22.csv** | 1,262          |    |  |
| **donor_feat_16_area_G18_G21_G22.csv** | 1,262          |    | |
| **feat_57km_11_place_wt.csv** |  |  |  |
| **feat_57km_16_place_wt.csv** |  |  |  |
| **donor_feat_11_place_B18_B21_B22.csv** | 1,262          |    |  |
| **donor_feat_16_pace_G18_G21_G22.csv** | 1,262          |    | |
| **gis_osm_places_free_1.shp**         | | | 4326 |
| **shape_57km_place_count.csv** | 1,262          | | 4283 |
| **AGIL.json**         | | | 4326 |
| **agil.shp**         | | | 4326 |
| **shape_57km_agil_count.shp** |           | | 4283 |
| **gis_osm_pois_free_1.shp**         | | | 4326 |
| **shape_57km_service_count.csv** |           | | 4283 |
| **gis_osm_pois_free_1.shp**         | | | 4283 |
| **shape_57km_bstation_count.csv** |           | | 4283 |
| **gis_osm_roads_free_1.shp**         | | | 4326 |
| **shape_57km_road_count.csv** |           | | 4283 |
| **mbsp_database.csv** ||| |
| **mbsp.shp** ||| |
| **shape_57km_mbsp_count.csv** |           | | 4283 |
| **shape_57km_area_11_16.shp**              | 1,262          | 377 KB    | 4283 |
| **shape_57km_place_11_16.shp**              | 1,262          | 377 KB    | 4283 |


### Disability, Need for Assistance and Carers (Census Data Dictionary)
- ASSNP Core Activity Need for Assistance
- UNCAREP Unpaid Assistance to a Person with a Disability
- CHCAREP Unpaid Child Care

http://www.ausstats.abs.gov.au/ausstats/subscriber.nsf/0/4D2CE49C30755BE7CA2581BE001540A7/$File/2016%20census%20dictionary.pdf

### ASSNP Core Activity Need for Assistance June release
Measures the number of people with a profound or severe disability.
People with a profound or severe disability are defined as those people needing
help or assistance in one or more of the three core activity areas of self-care,
mobility and communication, because of a disability, long-term health condition
(lasting six months or more) or old age.
Applicable to: All persons
Categories: 

|Code|Description|
|:--|:--------------------------|
|1|Has need for assistance with core activities|
|2|Does not have need for assistance with core activities|
|&|Not stated|
|V|Overseas visitor|

Number of categories: 4

### UNCAREP Unpaid Assistance to a Person with a Disability June release
Records people who in the two weeks prior to Census night spent time providing unpaid care, help or
assistance to family members or others because of a disability, a long-term health condition or
problems related to old age. This includes people who are in receipt of a Carer Allowance or Carer
Payment. It does not include work done through a voluntary organisation or group.
Applicable to: Persons aged 15 years and over
Categories: 

|Code|Description|
|:--|:--------------------------|
|1|No unpaid assistance provided|
|2|Provided unpaid assistance|
|&|Not stated|
|@|Not applicable|
|V|Overseas visitor|

- Number of categories: 5
- Not applicable (@) category comprises:
- Persons aged under 15 years

### CHCAREP Unpaid Child Care June release
Records people, who in the two weeks prior to Census night, spent time caring for a child/children
(under 15 years) without pay.
Applicable to: Persons aged 15 years and over
Categories: 

|Code|Description|
|:--|:--------------------------|
|1| Did not provide child care|
|2|Cared for own child/children|
|3|Cared for other child/children|
|4|Cared for own child/children and other child/children|
|&|Not stated|
|@|Not applicable|
|V|Overseas visitor|

- Number of categories: 7
- Not applicable (@) category comprises:
- Persons aged under 15 years

### Disability, Need For Assistance and Carers Census Data Pack Tables with Output Column Names

|2011|2016|Table Name | count 11 | count 16 | total 11 | total 16 |
|:---|:----|:-------------------------------------------------------------|:----|:----|:----|:----|
|B18|G18|Core Activity Need for Assistance by Age by Sex|NeedA11|NeedA16|NeedAT11|TNeedAT16|
|B21|G21|Unpaid Assistance to a Person with a Disability by Age by Sex|UPunPA11|UPunP16|UPunPT11|UPunPT16|
|B22B|G22B|Unpaid Child Care by Age by Sex|PUnPCC11|PUnPCC16|PUnPCCT11|PUnPCCT16|

### Census Data Pack Metadata

|Year|Profile table|Data Pack file|Short       |Long      |Column heading description in profile|Type|
|:---|:-----------|:---------|:-----------------------|:-------------------------------------|:----------|:------|
|2011|B18|B18|P_Tot_Need_for_assistance|***Persons_Total_Has_need_for_assistance***|Need for assistance|PERSONS|
| | | |P_Tot_No_need_for_assistance|Persons_Total_Does_not_have_need_for_assistance|No need for assistance|PERSONS|
| | | |P_Tot_Need_for_assistance_ns|Persons_Total_Need_for_assistance_not_stated|Need for assistance not stated|PERSONS|
| | | |P_Tot_Tot|***Persons_Total_Total***|Total|PERSONS|
| |B21|B21|P_Tot_prvided_unpaid_assist|***Persons_Total_Provided_unpaid_assistance***|Provided unpaid assistance|PERSONS|
| | | |P_Tot_No_unpaid_asst_prvided|Persons_Total_No_unpaid_assistance_provided|No unpaid assistance provided|PERSONS|
| | | |P_Tot_Unpaid_assist_ns|Persons_Total_Unpaid_assistance_not_stated|Unpaid assistance not stated|PERSONS
| | | |P_Tot_Tot|***Persons_Total_Total***|Total|PERSONS|
| |B22B|B22|P_Tot_CF_Total|***Persons_Total_Cared_for_Total***|Cared for: Total|PERSONS|
| | | |P_Tot_DNPCC|Persons_Total_Did_not_provide_child_care|Did not provide child care|PERSONS|
| | | |P_Tot_UCC_NS|Persons_Total_Unpaid_child_care_not_stated|Unpaid child care not stated|PERSONS|
| | | |P_Tot_Total|***Persons_Total_Total***|Total|PERSONS|
|2016|G18|G18|***P_Tot_Need_for_assistance***|Persons_Total_Has_need_for_assistance|Need for assistance|PERSONS|
| |||P_Tot_No_need_for_assistance|Persons_Total_Does_not_have_need_for_assistance|No need for assistance|PERSONS|
| |||P_Tot_Need_for_assistance_ns|Persons_Total_Need_for_assistance_not_stated|Need for assistance not stated|PERSONS|
| |||***P_Tot_Tot***|Persons_Total_Total|Total|PERSONS|
| |G21|G21|***P_Tot_prvided_unpaid_assist***|Persons_Total_Provided_unpaid_assistance|Provided unpaid assistance|PERSONS|
| |||P_Tot_No_unpaid_asst_prvided|Persons_Total_No_unpaid_assistance_provided|No unpaid assistance provided|PERSONS|
| |||P_Tot_Unpaid_assist_ns|Persons_Total_Unpaid_assistance_not_stated|Unpaid assistance not stated|PERSONS|
| |||***P_Tot_Tot***|Persons_Total_Total|Total|PERSONS|
| |G22B|G22|***P_Tot_CF_Total***|Persons_Total_Cared_for_Total|Cared for: Total|PERSONS|
| |||P_Tot_DNPCC|Persons_Total_Did_not_provide_child_care|Did not provide child care|PERSONS|
| |||P_Tot_UCC_NS|Persons_Total_Unpaid_child_care_not_stated|Unpaid child care not stated|PERSONS|
| |||***P_Tot_Total***|Persons_Total_Total|Total|PERSONS|



