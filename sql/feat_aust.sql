SELECT 
 'P' as Feat_Type,
'SA1_2016' as Feat_Src,
Feat.SA1_MAIN16 as Feat_Code,
'' as Feat_Name,
Shapes.p as Poly,  
(ST_Area(ST_Intersection(Feat.geometry,Shapes.geometry))*12391.3)/(st_area(Feat.geometry)*12391.3) as Feat_Prop, 
(ST_Area(ST_Intersection(Feat.geometry,Shapes.geometry))*12391.3)/(st_area(Shapes.geometry)*12391.3) as Shp_Prop, 
st_area(Shapes.geometry)*12391.3 as Shp_Area, 
ST_Intersection(Feat.geometry,Shapes.geometry) 
FROM Feat,Shapes 
WHERE ST_Intersection(Feat.geometry,Shapes.geometry) or 
ST_Intersects(Feat.geometry,Shapes.geometry) or 
ST_Contains(Feat.geometry,Shapes.geometry) or 
ST_Intersects(Feat.geometry,Shapes.geometry) or 
ST_Within(ST_Centroid(Feat.geometry),Shapes.geometry) or 
ST_Crosses(Feat.geometry,Shapes.geometry)
