
import urllib.request
from pyunpack import Archive
import subprocess

from isotiles.parameters import Bounding_Box, OSVars, Offsets, DataSets, Defaults

class Util():

    defaults = Defaults()

    def __init__(self,radial: Defaults = defaults.Radial,
                 shape: Defaults = defaults.Shape,
                 images: Defaults = defaults.ImagesPath,
                 metadata: Defaults = defaults.MetaDataPath,
                 tabfiles: Defaults = defaults.TabfilesPath,
                 shapefiles: Defaults = defaults.ShapefilesPath,
                 geojson: Defaults = defaults.GeoJSONPath,
                 vrt: Defaults = defaults.VRTPath,
                 csv: Defaults = defaults.CSVPath,
                 spatialite: Defaults = defaults.SpatialitePath,
                 sql: Defaults = defaults.SQLPath):
        posixvars = OSVars.posix()
        ntvars = OSVars.nt()
        os.environ['SPATIALITE_SECURITY'] = 'relaxed'
        self.Radial = radial
        self.Shape = shape
        self.Charset = 'CP1252'

        self.SpatialitePath = spatialite
        self.SQLPath = sql
        self.ImagesPath = images
        self.MetaDataPath = metadata
        self.TabfilesPath= tabfiles
        self.ShapefilesPath = shapefiles
        self.GeoJSONPath = geojson
        self.VRTPath = vrt
        self.CSVPath = csv 
        self.SpatialitePath = spatialite
        self.SQLPath = sql
        
        my_os = str(os.name)
        if (my_os is 'posix'):
            self.Ogr2ogr = posixvars.Ogr2ogr # '/usr/bin/ogr2ogr'
            self.Slash = posixvars.Slash # '/'
            self.Extn = "SELECT load_extension('mod_spatialite.so');"
            self.Spatialite = posixvars.Spatialite
        else:
            self.Ogr2ogr = ntvars.Ogr2ogr # 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
            self.Slash = ntvars.Slash # '\\'
            Gdal_vars = {'GDAL_DATA': 'C:\OSGeo4W64\share\gdal'}
            os.environ.update(Gdal_vars)
            self.Extn = "SELECT load_extension('mod_spatialite.dll');"
            self.Spatialite = ntvars.Spatialite

        
    def file_deploy(self,RData):
        """
        Deploy downloaded files
        
        Prerequisites:
        ref_files
        
        Input variables:
        """
        if not os.path.isfile(RData.FilePath.format(slash = self.Slash)):
            print('Downloading {descr} file in {fmt} file format'\
                  .format(fmt = RData.Format, descr = RData.Description))
            if RData.DownURL is not '':
                urllib.request.urlretrieve(RData.DownURL, RData.ZipPath.format(slash = self.Slash))
                print('Unzipping {descr} file in {fmt} file format'\
                      .format(descr = RData.Description, fmt = RData.Format ))
                Archive(RData.ZipPath.format(slash = self.Slash)).extractall(RData.ZipDir\
                                                                             .format(slash = self.Slash))
        else:
            print('{descr} file in {fmt} file format exists'\
                  .format(descr = RData.Description, fmt = RData.Format))

    def ref_files_polygons(self):
        """
        Get reference files
        Prerequisites:
        
        Input variables:
        """
        RefData = DataSets.Australia.ShapeFormat()
        self.file_deploy(RefData)


    def ref_files_poly_wt(self):
        """
        Get reference files
        Prerequisites:
        
        Input variables:
        """
        RefData = DataSets.Australia.ShapeFormat()
        self.file_deploy(RefData)

        RefData = DataSets.Australia.TabFormat()
        self.file_deploy(RefData)

        RefData = DataSets.Statistical_Areas_Level_1_2011.ShapeFormat()
        self.file_deploy(RefData)

        RefData = DataSets.Statistical_Areas_Level_1_2016.ShapeFormat()
        self.file_deploy(RefData)

        RefData = DataSets.AGIL_Dataset.CSVFormat()
        self.file_deploy(RefData)

        RefData = DataSets.OpenStreetMaps.ShapeFormat()
        self.file_deploy(RefData)
