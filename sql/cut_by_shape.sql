SELECT ref_g.SA1_MAIN16, 
shapes.p,  
(ST_Area(ST_Intersection(ref_g.geometry,shapes.geometry))*12391.3)/(st_area(ref_g.geometry)*12391.3) as ref_prop, 
st_area(shapes.geometry)*12391.3 as shp_area, 
'SA1_2016',
ST_Intersection(ref_g.geometry,shapes.geometry) 
FROM ref_g,shapes 
WHERE ST_Intersection(ref_g.geometry,shapes.geometry) or 
ST_Intersects(ref_g.geometry,shapes.geometry) or 
ST_Contains(ref_g.geometry,shapes.geometry) or 
ST_Intersects(ref_g.geometry,shapes.geometry) or 
ST_Within(ST_Centroid(ref_g.geometry),shapes.geometry) or 
ST_Crosses(ref_g.geometry,shapes.geometry)
