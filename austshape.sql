SELECT shapes.*,shapes.geometry FROM shapes, aust WHERE ST_Intersects(shapes.geometry,aust.geometry)