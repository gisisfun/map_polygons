SELECT 
 'R' as Feat_Type,
'SA1_2011' as Feat_Src,
CAST(SA1_11.SA1_7DIG11 AS INT) as Feat_Code,
'' as Feat_Name,
Shape_Aust.p as Poly,  
(ST_Area(ST_Intersection(SA1_11.geometry,Shape_Aust.geometry))*12391.3)/(st_area(SA1_11.geometry)*12391.3) as Feat_Prop,  
ST_Intersection(SA1_11.geometry,Shape_Aust.geometry) 
FROM SA1_11,Shape_Aust 
WHERE ST_Intersects(SA1_11.geometry,Shape_Aust.geometry) 
and Feat_Prop is not NULL
ORDER by Feat_Code
