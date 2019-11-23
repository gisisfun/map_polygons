import os

class Defaults:
    """
    """
    ...
    __slots__ = ("Radial","Shape","ShapefilesPath","LogfilesPath", "KMLFiles", "MetaDataPath", \
                 "GeoJSONPath","CSVPath","KMLfilesPath","ImagesPath","SQLPath","SpatialitePath", \
                 "VRTPath","Weight","Ogr2ogr","Spatialite","Extn","Slash")
    
    def __init__(self):
        self.Radial = 57
        self.Shape = 'hex'
        self.ShapefilesPath = 'shapefiles'
        self.LogfilesPath  = 'logfiles'
        self.KMLfilesPath  = 'kmlfiles'
        self.MetaDataPath = 'metadata'
        self.GeoJSONPath = 'geojson'
        self.CSVPath = 'csv'
        self.ImagesPath = 'images'
        self.SQLPath = 'sql'
        self.SpatialitePath = 'spatialite_db'
        self.VRTPath = 'vrt'
        self.Weight = "place"
        my_os = str(os.name)

        self.Ogr2ogr = self.os_ogr2ogr(my_os) # '/usr/bin/ogr2ogr'
        self.Slash = self.os_slash(my_os) # '/'
        self.Extn = self.os_extn(my_os)
        self.Spatialite = self.os_spatialite(my_os)
        self.os_extn(my_os)

    def os_ogr2ogr(self,my_os):
        posixvars = OSVars.posix()
        ntvars = OSVars.nt()
        if (my_os is 'posix'):
            ogr2ogr = posixvars.Ogr2ogr # '/usr/bin/ogr2ogr'
        else:
            ogr2ogr = ntvars.Ogr2ogr # 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
        return ogr2ogr

    def os_slash(self,my_os):
        posixvars  = OSVars.posix()
        ntvars = OSVars.nt()
        if (my_os is 'posix'):
            slash = posixvars.Slash  #  '/'
        else:
            slash = ntvars.Slash # '\\'
        return slash

    def os_gdal_vars(self,my_os):
        ntvars = OSVars.nt()
        if (my_os is 'nt'):
            Gdal_vars = {'GDAL_DATA': 'C:\OSGeo4W64\share\gdal'}
            os.environ.update(Gdal_vars)

    def os_extn(self,my_os):
        posixvars = OSVars.posix()
        ntvars = OSVars.nt()
        if (my_os is 'posix'):
            extn = "SELECT load_extension('mod_spatialite.so');"
        else:
            extn = "SELECT load_extension('mod_spatialite.dll');"
        return extn

    def os_spatialite(self,my_os):
        posixvars = OSVars.posix()
        ntvars = OSVars.nt()
        if (my_os is 'posix'):
            spatialite = posixvars.Spatialite
        else:
            spatialite = ntvars.Spatialite
        return spatialite


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
            self.North = -7
            self.South = -45
            self.East = 170
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
