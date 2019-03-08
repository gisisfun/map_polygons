SELECT Shape.*,
st_area(Shape.geometry)*12391.3 as area,
Shape.geometry 
FROM Shape, Aust 
WHERE 
ST_Intersects(Shape.geometry,Aust.geometry)
