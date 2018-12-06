SELECT poly.SA1_MAIN16, 
shapes.p,  
(ST_Area(ST_Intersection(poly.geometry,shapes.geometry))*12391.3)/(st_area(poly.geometry)*12391.3) as ref_prop, 
st_area(shapes.geometry)*12391.3 as shp_area, 
'SA1_2016',
ST_Intersection(poly.geometry,shapes.geometry) 
FROM poly,shapes 
WHERE ST_Intersection(poly.geometry,shapes.geometry) or 
ST_Intersects(poly.geometry,shapes.geometry) or 
ST_Contains(poly.geometry,shapes.geometry) or 
ST_Intersects(poly.geometry,shapes.geometry) or 
ST_Within(ST_Centroid(poly.geometry),shapes.geometry) or 
ST_Crosses(poly.geometry,shapes.geometry)
