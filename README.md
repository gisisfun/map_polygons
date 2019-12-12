# Map Polygons for Data Visualisation (Hexagons and Boxes)
*A good visualisation is worth the wait(weight).*

![alt text](https://raw.githubusercontent.com/gisisfun/map_polygons/master/images/polygons_output.png)
![alt text](https://raw.githubusercontent.com/gisisfun/map_polygons/master/images/neighbours.png)
*output of polygons.py as png output and reference points for islands added in QGIS*

 *aus_hex_57km_layer*

Download Links
- Shapefile Format: [ESRI .prj](https://github.com/downloads/gisisfun/map_polygons/shapefiles/aus_hex_57km_layer.prj), [ESRI .shp ](https://raw.githubusercontent.com//gisisfun/map_polygons/shapefiles/aus_hex_57km_layer.shp), [ESRI .shx](https://raw.githubusercontent.com/s/gisisfun/map_polygons/shapefiles/aus_hex_57km_layer.shx), [ESRI .dbf](https://raw.githubusercontent.com/s/gisisfun/map_polygons/shapefiles/aus_hex_57km_layer.dbf)
- [GeoJSON](https://raw.githubusercontent.com//gisisfun/map_polygons/geojson/aus_hex_57km_layer.json)
- [KML](https://raw.githubusercontent.com/gisisfun/map_polygons/kmlfiles/aus_hex_57km_layer.kml)

**Why Wait?**
The Python approach to cutting out the shape of 'australia' from the derived polygon dataset is not as efficient as using an SQL approach. SQL is efficient but no where near as flexible as Python. If you are not blending region based statistics into the final data set then the 'aus_(hex or box)_(size in km)km_layer' file in kml, geojson and shapefile will meet your needs.

Note: Python joins allow for two islands have added to the map (mapping layer) : Ashmore Reef and Norfolk Island. Complex SQL joins or modification of the base mapping layer are normally required to achieve the same effect.


Proceed to **poly_wt.py** to add the demographic data of your choice. In this case ABS Statistical Area Level 1 data sets are merged together to mease the 'relative change in need for assistance'.

**output of map_me.py**
![alt text](https://raw.githubusercontent.com/gisisfun/map_polygons/master/images/rel_need_for_assistance_by_place_weight.png)

 *hex_57km_place_11_16*

Download Links
- Shapefile Format: [ESRI .prj](https://github.com/downloads/gisisfun/map_polygons/shapefiles/hex_57km_place_11_16.prj), [ESRI .shp](https://github.com/downloads/gisisfun/map_polygons/shapefiles/hex_57km_place_11_16.shp), [ESRI .shx](https://github.com/downloads/gisisfun/map_polygons/shapefiles/hex_57km_place_11_16.shx), [ESRI .dbf](https://github.com/downloads/gisisfun/map_polygons/shapefiles/hex_57km_place_11_16.dbf)
- [GeoJSON](https://github.com/downloads/gisisfun/map_polygons/geojson/hex_57km_place_11_16.json)
- [KML](https://github.com/downloads/gisisfun/map_polygons/kmlfiles/hex_57km_place_11_16.kml)

![alt text](https://raw.githubusercontent.com/gisisfun/map_polygons/master/images/rel_need_for_assistance_by_area_weight.png)

 *hex_57km_area_11_16*
Download Links
- Shapefile format: [ESRI .prj](https://github.com/downloads/gisisfun/map_polygons/shapefiles/hex_57km_area_11_16.prj), [ESRI .shp](https://github.com/downloads/gisisfun/map_polygons/shapefiles/hex_57km_area_11_16.shp), [ESRI .shx](https://github.com/downloads/gisisfun/map_polygons/shapefiles/hex_57km_area_11_16.shx), [ESRI .dbf](https://github.com/downloads/gisisfun/map_polygons/shapefiles/hex_57km_area_11_16.dbf)
- [GeoJSON](https://github.com/downloads/gisisfun/map_polygons/geojson/hex_57km_area_11_16.json)
- [KML](https://github.com/downloads/gisisfun/map_polygons/kmlfiles/hex_57km_area_11_16.kml)

## How does it work ##

- **CPython 3.7** for list creation/management and construction of geometric shapes.
- **pandas** for csv file outputs.

*Map Polygons* - polgons.py
- **geopy** for projection based point calculations for list.
- **geojson** for encoding of the geometric shapes.
- **matplotlib** find points inside polygons.
- **pyshp** for encoding ESRI shapefiles.
Note: additional operating system libraries are not required for the python modules listed above (Thank you @psmaAaron). This will be useful if your IT department does not support the GDAL libraries/executables on the operating system.

*Post Processing* - poly_wt.py
- **pyunpack** for downloading and unzipping content from the ABS website.
- **GDAL/ogr2ogr** for shapefile conversion, simple geometry SQL queries.
- **sqlite3** for accessing for **spatialite** content and processing large tables of tabular content.
Note: Operating system libraries are required for GDAL support.

*Visulisation* - map_me.py
- **geopandas**, **numpy** and **matplotlib** for making really good maps.
- **QGIS** or your favourite GIS Package.
- **You** can contribute or make something better
- Have a look in the shapefiles directory for the processed shape files for area weighted and place point of interest weighted files.

**Useful Python and R Libraries**
Choropleths (Thematic mapping) choroplethr (R) pysal (Python)

**The Python Code will switch between Linux and Windows Enviromments**

For full functionality with Windows OS, download the OSGeo4W package and install the 'express install'. The code will map to the standard installation location on C drive. The code was originally bult for Linux OS. Linux has pretty good package management so no worries here. All python modules are installed using pip3. **polygons.py** has been tested and works with Linux and Windows.

Download and install with default options the OSGeo4W distriution for Windows

- https://trac.osgeo.org/osgeo4w/

Download the python wheel packages from links for geopandas

- https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona 
- https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal 
- https://www.lfd.uci.edu/~gohlke/pythonlibs/#basemap

Add the PATH variable

- C:\OSGeo4W64\bin
- C:\OSGeo4W64\include

Create/add a GDAL_PATH variable

- C:\OSGeo4W64\share\gdal

to the Windows environment variables for 'PATH' and path c:\OSGeo4W\share\gdal for 'GDAL_PATH' .You can 'pip3 install' your modules.
**pygeogrids**

https://pygeogrids.readthedocs.io/en/v0.1/_rst/pygeogrids.html 

**R version in development**

Not everyone has access to Python so there is an R version of the code with much of the same features. Have a look at **polygons2.R**. The code is functional in a Windows environment using the OSGeo4W software. 

see the end result http://rpubs.com/damien123/506636

This R library is quite nice https://github.com/r-barnes/dggridR  and result http://rpubs.com/damien123/506921

Add to the PATH variable

- C:\OSGeo4W64\bin
- C:\OSGeo4W64\include
- C:\Program Files\R\R-3.6.0\bin


**Why not use Vendor 'XYZ' or 'ABC' Software?**

The processes applied to the datasets would normally be tasked to individual analysts and use software purchased for that purpose.
There are software packages that work at a larger scale than the desktop analysis to perform more industrial scale processes. Again there is another set of personnel to achieve perform these tasks.
Making the best use of both types of software is a challenge. A task can escalate beyond the capabalilities of desktop software or a task began at the indsutrial scale can become unmanageable.

The list of software is entirely open sourced. The coding and deployement of sub systems where chosen according to each software's ability to perform a given task in set period of time balancing out memory, storage and CPU access requirements.
The data could be processed by running a single Python program (currently three) by one person. In an open source environment interoperability of automation, data format and operating system support is assumed.

A process built around purchased software would deliver a dataset output like this one, but it would have to work arounf the constraints of the environment in which the software has been deployed. Vendor purchased software is interoperable with other software from the same vendor at the data and automation level.

Vendor operating systems such as Windows 10 now allows for an instance of the open source Linux operating system to operate on top of a Windows 10 platform. If not there are other options that are less attractive. The Windows Subsystem for Linux (WSL) once enabled allows for a choice of your preferred Linux distribution.The other option is to deploy open source software and sub systems in Windows 10 is to use the OSGeo4W resource.

OSGeo4W is a binary distribution of a broad set of open source geospatial software for Win32 and Win64 environments (Windows XP, Vista, Windows 7, Windows 10). OSGeo4W includes GDAL/OGR, ​Python3, ​QGIS, ​SQLite, as well as many other packages (over 150 as of December 2015). This has dependencies on Windows 10 Developer software for compiling Python libraries and and SQL server runtime software that tends the prevents installation of the software.

**polygons.py**

This program was an attempt to replicate the Discrete Global Grid System (DGGS) standrd output . In attempting achieve this goal other options were able to explored and a lot of fun had while keeping the desired functionality of the DGGS with the functionality of existing boundary data sets. The polygons cover the same area as the boundary data. 

command line arguments are: 
- shape - hex or box 
- bounding north
- bounding south
- bounding east
- bounding west
- radial in km
- filename for output

for hexagon:
python3 polygons.py hex -8 -45 168 96 212 hex_212km

for boxes:
python3 polygons.py box -8 -45 168 96 212 box_212km

**Why the Weight - Places or Regions** 

Region data with aggregate data values is represented by summarised from an area defined by a polygon. The majority of administrative boundary data sets small areas areas for high population counts and large areas for small population counts. 

For an area weighted correspondence file to a smaller polgons dataset, larger polygon areas with low population counts will mask areas of high values within the polygon. Area weighting is good for land management, associating population density with the feature count. Area weighting takes less time and computer resources, but is more relevant to regions rather than places.

For a population weighted correspondence file to a smaller polgons dataset, larger polygon areas with low population counts will be weighted to where people live within the polygon. Population weights reflect the population criteria with a smaller polygon size that better relates to discrete locations of interest. Population weighting takes more time and computer resources, but is more relevant to places rather than regions.

In this example the number of points of interest (POI) within and between interecting areas is used a proxy for a population weight.

**poly_wt.py**

This program populate the shapes with demographic and POI based dataset content dor the **area** weighted analysis and include some of of this data to **place** weight values in larger overlalapping regions.

**map_me.py**

Make the really good map at the top of the document.

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
| *data.gov.au* | Australian Government Indigenous Programs & Policy Locations (AGIL) dataset |[download_link](https://data.gov.au/dataset/34b1c164-fbe8-44a0-84fd-467dba645aa7/resource/625e0a41-6a30-4c11-9a20-ac64ba5a1d1f/download/agil_locations20190208.csv)|          |
| | Mobile Black Spot Program Round 4 | [download_link](https://data.gov.au/dataset/7be6e3ee-043a-4c47-a6eb-a97702419ccd/resource/c6b211ad-3aa2-4f53-8427-01b52a6433a7/download/mbsp_database.csv)|   |  |

## Data Processing Files 
Polygon shapes are given attributes from data sets with spatial references. The polygon data is processed using scripts with their SQL and vrt file pointing to file names.  
For this example, spatial and tabular attribute data have been selected. The content is ABS SA1 2011 and 2016 shapefiles with associated demographic data items. The data was sourced from the the Australian Bureau of Statistics (ABS).

The hexagon or box shapes are created by the polygons.py python program. The features can be points, lines, polygons with or with attributes to be aggrregated into the hexagon or box shapes.

## Populate shapes with data 

After you have download the files in the table above add data using file_to_db.py:
python3.py file_to_db.py or the following bash shell scripts:

(only works with hexagons of 57km at this point time)
Performs the functions:

- Filter to coastline
- Feature cut to shape and calculate area weight
- Attrib Data to shape and apply area weight
- Calculate place weights 
- Attrib Data to shape and apply place weights
- Make non ABS counts for each shape
- Merge attrib data to area and place weighted shapes

### Table Summary of processing files and components

| File | VRT File | SQL File |
|:-------------|:----------|:-------|
| **polygons.py**       |                    |                    |
| **place_wt.py**     ||aust_shape.sql |
|  |all.vrt|feat_aust_11.sql |
|   |all.vrt|feat_aust_16.sql |
|  | |tabular_place_wt.txt |
| | |tabular_area_wt.txt|
|    |all.vrt|shape_11_16_area.sql|
|  |all.vrt|shape_11_16_place.sql|

### Table of processing files and their input and output files

| File             | Input                            | Output                           |
| :----------------|:---------------------------------|:---------------------------------|
| **polygons.py**      | hex_57km_layer.json              | hex_57km_layer.shp               |
|  | hex_57km_points.csv | hex_57km_neighbours.csv |
| **place_wt.py**     | hex_57km_layer.shp               |          |
|                  | AUS_2016_AUST.shp                |    aust_hex_shape_57km.shp      |
|  |        SA1_2011_AUST.shp   | feat_aust_57km_sa1_11.shp        | 
|   |     SA1_2016_AUST.shp       | feat_aust_57km_sa1_16.shp        |
|                  | 2011Census_B18_AUST_SA1_long.csv |                                  |
|                  | 2011Census_B21_AUST_SA1_long.csv |                                  |
|                  | 2011Census_B22B_AUST_SA1_long.csv |                               |                           
|                  | 2016Census_G18_AUS_SA1.csv       |                                  |                             
|                  | 2016Census_G21_AUS_SA1.csv      |                                  |                              
|                  | 2016Census_G22_AUS_SA1.csv     |                                  |                                       |
| | agil.shp | |
|  | gis_osm_places_free_1.shp | |
|  | gis_osm_pois_free_1.shp  | |
|  | gis_osm_roads_free_1.shp  |  |
|  | mbsp_database.csv  | |
| | mbsp.shp ||
|   | tabular_hex_57km_11_16_area.csv  | hex_57km_area_11_16.shp          |
|   | tabular_hex_57km_place.csv  | hex_57km_place_11_16.shp             |

*The Australian Bureau of Statistics (ABS) supplies Census demographic to the level to Statistical Area Level 2 (SA2) via a public facing Web API. Statistical Area Level 1 have the most detail and the lowest geographic classification. Truncated CSV files Census data pack tables have been used for this example.

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
| **donor_feat_11_place_B18_B21_B22.csv** | 1,262          |    |  |
| **donor_feat_16_pace_G18_G21_G22.csv** | 1,262          |    | |
| **gis_osm_places_free_1.shp**         | | | 4326 |
| **AGIL.json**         | | | 4326 |
| **agil.shp**         | | | 4326 |
| **gis_osm_pois_free_1.shp**         | | | 4326 |
| **gis_osm_pois_free_1.shp**         | | | 4283 |
| **gis_osm_roads_free_1.shp**         | | | 4326 |
| **mbsp_database.csv** ||| |
| **mbsp.shp** ||| |
| **tabular_57km_11_16_area**||| |
| **tabular_57km_11_16_place** ||| |
| **hex_57km_area_11_16.shp**              | 1,262          | 377 KB    | 4283 |
| **hex_57km_place_11_16.shp**              | 1,262          | 377 KB    | 4283 |


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

### Conclusion
If you have read down to this point in the documemtation then you can see the end result is worth the wait. The benefits of using a Discrete Global Grid System (DGGC) like visualisation is better on the eye once you see it for yourself. But this depends on how your data is made and how fast you want it made. If your data is like this then a traditional SQL server will do just fine, with a bit of extra work. You will have access to all of the viewing and map production software that the current generation of software going back to the 1990s will provide. 

Larger volumes of data and newer SPARQL/GeoSPARQL and Discrete Global Grid System (DGGC) enabled systems and and data sets provide a much better end product for the real users of this data. Not the Geospatial Anaysts, staticians but the people who benefit from decisions informed from data.  

**Further Reading**

- http://redblobgames.com/grids/hexagons
- https://geoawesomeness.com/discrete-global-grid-system-dggs-new-reference-system/
- https://wiki.openstreetmap.org/wiki/Australian_data_catalogue



To finish things off it would be nice to be able to run multiple instances of the same code to process all of the different data sources and visualisation requirements. Containerisation allows for all of this to happen.
## Done
**Class and method conversion of Python code.**
see **polygons.py**, **poly_wt.py**, **map_me.py** and **isotiles** directory for work on 'pythonisation' (classes) of polygons,py code to allow for Docker and API use cases. Fixed some buggy SQL code for area weighted calculations.

## To Do

**PostGIS** 
PostgreSQL/Postgis does some really good things with spatial data and ogr2ogr handles the Nerd (DDL) content issues.

**Docker/Containerisation**

Rebuilding the Python and SQLITE code around the Docker environment makes the code portable and usable in a production environment. 
