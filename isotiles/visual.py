"""
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import geopandas as gpd
from isotiles.__init__ import Defaults # OSVars,
#Visual


mpl.use('Agg')



class Visual:
    """
    """
    defaults = Defaults()
    def __init__(self,\
                 radial: Defaults = defaults.radial,
                 shape: Defaults = defaults.shape,
                 weight: Defaults = defaults.weight,
                 images: Defaults = defaults.images_path,
                 shapefiles: Defaults = defaults.shape_files_path,
                 slash: Defaults = defaults.slash):
        #posixvars = OSVars.posix()
        #ntvars = OSVars.nt()
        self.images_path = images
        self.shape = shape
        self.radial = radial
        self.weight = weight
        self.shape_files_path = shapefiles
        self.slash = slash

    def map_data(self):
        """
        """
        shp_path = "{shapePath}{slash}{shape}_{size}km_{weight}_11_16.shp".\
                   format(slash=self.slash,\
                          shapePath=self.shape_files_path,\
                          shape=self.shape,\
                          size=self.radial,\
                          weight=self.weight)

        shape_file = gpd.read_file(shp_path)
        shape_file['rel_need_for_assistance'] = \
        ((shape_file.NeedA16-shape_file.NeedA11)/(shape_file.NeedAT16-\
         shape_file.NeedAT11))*1
        shape_file = shape_file.fillna(9999)
        shape_file = shape_file[(shape_file.rel_need_for_assistance != 9999)]
        shape_file = shape_file.sort_values(['rel_need_for_assistance'], \
                                            ascending=[1])
        shape_file = shape_file[shape_file.replace([np.inf, -np.inf], \
                                                   np.nan).notnull().\
                     all(axis=1)]  # .astype(np.float64)
        plt.rcParams["figure.figsize"] = (10, 6)
        the_title = """2016 to 2011 Relative Change in Need For Assistance \
(Quantiles) for Statistical Area Level 1\n{weight} Weighted {shape} {size}km""".\
        format(weight=self.weight.title(),\
               shape=self.shape,
               size=self.radial)
        shape_file.plot(column='rel_need_for_assistance', scheme='quantiles', \
                k=5, linewidth=0, cmap='Reds', legend=True).\
                set_title(the_title)
        plt.annotate("""Source: ABS Census of Population and Housing, 2016 \
and 2011""", xy=(0.1, .08), xycoords='figure fraction', \
                     horizontalalignment='left', verticalalignment='top', \
                     fontsize=12, color='#555555')
        plt.axis('off')

        plt.savefig("""{imagePath}{slash}{shape}_{size}km_rel_need_for_assistance_by_{weight}_\
weight.png""".\
                    format(shape=self.shape, slash=self.slash, size=self.radial,\
                           imagePath=self.images_path, weight=self.weight),\
                    bbox_inches='tight')
        #plt.show() #
