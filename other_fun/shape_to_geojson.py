import shapefile
class test():
    def me():
        sf = shapefile.Reader("shapefiles/SA3_2016_AUST") # , shapeType=3)
        shapes = sf.shapes()
        print(len(sf))

        #how many empty and real polgons and subpolygons
        shapes_list= []
        [shapes_list.append([len(x.points),len(x.parts)]) for x in shapes]

        # add a row_id
        shapes_list_with_row_id = []
        [shapes_list_with_row_id.append([x,shapes_list[x][0],shapes_list[x][1]]) for x in range(len(shapes_list))]

        # drop all array rows ith 0 parts
        shapes_list_no_null = [a for a in shapes_list_with_row_id if a[2] not in [0]]

        #get the field names
        fields = sf.fields
        column_list = []
        [column_list.append(x[0]) for x in fields]

        # data values with null geography
        tab_data = sf.records()

        tab_data_val = []
        for tab_row in range(len(shapes_list_no_null)): # all rows
            #for column_name in column_list:
            row_data = [0]
            for tab_val in tab_data[shapes_list_no_null[tab_row][0]]: # each row of tab data (y)
                row_data.append(tab_val) #,len(shapes[tab_row].points)])
                #column_dict[column_name] = str(tab_col)
            tab_data_val.append(row_data) # column_dict)
    
        geojson_list = []
        for tab_row in tab_data_val:
            dataset_dict_row = {}
        for i in range(0,len(column_list)):
            #print(i)
            dataset_dict_row[column_list[i]] = tab_row[i]
            geojson_list.append(dataset_dict_row)
    
        # make a parts list find numbers of points
        parts_list = []
        points_len = []
        for geom_data in shapes:
            
            if len(geom_data.parts) > 0:
                parts_list.append(geom_data.parts)
                points_len.append(len(geom_data.points))
                
        return points_len 
            
            
fred = test.me()
print(fred[0])
