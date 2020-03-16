#This code finds and adds neighbors as new field value joined by comma.
import pandas as pd
import geopandas as gp

file= "/home/pi/Documents/map_polygons/shapefiles/LGA_2019_AUST.shp"    

df = gp.read_file(file) # open file
df["NEIGHBOURS_CODE"] = None  # add NEIGHBORS column
df["NEIGHBOURS_NAME"] = None  # add NEIGHBORS column
df=  df[~df["LGA_NAME19"].str.contains('address', na=False)]
df=  df[~df["LGA_NAME19"].str.contains('Migratory', na=False)]
print(df["LGA_NAME19"])
for index, boundary in df.iterrows():   
    # get 'not disjoint' countries
     
    neighbours_name = df[~df.geometry.disjoint(boundary.geometry)].LGA_NAME19.tolist()
    neighbours_code = df[~df.geometry.disjoint(boundary.geometry)].LGA_CODE19.tolist()
    # remove own name from the list
    neighbours_name = [ name for name in neighbours_name if boundary.LGA_NAME19 != name ]
    neighbours_code = [ code for code in neighbours_code if boundary.LGA_CODE19 != code ]
    # add names of neighbors as NEIGHBOURS value
    df.at[index, "NEIGHBOURS_NAME"] = ", ".join(neighbours_name)
    df.at[index, "NEIGHBOURS_CODE"] = ", ".join(neighbours_code)



# save GeoDataFrame as a new shp file
df.to_file("/home/pi/Documents/map_polygons/shapefiles/new_LGA_2019_AUST.shp")

# save DataFrame as a new csv file
df.to_csv("/home/pi/Documents/map_polygons/new_LGA_2019_AUST.csv", header = True, index= False, columns= ['LGA_NAME19','LGA_CODE19','NEIGHBOURS_CODE','NEIGHBOURS_NAME'])

# stack output
new_df = pd.DataFrame([])
for i, row in df.iterrows():
    for neigbour_name in iter(row.NEIGHBOURS_NAME.split(',')):
        print(row.LGA_CODE19, row.LGA_NAME19, neigbour_name.strip())
        new_df = new_df.append({'LGA_CODE19': row.LGA_CODE19, 'LGA_NAME19': row.LGA_NAME19,"NEIGHBOUR": neigbour_name.strip()}, ignore_index=True)

#print(new_df)

# save stacked DataFrame as a new csv file
new_df.to_csv("/home/pi/Documents/map_polygons/stacked_LGA_2019_AUST.csv", header = True, index= False)
