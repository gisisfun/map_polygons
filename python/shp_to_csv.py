import ogr
import csv
import sys
import pandas as pd
#source: https://gis.stackexchange.com/questions/19163/convert-shapefile-to-csv-including-attributes-and-geometry
shpfile=r'cut_sa1.shp' #sys.argv[1]
csvfile=r'cut_sa1.csv' #sys.argv[2]

#Open files
ds=ogr.Open(shpfile)
lyr=ds.GetLayer()

#Get field names
dfn=lyr.GetLayerDefn()
nfields=dfn.GetFieldCount()
fields = []
tabular_list = []
for i in range(nfields):
    fields.append(dfn.GetFieldDefn(i).GetName())
    print(dfn.GetFieldDefn(i).GetName())


# Write attributes and kml out to csv
for feat in lyr:
    tabular_line = []
    attributes=feat.items()
    for i in range(len(attributes.keys())):
       tabular_line.append(attributes[fields[i]])
    tabular_list.append(tabular_line)

tabular_df = pd.DataFrame(tabular_list) #convert tabular array to tabular data frame
tabular_df.columns = fields
print(tabular_df)
#filtered_df = tabular_df.dropna()
#or
filtered_df = tabular_df[tabular_df['Shp_Prop'].notnull()]
filtered_df.to_csv('{0}'.format(csvfile), sep=',')
#clean up
del lyr,ds

