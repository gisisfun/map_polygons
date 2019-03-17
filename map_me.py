import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

shp_path = "Downloads/map_polygons-master/shapefiles/shape_57km_place_11_16.shp"
sf = gpd.read_file(shp_path)
print(len(sf))
#sf.plot()
#ax.set_title("Hexagons. Default view)");
sf['rel_need_for_assistance'] = ((sf.NeedA16-sf.NeedA11)/(sf.NeedAT16-sf.NeedAT11))*1
sf = sf.fillna(9999)
sf = sf[(sf.rel_need_for_assistance!=9999)]
sf = sf.sort_values(['rel_need_for_assistance'], ascending = [1])
sf=sf[sf.replace([np.inf, -np.inf], np.nan).notnull().all(axis=1)]  # .astype(np.float64)
print(sf['rel_need_for_assistance'])
#sf.plot(column='NeedA16').set_title("Hexagons. Default view");
sf.plot(column='rel_need_for_assistance').set_title("Hexagons. Default view");
plt.show()