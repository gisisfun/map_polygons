SELECT shapes.*, st_area(shapes.geometry)*12391.3 as area, shapes.geometry FROM shapes, aust WHERE ST_Intersects(shapes.geometry,aust.geometry)
