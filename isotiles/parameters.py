"""
Parameters for map_polygons
"""

import os

class Defaults:
    """
    Default values for map_polygons and other bits of code
    """
    __slots__ = ("radial", "shape", "shape_files_path", "log_files_path", \
                 "kml_files_path", "metadata_path", "geojson_path", \
                 "csv_files_path", "images_path", "sql_files_path", \
                 "spatialite_path", "vrt_files_path", "weight", "ogr2ogr", \
                 "spatialite", "extn", "slash")

    def __init__(self):
        self.radial = 57
        self.shape = 'hex'
        self.shape_files_path = 'shapefiles'
        self.log_files_path = 'logfiles'
        self.kml_files_path = 'kmlfiles'
        self.metadata_path = 'metadata'
        self.geojson_path = 'geojson'
        self.csv_files_path = 'csv'
        self.images_path = 'images'
        self.sql_files_path = 'sql'
        self.spatialite_path = 'spatialite_db'
        self.vrt_files_path = 'vrt'
        self.weight = "place"
        my_os = str(os.name)

        self.ogr2ogr = self.os_ogr2ogr(my_os) # '/usr/bin/ogr2ogr'
        self.slash = self.os_slash(my_os) # '/'
        self.extn = self.os_extn(my_os)
        self.spatialite = self.os_spatialite(my_os)
        self.os_extn(my_os)

    def os_ogr2ogr(self, my_os):
        """
        OS Specific values for ogr2ogr command line utility
        """
        posixvars = OSVars.Posix()
        ntvars = OSVars.NTWindows()
        if my_os == 'posix':
            ogr2ogr = posixvars.ogr2ogr # '/usr/bin/ogr2ogr'
        else:
            ogr2ogr = ntvars.ogr2ogr # 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
        return ogr2ogr

    def os_slash(self, my_os):
        """
        OS Specific values for slash character
        """
        posixvars = OSVars.Posix()
        ntvars = OSVars.NTWindows()
        if my_os == 'posix':
            slash = posixvars.slash  #  '/'
        else:
            slash = ntvars.slash # '\\'
        return slash

    def os_gdal_vars(self, my_os):
        """
        OS Specific values for gdal file directory tree
        """
        ntvars = OSVars.NTWindows()
        if my_os == 'nt':
            gdal_vars = {'GDAL_DATA': 'C:\OSGeo4W64\share\gdal'}
            os.environ.update(gdal_vars)

    def os_extn(self, my_os):
        """
        OS Specific values for sqlite3 extension for Spatialite
        """
        posixvars = OSVars.Posix()
        ntvars = OSVars.NTWindows()
        if my_os == 'posix':
            extn = "SELECT load_extension('mod_spatialite.so');"
        else:
            extn = "SELECT load_extension('mod_spatialite.dll');"
        return extn

    def os_spatialite(self, my_os):
        """
        OS Specific values for spat
        """
        posixvars = OSVars.Posix()
        ntvars = OSVars.NTWindows()
        if my_os == 'posix':
            spatialite = posixvars.spatialite
        else:
            spatialite = ntvars.spatialite
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
        __slots__ = ("epsg", "name", "perimeter", "inv_flat")
        def __init__(self):
            self.epsg = '4326'
            self.name = 'WGS 84'
            self.perimeter = 6378137
            self.inv_flat = 298.257223563

    class GDA94:
        """
        GDA 94 Projection
        Geocentric Datum of Australia 1994
        """
        __slots__ = ("epsg", "name", "perimeter", "inv_flat")
        def __init__(self):
            self.epsg = '4283'
            self.name = 'GDA 84'
            self.perimeter = 6378137
            self.inv_flat = 298.257222101

    class GDA2020:
        """
        GDA 94 Projection
        Geocentric Datum of Australia 1994
        """
        __slots__ = ("epsg", "name", "perimeter", "inv_flat")
        def __init__(self):
            self.epsg = '7844'
            self.name = 'GDA 2020'
            self.perimeter = 6378137
            self.inv_flat = 298.257222101

class BoundingBox:
    """
    Parameters for request to create tessilating shapes
    """
    class Australia:
        """
        Bounding box for Australia
        """
        __slots__ = ("north", "south", "east", "west")

        def __init__(self):
            """
            Init
            """
            self.north = -7
            self.south = -45
            self.east = 170
            self.west = 96

class Offsets:
    """
    Offset ratios for underlying points grid
    """
    __slots__ = ("short", "long")
    def __init__(self):
        self.short = 0.7071
        self.long = 1

class OSVars:
    """
    Operating System Dependant values for 'posix' and 'nt'
    """

    class Posix:
        """
        Posix (Mac OS, Linux) OS values
        """
        __slots__ = ("slash", "ogr2ogr", "spatialite")
        def __init__(self):
            self.slash = '/'
            self.ogr2ogr = '/usr/bin/ogr2ogr'
            self.spatialite = 'spatialite'


    class NTWindows:
        """
        NT (Windows) Operating System values
        """
        __slots__ = ("slash", "ogr2ogr", "spatialite")
        def __init__(self):
            self.slash = '\\'
            self.ogr2ogr = 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
            self.spatialite = 'c:\\OSGeo4W64\\bin\\sqlite3.exe'
