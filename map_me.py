import geopandas as gpd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import sys
import os

def map_data(shape,size):
   my_os=os.name
   if (my_os is 'posix'):
        cmd_text='/usr/bin/ogr2ogr'
        slash='/'
   else:
        cmd_text='c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
        slash='\\'
        gdal_vars = {'GDAL_DATA': 'C:\OSGeo4W64\share\gdal'}
        os.environ.update(gdal_vars)

        
   shp_path = "shapefiles{slash}{shape}_{size}km_place_11_16.shp".format(shape=shape,slash=slash,size=size)
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
   print('hello')
   plt.savefig('images{slash}rel_need_for_assistance.png'.format(slash=slash),bbox_inches='tight')
   #plt.show()  

print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) is 1:
    (shape, size) = ['hex',57]
    map_data(shape, size)
else:
    if (len(sys.argv) <3 ):
        sys.exit("arguments are \nshape - hex or box \n size (in km) \n \npython3 map_me.py hex 57\n")
    else:
        (blah,shape,size) = sys.argv
        map_data(shape, size)
    



