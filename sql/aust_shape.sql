SELECT Shapes.*, st_area(Shapes.geometry)*12391.3 as area, Shapes.geometry FROM Shapes, Aust WHERE ST_Intersects(Shapes.geometry,Aust.geometry)
