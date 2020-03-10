
"""
isotiles - Supporting functions for map_polygons code base

isotiles has four libraries

parameters - library containing definitions variables used in tiles, postprocess and visual library functions. 
tiles - used for polygons.py code.
postprocess - used for  poly_wt.py code.
visual - used for map_me.py code.
"""
"""
Parameters for map_polygons
"""

import os

class Defaults:
    """
    Default values for map_polygons and other bits of code
    """
    __slots__ = ("radial", "shape")

    def __init__(self):
        self.radial = 57
        self.shape = 'hex'

    @property
    def kml_files_path(self):
        """
        Path to GeoJSON files
        """
        return 'files/kmlfiles'

    @property
    def json_files_path(self):
        """
        Path to JSON files
        """
        return 'files/jsonfiles'

    @property
    def geojson_path(self):
        """
        Path to GeoJSON files
        """
        return 'files/geojson'

    @property
    def csv_files_path(self):
        """
        Path to images files
        """
        return 'files/csv'

    @property
    def images_path(self):
        """
        Path to images files
        """
        return 'files/images'

    @property
    def sql_files_path(self):
        """
        Path to SQL files
        """
        return 'sql'

    @property
    def spatialite_path(self):
        """
        Path to spatialite files
        """
        return 'spatialite_db'

    @property
    def vrt_files_path(self):
        """
        Path to Virtual File Template (VRT) files
        """
        return 'files/vrt'

    @property
    def shape_files_path(self):
        """
        Long interval to next reference point
        """
        return 'files/shapefiles'


    @property
    def ogr2ogr(self):
        """
        OS dependant path to ogr2ogr excutable file.
        """
        my_os = str(os.name)
        os_dict = {"posix":{"ogr2ogr": '/usr/bin/ogr2ogr'},\
                    "nt":{"ogr2ogr": 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'}}
        return os_dict[my_os]['ogr2ogr'] # '/usr/bin/ogr2ogr'

    @property
    def slash(self):
        """
        OS dependant path slash character.
        """
        my_os = str(os.name)
        os_dict = {"posix":{"slash": "/"}, "nt":{"slash": '\\'}}
        return os_dict[my_os]['slash'] # '/'

    @property
    def extn(self):
        """
        OS dependant filename of mod_spatialite library file.
        """
        my_os = str(os.name)
        os_dict = {"posix":{"extn": 'mod_spatialite.so'},\
                    "nt":{"extn": 'mod_spatialite.dll'}}
        return os_dict[my_os]['extn']

    @property
    def spatialite(self):
        """
        OS dependant filename of spatialite excutable file.
        """
        my_os = str(os.name)
        os_dict = {"posix":{"spatialite": 'spatialite'},\
                    "nt":{"spatialite": 'c:\\OSGeo4W64\\bin\\sqlite3.exe'}}
        return os_dict[my_os]['spatialite']

    @property
    def proj_dict(self):
        """
        Projection values
        """
        proj_dict = {"Projection":{"WGS84":{{"epsg": '4326',"elipsoid": 'WGS 1984', "name": 'WGS 84', \
                                            "perimeter": 6378137, \
                                            "inv_flat": 298.257223563},\
                                    "GDA94":{"epsg": '4283',"elipsoid": 'GRS 1980',  "name": 'GDA 94', \
                                             "perimeter": 6378137, \
                                             "inv_flat": 298.257222101},\
                                    "GDA2020":{"epsg": '7844',"elipsoid": 'GRS 1980',"epsg": '7844', \
                                               "name": 'GDA 2020', \
                                               "perimeter": 6378137, \
                                               "inv_flat": 298.257222101}}}
        return proj_dict

    @property
    def weight(self):
        """
        Weighting Factor
        """
        return 'Place'

    @property
    def north(self):
        """
        North Bounding value of bounding box
        """
        return -7

    @property
    def south(self):
        """
        South Bounding value of bounding box
        """
        return -45

    @property
    def east(self):
        """
        East Bounding value of bounding box
        """
        return 169

    @property
    def west(self):
        """
        West Bounding value of bounding box
        """
        return 96

