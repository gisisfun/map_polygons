
#This code finds and adds neighbors as new field value joined by comma.

import geopandas as gp

file= "/home/pi/Downloads/map_polygons-master/shapefiles/CED_2016_AUST.shp"    

df = gp.read_file(file) # open file
df["NEIGHBORS"] = None  # add NEIGHBORS column
df=  df[~df["CED_NAME16"].str.contains('address', na=False)]
df=  df[~df["CED_NAME16"].str.contains('Migratory', na=False)]
##print(df["CED_NAME16"])
for index, country in df.iterrows():   
    # get 'not disjoint' countries
     
    neighbors = df[~df.geometry.disjoint(country.geometry)].CED_NAME16.tolist()
    # remove own name from the list
    neighbors = [ name for name in neighbors if country.CED_NAME16 != name ]
    # add names of neighbors as NEIGHBORS value
    df.at[index, "NEIGHBORS"] = ", ".join(neighbors)

# save GeoDataFrame as a new file
df.to_file("/home/pi/Downloads/map_polygons-master/shapefiles/new_ced.shp")
