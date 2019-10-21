class Defaults:
    """
    """
    ...
    
    
    def __init__(self):
        self.Radial = 57
        self.Shape = 'hex'
        

class Bounding_Box:
    """
    Parameters for request to create tessilating shapes
    """
    ...
    class Australia:
        __slots__ = ("North","South","East","West","Radial","Shape")
    
        def __init__(self):
            """
            Init
            """
            self.North = -8
            self.South = -45
            self.East = 168
            self.West = 96

class Offsets:
    """
    Offset ratios for underlying points grid
    """

    __slots__ = ("Short","Long")
    def __init__(self):
        self.Short = 0.7071
        self.Long = 1

class OSVars:
    """
    Operating System Dependant values for 'posix' and 'nt'
    """

    class posix:
        __slots__ = ("Slash","ogr2ogr")
        def __init__(self):
            self.Slash = '/'
            self.ogr2ogr = '/usr/bin/ogr2ogr'
        

    class nt:
        __slots__ = ("Slash","ogr2ogr")
        def __init__(self):
            self.Slash = '\\'
            self.ogr2ogr = 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'

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
                
    
        class TabFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            def __init__(self):
                self.Description = 'ABS Australia'
                self.Format = 'Tab'
                self.FilePath = 'tabfiles{slash}AUS_2016_AUST.tab'
                self.DownURL = 'http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_aus_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&5503B37F8055BFFECA2581640014462C&0&July%202016&24.07.2017&Latest'
                self.ZipDir = 'tabfiles'
                self.ZipPath ='tabfiles{slash}1270055001_aus_2016_aust_tab.zip'
                
        class Statistical_Areas_Level_1_2011:
            class Shape:
                self.Description = 'ABS Australia'
                self.Format = 'Shape'
                self.FilePath = 'shapefiles{slash}SA1_2011_AUST.shp'
                self.DownURL = 'http://www.abs.gov.au/ausstats/subscriber.nsf/log?openagent&1270055001_sa1_2011_aust_shape.zip&1270.0.55.001&Data%20Cubes&24A18E7B88E716BDCA257801000D0AF1&0&July%202011&23.12.2010&Latest'
                self.ZipDir = 'shapefiles'
                self.ZipPath ='shapefiles{slash}1270055001_sa1_2011_aust_shape.zip'
                
        class Statistical_Areas_Level_1_2016:
            class Shape:
                self.Description = 'ABS Australia'
                self.Format = 'Shape'
                self.FilePath = 'shapefiles{slash}SA1_2011_AUST.shp'
                self.DownURL = 'http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa1_2016_aust_tab.zip&1270.0.55.001&Data%20Cubes&39A556A0197D8C02CA257FED00140567&0&July%202016&12.07.2016&Latest'
                self.ZipDir = 'shapefiles'
                self.ZipPath ='shapefiles{slash}1270055001_sa1_2011_aust_shape.zip'
                
        class AGIL_Dataset:
            class csv:
                self.Description = 'AGIL DataSet'
                self.Format = 'CSV'
                self.FilePath = 'csv{slash}agil_locations20190208.csv'
                self.DownURL = 'https://data.gov.au/dataset/34b1c164-fbe8-44a0-84fd-467dba645aa7/resource/625e0a41-6a30-4c11-9a20-ac64ba5a1d1f/download/agil_locations20190208.csv'                
                self.ZipDir = 'csv'
                self.ZipPath =''
                                
                
                https://data.gov.au/dataset/34b1c164-fbe8-44a0-84fd-467dba645aa7/resource/625e0a41-6a30-4c11-9a20-ac64ba5a1d1f/download/agil_locations20190208.csv
                
    class OpenStreetMaps:
        
        class ShapeFormat:
            
            def __init__(self):
                self.Description = 'OpenStreetMaps'
                self.Format = 'Shape'
                self.FilePath = 'shapefiles{slash}gis_osm_places_free_1.shp'
                self.DownURL = 'https://download.geofabrik.de/australia-oceania/australia-latest-free.shp.zip'
                self.ZipDir = 'shapefiles'
                self.ZiPath = 'shapefiles{slash}australia-latest-free.shp.zip'
        