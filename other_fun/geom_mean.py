#https://medium.com/@sumit.arora/plotting-weighted-mean-population-centroids-on-a-country-map-22da408c1397

import geopandas as gpd
from shapely.geometry import Point

mb_counts_url = 'https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&2016%20census%20mesh%20block%20counts.csv&2074.0&Data%20Cubes&1DED88080198D6C6CA2581520083D113&0&2016&04.07.2017&Latest'
mb_counts = gpd.pd.read_csv('csv/2016_census_mesh_block_counts.csv')
def mb_aust():
    mbact = gpd.read_file('shape/MB_2016_ACT.shp')
    mbnsw = gpd.read_file('shape/MB_2016_NSW.shp')
    mbnt = gpd.read_file('shape/MB_2016_NT.shp')
    mbot = gpd.read_file('shape/MB_2016_OT.shp')
    mbqld = gpd.read_file('shape/MB_2016_QLD.shp')
    mbsa = gpd.read_file('shape/MB_2016_SA.shp')
    mbtas = gpd.read_file('shape/MB_2016_TAS.shp')
    mbvic = gpd.read_file('shape/MB_2016_VIC.shp')
    mbwa = gpd.read_file('shape/MB_2016_WA.shp')
    gdf = gpd.pd.concat([mbact, mbnsw, mbnt, mbnt, mbot,
                     mbqld, mbsa, mbtas, mbvic, mbwa])
    #gdf.STE_NAME16.astype('category').unique()
    return gdf

mb_data = mb_aust() 


mb_clean = mb_data.loc[mb_data.AREASQKM16!=0,]
mb_clean = mb_clean[['MB_CODE16','geometry']]
geom = gpd.GeoSeries(mb_clean['geometry'])
mb_clean['centroid_x'] = geom.centroid.x
mb_clean['centroid_y'] = geom.centroid.y
mb_clean.reindex()
mb_clean = mb_clean[['MB_CODE16','centroid_x','centroid_y']]
mb_clean.to_csv('new_mb.csv', index=False)

mb_clean['MB_CODE16'] = mb_clean['MB_CODE16'].astype('int64')
new =gpd.pd.merge(mb_clean,mb_counts, left_on='MB_CODE16',right_on='MB_CODE_2016',
             how='left')


#mb_clean.to_file("shape/mb_new_cent.shp")
new = new[['MB_CODE16', 'centroid_x', 'centroid_y', 'AREA_ALBERS_SQKM', \
           'Dwelling', 'Person']]

#geopandas 0.8.0
# geom = gpd.points_from_xy(x=mb_clean.centroid_x, y=mb_clean.centroid_y)


#geopandas 0.4.0

geom = [Point(xy)  for xy in zip(new.centroid_y, new.centroid_x)]

mb_clean_pts_gdf = gpd.GeoDataFrame(new,geometry = geom, crs='EPSG:4283') 

mb_clean_pts_gdf.to_file('shape/mb_mg_cent_pop.shp')           
