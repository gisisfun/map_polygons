import geopandas as gpd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys

from isotiles.parameters import Bounding_Box, OSVars, Offsets, DataSets, Defaults

class Visual:
   
   defaults = Defaults()
   
   def __init__(self,self,radial: Defaults = defaults.Radial,
                 shape: Defaults = defaults.Shape,
                 images: Defaults = defaults.ImagesPath,
                 tabfiles: Defaults = defaults.TabfilesPath,
                 shapefiles: Defaults = defaults.ShapefilesPath ):
      self.imagesPath = images
              my_os = str(os.name)
      if (my_os is 'posix'):
         self.Ogr2ogr = posixvars.Ogr2ogr # '/usr/bin/ogr2ogr'
         self.Slash = posixvars.Slash # '/'
         self.Extn = "SELECT load_extension('mod_spatialite.so');"
         self.Spatialite = posixvars.Spatialite 
     else
   self.Ogr2ogr = ntvars.Ogr2ogr # 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
            self.Slash = ntvars.Slash # '\\'
            Gdal_vars = {'GDAL_DATA': 'C:\OSGeo4W64\share\gdal'}
            os.environ.update(Gdal_vars)
            self.Extn = "SELECT load_extension('mod_spatialite.dll');"
            self.Spatialite = ntvars.Spatialite
      
   def map_data(shape,size):
      shp_path = "shapefiles/{shape}_{size}km_place_11_16.shp".format(shape=shape,size=size)
      sf = gpd.read_file(shp_path)
      sf['rel_need_for_assistance'] = ((sf.NeedA16-sf.NeedA11)/(sf.NeedAT16-sf.NeedAT11))*1
      sf = sf.fillna(9999)
      sf = sf[(sf.rel_need_for_assistance!=9999)]
      sf = sf.sort_values(['rel_need_for_assistance'], ascending = [1])
      sf=sf[sf.replace([np.inf, -np.inf], np.nan).notnull().all(axis=1)]  # .astype(np.float64)
      plt.rcParams["figure.figsize"] = (10,6)
      sf.plot(column='rel_need_for_assistance', scheme = 'quantiles', k=5, linewidth=0,cmap='Reds',legend=True).set_title("2016 to 2011 Relative Change in Need For Assistance (Quantiles)") ;
      plt.annotate('Source: ABS Census of Population and Housing, 2016 and 2011',xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')
      plt.axis('off')
      plt.show()
      mpl.use('Agg')
      plt.savefig('images/rel_need_for_assistance.png',bbox_inches='tight')
      #    




