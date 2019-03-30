import geopandas as gpd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

shp_path = "shapefiles/shape_57km_place_11_16.shp"
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
plt.savefig('images/rel_need_for_assistance.png',bbox_inches='tight')
plt.show()  



