#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 16:17:33 2020

@author: damienclarke
"""
# https://stackoverflow.com/questions/38253948/geopandas-plots-as-subfigures
import pandas as pd
import geopandas
from geopandas import GeoDataFrame as gdf
from shapely.geometry import Point
#import geoplot
import os
import matplotlib.pyplot as plt
import zipfile
from datetime import datetime
#import urllib2




def narrow(file_name,col_name):
            
    file_path = ['COVID-19',
                 'csse_covid_19_data',
                 'csse_covid_19_time_series',
                 file_name]
    cv_df = pd.read_csv(os.path.join(*file_path))

    idvars = ['Province/State','Country/Region','Lat','Long']
    narrow_df = pd.melt(cv_df,id_vars=idvars,var_name='date',
                        value_name=col_name)

    #fix formatting of date column
    narrow_df.date = pd.to_datetime(narrow_df.date)
    return narrow_df


aust = geopandas.read_file('STE_2016_AUST.shp')

narrow_conf_df = narrow('time_series_covid19_confirmed_global.csv','confirmed')
narrow_death_df = narrow('time_series_covid19_deaths_global.csv','death')
narrow_recovery_df = narrow('time_series_covid19_recovered_global.csv','recovery')
#split out data set for australia
aust_conf_cv = narrow_conf_df.set_index(narrow_conf_df['Country/Region']).\
    loc['Australia',]

aust_death_cv = narrow_death_df.set_index(narrow_death_df['Country/Region']).\
    loc['Australia',]

aust_recovery_cv = narrow_recovery_df.set_index(narrow_recovery_df['Country/Region']).\
    loc['Australia',]

# charts
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True, sharey=False)
aust_conf_cv.groupby('date')['confirmed'].sum().plot(ax=ax1, title="Confirmed")
aust_death_cv.groupby('date')['death'].sum().plot(ax=ax2, title="Deaths")
aust_recovery_cv.groupby('date')['recovery'].sum().plot(ax=ax3, title="Recovery")

#choose most recent date 
end_date = datetime.strftime(narrow_conf_df.date.max(),"%m/%d/%Y")
date_conf_df = narrow_conf_df.loc[narrow_conf_df['date']==end_date,]
#
# Datad=Frame as GeoDataFrame
points_list = [Point(x, y) for x, y in zip(date_conf_df.Long, date_conf_df.Lat)]
points = gdf(date_conf_df, geometry=points_list)
points.crs = {'init' :'epsg:4326'}
points = points.to_crs({'init': 'epsg:4283'})

# join points data to australia by location
m_layer = geopandas.sjoin(aust, points, how="inner", op='intersects')

#make the map
m_layer.plot(column='confirmed', cmap='Blues', linewidth=0.8, edgecolor='0.8',
             label="confirmed")
vmin = m_layer['confirmed'].min()
vmax = m_layer['confirmed'].max()
sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, 
                                                            vmax=vmax))

# Chlorepleth : 
# empty array for the data range
sm._A = []
# add the colorbar to the figure
cbar = plt.colorbar(sm)
plt.axis("off")
# points.plot(marker='o', markersize=5);
plt.title('Figures as of ' + end_date)

plt.savefig('map.png')
plt.show()



# =============================================================================
# def download(url,directory,name):
#  webfile = urllib2.urlopen('http://www.sec.gov'+url)
#  webfile2 = zipfile.ZipFile(webfile)
#  content = zipfile.ZipFile.open(webfile2).read()
#  localfile = open(directory+name, 'w')
#  localfile.write(content)
#  localfile.close()
#  return()
# link = 'https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_ste_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&65819049BE2EB089CA257FED0013E865&0&July%202016&12.07.2016&Latest'
# 
# download(link,'./fails_data', link.text)
# =============================================================================

# =============================================================================
#p1 = geometry.Polygon([(0,0),(0,1),(1,1),(1,0)])
#p2 = geometry.Polygon([(3,3),(3,6),(6,6),(6,3)])
#p3 = geometry.Polygon([(3,.5),(4,2),(5,.5)])
#
#gdf = geopandas.GeoDataFrame(dict(
#        geometry=[p1, p2, p3],
#        Value1=[1, 10, 20],
#        Value2=[300, 200, 100],
#))
#
#fig, (ax1, ax2) = pyplot.subplots(ncols=2, sharex=True, sharey=True)
#gdf.plot(ax=ax1, column='Value1')
#gdf.plot(ax=ax2, column='Value2')
# =============================================================================
