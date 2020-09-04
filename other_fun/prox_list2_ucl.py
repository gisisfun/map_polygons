#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 13:56:51 2020
@author: pi
"""
#import geopandas as gpd
#from shapely.geometry import Point
from geopy.distance import geodesic
import pandas as pd
from sqlalchemy import create_engine, MetaData,Table, select,and_
import geopandas as gpd
from shapely.geometry import Point

import numpy as np

def read_poi(fname,tab=False):
    sep_char=','
    if tab:
        sep_char ='\t'
    df=pd.read_csv(fname,sep=sep_char)
    return df


def closest_addresses_ucl(v_stmt,row,tolerance = 1):
    v_stmt_loop = v_stmt.where(
            and_(v_address_view.columns.Longitude.between(int(row.Longitude)-tolerance,
                                                          int(row.Longitude)+tolerance),
    v_address_view.columns.Latitude.between(int(row.Latitude)-tolerance,
                                            int(row.Latitude)+tolerance)))
    found = False
    print('* query to dataframe *')
    data=[]
    for result in connection.execute(v_stmt_loop):
    
    
    
        distance_km = geodesic((result.Latitude,result.Longitude),
                               (row.Latitude,row.Longitude)).km
                               
        data.append([result.Address_Detail_PID,result.AddressText.strip(),
                     result.Latitude,result.Longitude,
                     row.UCL_CODE_2016,row.UCL_NAME_2016,
                     row.Latitude,row.Longitude, distance_km])
        
    data_df=pd.DataFrame(data,columns=['Address_Detail_PID','AddressText',
                                             'address_latitude','address_longitude',
                                             'UCL_CODE_2016','UCL_NAME_2016',
                                             'locality_latitude',
                                             'locality_longitude','distance_km'])
    return data_df,found


def closest_address_ucl(v_stmt,row,tolerance = 1):

    v_stmt_loop = v_stmt.where(
            and_(v_address_view.columns.Longitude.between(int(row.Longitude)-tolerance,
                                                          int(row.Longitude)+tolerance),
    v_address_view.columns.Latitude.between(int(row.Latitude)-tolerance,
                                            int(row.Latitude)+tolerance)))
    found = False
    small_data = ['0', 0, 0, 0, row.UCL_CODE_2016,\
                row.UCL_NAME_2016,row.Latitude, row.Longitude,0]
    smallest=99999
    for result in connection.execute(v_stmt_loop):
        distance_km=geodesic((result.Latitude,result.Longitude), 
                             (row.Latitude,row.Longitude)).km
        #if distance_km < 60:

        if distance_km < smallest:
            smallest=distance_km
            small_data=[result.Address_Detail_PID,result.AddressText.strip(),
                        result.Latitude,result.Longitude, row.UCL_CODE_2016,
                        row.UCL_NAME_2016,row.Latitude, row.Longitude,
                        distance_km]
            found = True
    return small_data, found


def add_cols_ucl(df,id_col,id_name):
    rafile = gpd.read_file('shape/RA_2016_AUST.shp')
    rafile['RA_NAME16'] = rafile['RA_NAME16'].str.replace('.\(.*\)','')
    rafile = rafile.loc[rafile.geometry!=None,['RA_NAME16','geometry']]
    #geom=[Point(xy) for xy in zip(df.locality_longitude, df.locality_latitude)]
    df_poi_gdf=gpd.GeoDataFrame(df[['Address_Detail_PID',
                                    'locality_latitude', 
                                    'locality_longitude']], 
            geometry = gpd.points_from_xy(df.locality_longitude, 
                                          df.locality_latitude), 
                                          crs = 'EPSG:4283')
    
    df_poi_ra_gdf = gpd.sjoin(df_poi_gdf, rafile, how='left', op='within')
    df_poi_ra = df_poi_ra_gdf.drop(columns=['geometry','index_right','locality_latitude', 'locality_longitude'])
    df_poi_ra.columns = ['Address_Detail_PID', 'locality_longlat_RA16']
    
    #geom=[Point(xy) for xy in zip(df.address_longitude, df.address_latitude)]
    
    df_address_gdf = gpd.GeoDataFrame(df,
                                    geometry = gpd.points_from_xy(df.address_longitude, 
                                                                df.address_latitude),
                                                                crs="EPSG:4283")
    
    df_address_ra_gdf = gpd.sjoin(df_address_gdf, rafile[['RA_NAME16','geometry']][rafile.geometry!=None], how='left', op='within')
    df_address_ra_gdf.rename(columns={'RA_NAME16': 'address_longlat_RA16'}, inplace=True)
    
    df_out = pd.merge(df_address_ra_gdf[['Address_Detail_PID', 'AddressText', 'address_latitude',
           'address_longitude', id_col, id_name,
           'locality_latitude', 'locality_longitude', 'distance_km','address_longlat_RA16']],df_poi_ra,on='Address_Detail_PID')
    df_out['RA16_Diff_Flag'] = df_out['address_longlat_RA16'] != df_out['locality_longlat_RA16']
    df_out['RA16_Diff_Flag'] = df_out.RA16_Diff_Flag.apply(lambda x:int(x))
    df_out= df_out.drop_duplicates(id_col)
    return df_out


def start_engine(dbase):
    engine = create_engine('sqlite:///spatialite_db/'+dbase+'.sqlite')
    #print(engine.table_names())
    connection = engine.connect()
#tables
    metadata = MetaData()
    return engine,metadata,connection

def close_connection(connection):
    connection.close()
    
#ADDRESS_DETAIL ->  ADDRESS_DETAIL_PID (in v_address_view)
#ADDRESS_MESH_BLOCK_2016 -> ADDRESS_MESH_BLOCK_2016_PID,ADDRESS_DETAIL_PID,MB_2016_PID
#MB_2016 -> MB_2016_PID,MB_2016_CODE

print('address view')
engine,metadata,connection = start_engine('gnaf_may_2020_new')
v_address_view= Table('ADDRESS_TBL2',metadata, autoload=True, 
                       autoload_with=engine)
print(v_address_view.columns.keys())



###layers = fiona.listlayers('asgs2011nonabsstructures.gpkg')
###layer = gpd.read_file('asgs2011nonabsstructures.gpkg', layer='local_government_area_2011')
closest=[]
test=read_poi('csv/ucl.txt',tab=True)
df=test[test.Latitude!=0]
v_stmt = select([v_address_view.columns.Address_Detail_PID,
v_address_view.columns.Latitude, v_address_view.columns.Longitude,
 v_address_view.columns.AddressText])
#
for index,row in df.iterrows():
    #limit by bounding box
    tolerance = 1

    while True:
        print('trying tolerance', tolerance,' degree and row \n',row)
        small_data, found = closest_address_ucl(v_stmt,row,tolerance)
        print(index,small_data)
        if found == True:
            break
        else:
            tolerance += 1 
 
    
    closest.append(small_data)



close_connection(connection)
print(closest)

df_closest=pd.DataFrame(closest,columns=['Address_Detail_PID','AddressText',
                                         'address_latitude','address_longitude',
                                         'UCL_CODE_2016','UCL_NAME_2016',
                                         'locality_latitude',
                                         'locality_longitude','distance_km'])
df_closest.to_csv('closest3.csv')
    
    
    
    
df_closest = read_poi('closest3.csv')
df_out = add_cols_ucl(df_closest,'UCL_CODE_2016','UCL_NAME_2016')


