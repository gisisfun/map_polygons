import pandas as pd
import geopandas as gpd

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
    gdf = pd.concat([mbact, mbnsw, mbnt, mbnt, mbot,
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
mb_clean[['MB_CODE16','centroid_x','centroid_y']].to_csv('new_mb.csv', 
        index=False)
