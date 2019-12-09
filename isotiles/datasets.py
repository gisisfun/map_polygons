class DataSets:
    

    class Australia:
        """
        ABS Australian Boundary
        """    
        ...
    
    
        class ShapeFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            def __init__(self):
                self.Description = 'ABS Australia'
                self.Format = 'Shape'
                self.FilePath = 'shapefiles{slash}AUS_2016_AUST.shp'
                self.DownURL = 'http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_aus_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&5503B37F8055BFFECA2581640014462C&0&July%202016&24.07.2017&Latest'
                self.ZipDir = 'shapefiles'
                self.ZipPath ='shapefiles{slash}1270055001_aus_2016_aust_shape.zip'
                
                
    class Statistical_Areas_Level_1_2011:

        class ShapeFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            def __init__(self):
                self.Description = '2011 ABS Statistical Areas Level 1'
                self.Format = 'Shape'
                self.FilePath = 'shapefiles{slash}SA1_2011_AUST.shp'
                self.DownURL = 'https://www.abs.gov.au/ausstats/subscriber.nsf/log?openagent&1270055001_sa1_2011_aust_shape.zip&1270.0.55.001&Data%20Cubes&24A18E7B88E716BDCA257801000D0AF1&0&July%202011&23.12.2010&Latest'
                self.ZipDir = 'shapefiles'
                self.ZipPath = 'shapefiles{slash}1270055001_sa1_2011_aust_shape.zip'
                
    class Statistical_Areas_Level_1_2016:

        class ShapeFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
            def __init__(self):
                self.Description = '2016 ABS Statistical Areas Level 1'
                self.Format = 'Shape'
                self.FilePath = 'shapefiles{slash}SA1_2016_AUST.shp'
                self.DownURL = 'https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa1_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&6F308688D810CEF3CA257FED0013C62D&0&July%202016&12.07.2016&Latest'
                self.ZipDir = 'shapefiles'
                self.ZipPath = 'shapefiles{slash}1270055001_sa1_2016_aust_shape.zip'
    class MBSP:
        class CSVFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
            def __init__(self):
                self.Description = 'mbsp database'
                self.Format = 'CSV'
                self.FilePath = 'csv{slash}mbsp_database.csv'
                self.DownURL = 'https://data.gov.au/dataset/7be6e3ee-043a-4c47-a6eb-a97702419ccd/resource/c6b211ad-3aa2-4f53-8427-01b52a6433a7/download/mbsp_database.csv'                
                self.ZipDir = 'csv'
                self.ZipPath ='csv{slash}mbsp_database.csv'
            
    class AGIL_Dataset:
        
        class CSVFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
            def __init__(self):
                self.Description = 'AGIL DataSet'
                self.Format = 'CSV'
                self.FilePath = 'csv{slash}agil_locations20190208.csv'
                self.DownURL = 'https://data.gov.au/dataset/34b1c164-fbe8-44a0-84fd-467dba645aa7/resource/625e0a41-6a30-4c11-9a20-ac64ba5a1d1f/download/agil_locations20190208.csv'                
                self.ZipDir = 'csv'
                self.ZipPath ='csv{slash}agil_locations20190208.csv'
                
    class OpenStreetMaps:
        
        class ShapeFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
            def __init__(self):
                self.Description = 'OpenStreetMaps'
                self.Format = 'Shape'
                self.FilePath = 'shapefiles{slash}gis_osm_places_free_1.shp'
                self.DownURL = 'https://download.geofabrik.de/australia-oceania/australia-latest-free.shp.zip'
                self.ZipDir = 'shapefiles'
                self.ZipPath = 'shapefiles{slash}australia-latest-free.shp.zip'


    class NASA_Active_Fire_Data:

        class VIIRS_375m:
        
            class ShapeFormat:
                __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
                def __init__(self):
                    self.Description = 'NASA Active Fire Data VIIRS 375m'
                    self.Format = 'Shape'
                    self.FilePath = 'shapefiles{slash}VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.shp'
                    self.DownURL = 'https://firms.modaps.eosdis.nasa.gov/active_fire/viirs/shapes/zips/VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.zip'
                    self.ZipDir = 'shapefiles'
                    self.ZipPath = 'shapefiles{slash}VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.zip'

            class CSVFormat:
                __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
                def __init__(self):
                    self.Description = 'NASA Active Fire Data VIIRS 375 m'
                    self.Format = 'CSV'
                    self.FilePath = 'csv{slash}VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.csv'
                    self.DownURL = 'https://firms.modaps.eosdis.nasa.gov/active_fire/viirs/text/VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.csv'                
                    self.ZipDir = 'csv'
                    self.ZipPath ='csv{slash}VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.csv'

            class KMLFormat:
                __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
                def __init__(self):
                    self.Description = 'NASA Active Fire Data VIIRS 375m'
                    self.Format = 'KML'
                    self.FilePath = 'kmlfiles{slash}VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h'
                    self.DownURL = 'https://firms.modaps.eosdis.nasa.gov/active_fire/c6/kml/MODIS_C6_Australia_and_New_Zealand_24h.kml'                
                    self.ZipDir = 'kmlfiles'
                    self.ZipPath ='kmlfiles{slash}VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.kml'


        class Modis_C6_1km:
        
            class ShapeFormat:
                __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
                def __init__(self):
                    self.Description = 'NASA Active Fire Data Modis C6 1km'
                    self.Format = 'Shape'
                    self.FilePath = 'shapefiles{slash}MODIS_C6_Australia_and_New_Zealand_24h.shp'
                    self.DownURL = 'https://firms.modaps.eosdis.nasa.gov/active_fire/c6/shapes/zips/MODIS_C6_Australia_and_New_Zealand_24h.zip'
                    self.ZipDir = 'shapefiles'
                    self.ZipPath = 'shapefiles{slash}MODIS_C6_Australia_and_New_Zealand_24h.zip'

            class CSVFormat:
                __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
                def __init__(self):
                    self.Description = 'NASA Active Fire Data Modis C6 1km'
                    self.Format = 'CSV'
                    self.FilePath = 'csv{slash}MODIS_C6_Australia_and_New_Zealand_24h.csv'
                    self.DownURL = 'https://firms.modaps.eosdis.nasa.gov/active_fire/c6/text/MODIS_C6_Australia_and_New_Zealand_24h.csv'                
                    self.ZipDir = 'csv'
                    self.ZipPath ='csv{slash}MODIS_C6_Australia_and_New_Zealand_24h.csv'

            class KMLFormat:
                __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
                def __init__(self):
                    self.Description = 'NASA Active Fire Data Modis C6 1km'
                    self.Format = 'KML'
                    self.FilePath = 'kmlfiles{slash}MODIS_C6_Australia_and_New_Zealand_24h.kml'
                    self.DownURL = 'https://firms.modaps.eosdis.nasa.gov/active_fire/c6/kml/MODIS_C6_Australia_and_New_Zealand_24h.kml'                
                    self.ZipDir = 'kmlfiles'
                    self.ZipPath ='kmlfiles{slash}MODIS_C6_Australia_and_New_Zealand_24h.kml'




