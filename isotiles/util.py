
import urllib.request
from pyunpack import Archive

from isotiles.parameters import Bounding_Box, OSVars, Offsets, Defaults
from isotiles.data import DataSets

class Util():

    defaults = Defaults()

    def __init__(self,radial: Defaults = defaults.Radial,
                 shape: Defaults = defaults.Shape,
                 images: Defaults = defaults.ImagesPath,
                 metadata: Defaults = defaults.MetaDataPath,
                 logfiles: Defaults = defaults.LogfilesPath,
                 kmlfiles: Defaults = defaults.KMLfilesPath,
                 shapefiles: Defaults = defaults.ShapefilesPath,
                 geojson: Defaults = defaults.GeoJSONPath,
                 vrt: Defaults = defaults.VRTPath,
                 csv: Defaults = defaults.CSVPath,
                 spatialite: Defaults = defaults.SpatialitePath,
                 sql: Defaults = defaults.SQLPath,
		 slash: Defaults = defaults.Slash,
		 ogr2ogr: Defaults = defaults.Ogr2ogr,
		 spatialite: Defaults = defaults.Spatialite,
		 extn: Defaults = defaults.Extn):

        os.environ['SPATIALITE_SECURITY'] = 'relaxed'
        self.Radial = radial
        self.Shape = shape
        self.Charset = 'CP1252'

        self.SpatialitePath = spatialite
        self.SQLPath = sql
        self.ImagesPath = images
        self.MetaDataPath = metadata
        self.LogfilesPath = logfiles
        self.KMLfilesPath= kmlfiles
        self.ShapefilesPath = shapefiles
        self.GeoJSONPath = geojson
        self.VRTPath = vrt
        self.CSVPath = csv 
        self.SpatialitePath = spatialite
        self.SQLPath = sql
		self.Slash = slash
		self.Ogr2ogr = ogr2ogr
		self.Spatialite = spatialite
		self.Extn = extn
        
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
