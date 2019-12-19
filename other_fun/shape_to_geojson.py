import shapefile

class test():
    def me(self):
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
        [column_list.append(x[0]) for x in fields[1:]]

        # data values with null geography
        tab_data = sf.records()

        tab_data_val = []
        row_ref = []
        i = 0
        for tab_row in range(len(shapes_list_no_null)): # all rows
            #for column_name in column_list:
            row_data = [] #shapes_list_no_null[tab_row][0]]
            
            for tab_val in tab_data[shapes_list_no_null[tab_row][0]]: # each row of tab data (y)
                row_ref.append(i)
                row_data.append(tab_val) #,len(shapes[tab_row].points)])
                #column_dict[column_name] = str(tab_col)
            i += 1 
            tab_data_val.append(row_data) # column_dict)
    
        geojson_properties_list = []
        for tab_row in tab_data_val:
            dataset_dict_row = {}
            for i in range(0,len(column_list)):
                #print(i)
                dataset_dict_row[column_list[i]] = tab_row[i]
            geojson_properties_list.append(dataset_dict_row)
    
        # make a parts list find numbers of points
        parts_list = []
        parts_count = []
        points_len = []
        for i  in range(len(tab_data_val)):
            the_list = shapes[row_ref[i]].parts
            parts_list.append(the_list)
            the_list = shapes[row_ref[i]].parts
            parts_count.append(len(shapes[row_ref[i]].parts))
            points_len.append(len(shapes[row_ref[i]].points))
                
        thing = []          
        for i in range(len(geojson_properties_list)):
            parts_list[i].append(points_len[i])
            shapes_ref = row_ref[i]
            #thing.append([geojson_properties_list[i],parts_count[i],parts_list[i]])
            
            for j in range(0,parts_count[i]):
                geojson_polygon = {}
                
                geopoly = Polygon([shapes[shapes_ref].points[parts_list[i][j]:parts_list[i][j+1]]])
                geopoly= Feature(geometry = geopoly, properties = geojson_properties_list[i])
                
                g_array.append(geopoly)
        return g_array
            
            
testing = test()
fred = testing.me()
