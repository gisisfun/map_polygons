#all
import os
import pandas as pd

#Visual
import geopandas as gpd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('Agg')

from isotiles.parameters import Bounding_Box, OSVars, Offsets, DataSets, Defaults

class Visual:
    defaults = Defaults()
    def __init__(self,\
                 radial: Defaults = defaults.Radial,
                 shape: Defaults = defaults.Shape,
                 weight: Defaults = defaults.Weight,
                 images: Defaults = defaults.ImagesPath,
                 shapefiles: Defaults = defaults.ShapefilesPath):
        posixvars = OSVars.posix()
        ntvars = OSVars.nt()
        self.imagesPath = images
        self.Shape = shape
        self.Radial = radial
        self.Weight = weight 
        self.ShapefilesPath = shapefiles
        my_os = str(os.name)
        if (my_os is 'posix'):
            self.Slash = posixvars.Slash # '/'
            
        else:
            self.Slash = ntvars.Slash # '\\'
            Gdal_vars = {'GDAL_DATA': 'C:\OSGeo4W64\share\gdal'}
            os.environ.update(Gdal_vars)
            
    def map_data(self):
        shp_path = "{shapePath}{slash}{shape}_{size}km_{weight}_11_16.shp".\
                   format(slash = self.Slash,\
                          shapePath = self.ShapefilesPath,\
                          shape = self.Shape,\
                          size = self.Radial,\
                          weight = self.Weight)
        
        sf = gpd.read_file(shp_path)
        sf['rel_need_for_assistance'] = ((sf.NeedA16-sf.NeedA11)/(sf.NeedAT16-sf.NeedAT11))*1
        sf = sf.fillna(9999)
        sf = sf[(sf.rel_need_for_assistance!=9999)]
        sf = sf.sort_values(['rel_need_for_assistance'], ascending = [1])
        sf=sf[sf.replace([np.inf, -np.inf], np.nan).notnull().all(axis=1)]  # .astype(np.float64)
        plt.rcParams["figure.figsize"] = (10,6)
        thetitle = "2016 to 2011 Relative Change in Need For Assistance (Quantiles)\n{weight} Weighted".format(weight = self.Weight.title())
        sf.plot(column='rel_need_for_assistance', scheme = 'quantiles', k=5, linewidth=0,cmap='Reds',legend=True).set_title(thetitle) ;
        plt.annotate('Source: ABS Census of Population and Housing, 2016 and 2011',xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')
        plt.axis('off')
        
        
        plt.savefig('{imagePath}{slash}rel_need_for_assistance_by_{weight}_weight.png'.\
                    format(slash = self.Slash,\
                           imagePath = self.imagesPath,\
                           weight = self.Weight),\
                    bbox_inches='tight')
        #plt.show() #    

