class Defaults:
    """
    """
    ...
    __slots__ = ("Radial","Shape","ShapefilesPath","TabfilesPath", "MetaDataPath", \
                 "GeoJSONPath","CSVPath","ImagesPath","SQLPath","SpatialitePath", \
                 "VRTPath","Weight")
    
    def __init__(self):
        self.Radial = 57
        self.Shape = 'hex'
        self.ShapefilesPath = 'shapefiles'
        self.TabfilesPath  = 'tabfiles'
        self.MetaDataPath = 'metadata'
        self.GeoJSONPath = 'geojson'
        self.CSVPath = 'csv'
        self.ImagesPath = 'images'
        self.SQLPath = 'sql'
        self.SpatialitePath = 'spatialite_db'
        self.VRTPath = 'vrt'
        self.Weight = "place"

class Projection:
    """
    Project Values
    """
    class WGS84:
        """
        WGS 84 Projection
        World Geodectic System 1984, used in GPS
        """
        __slots__ = ("EPSG","name","Perimeter","invFlat")
        def __init__(self):
            self.EPSG = '4326'
            self.Name = 'WGS 84'
            self.Perimeter = 6378137
            self.invFlat = 298.257223563
            
    class GDA94:
        """
        GDA 94 Projection
        Geocentric Datum of Australia 1994
        """
        __slots__ = ("EPSG","name","Perimeter","Flatness")
        def __init__(self):
            self.EPSG = '4283'
            self.Name = 'GDA 84'
            self.Perimeter = 6378137
            self.invFlat = 298.257222101         
            
    class GDA2020:
        """
        GDA 94 Projection
        Geocentric Datum of Australia 1994
        """
        __slots__ = ("EPSG","name","Perimeter","invFlat")
        def __init__(self):
            self.EPSG = '7844'
            self.Name = 'GDA 2020'
            self.Perimeter = 6378137
            self.invFlat = 298.257222101  

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
        __slots__ = ("Slash","Ogr2ogr","Spatialite")
        def __init__(self):
            self.Slash = '/'
            self.Ogr2ogr = '/usr/bin/ogr2ogr'
            self.Spatialite = 'spatialite'
        

    class nt:
        __slots__ = ("Slash","Ogr2ogr","Spatialite")
        def __init__(self):
            self.Slash = '\\'
            self.Ogr2ogr = 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
            self.Spatialite = 'c:\\OSGeo4W64\\bin\\sqlite3.exe'

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

        class ShapeFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            def __init__(self):
                self.Description = '2011 ABS Statistical Areas Level 1'
                self.Format = 'Shape'
                self.FilePath = 'shapefiles{slash}SA1_2011_AUST.shp'
                self.DownURL = 'http://www.abs.gov.au/ausstats/subscriber.nsf/log?openagent&1270055001_sa1_2011_aust_shape.zip&1270.0.55.001&Data%20Cubes&24A18E7B88E716BDCA257801000D0AF1&0&July%202011&23.12.2010&Latest'
                self.ZipDir = 'shapefiles'
                self.ZipPath ='shapefiles{slash}1270055001_sa1_2011_aust_shape.zip'
                
    class Statistical_Areas_Level_1_2016:

        class ShapeFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
            def __init__(self):
                self.Description = 'ABS Australia'
                self.Format = 'Shape'
                self.FilePath = 'shapefiles{slash}SA1_2011_AUST.shp'
                self.DownURL = 'http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa1_2016_aust_tab.zip&1270.0.55.001&Data%20Cubes&39A556A0197D8C02CA257FED00140567&0&July%202016&12.07.2016&Latest'
                self.ZipDir = 'shapefiles'
                self.ZipPath ='shapefiles{slash}1270055001_sa1_2011_aust_shape.zip'
                
    class AGIL_Dataset:
        
        class CSVFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
            def __init__(self):
                self.Description = 'AGIL DataSet'
                self.Format = 'CSV'
                self.FilePath = 'csv{slash}agil_locations20190208.csv'
                self.DownURL = 'https://data.gov.au/dataset/34b1c164-fbe8-44a0-84fd-467dba645aa7/resource/625e0a41-6a30-4c11-9a20-ac64ba5a1d1f/download/agil_locations20190208.csv'                
                self.ZipDir = 'csv'
                self.ZipPath =''
                
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

    class GNAFLocality:
        class: List:

	    def __init__(self):
                self.Items ="""locality_name,state_abbreviation,postcode,latitude,longitude
"""
    class cities:
        class: List:

	    def __init__(self):
                self.Items ="""locality_name,state_abbreviation,postcode,latitude,longitudecity,city_ascii,lat,lng,country,iso2,iso3,admin_name,capital,population,id
"""      
