SELECT 
 'R' as Feat_Type,
'SA1_2016' as Feat_Src,
CAST(SA1_16.SA1_7DIG16 AS INT) as Feat_Code,
'' as Feat_Name,
Shape_Aust.p as Poly,  
(ST_Area(ST_Intersection(SA1_16.geometry,Shape_Aust.geometry))*12391.3)/(ST_Area(SA1_16.geometry)*12391.3) as Feat_Prop,  
ST_Intersection(SA1_16.geometry,Shape_Aust.geometry) 
FROM SA1_16,Shape_Aust 
WHERE ST_Intersects(SA1_16.geometry,Shape_Aust.geometry) 
and Feat_Prop is not NULL
ORDER by Feat_Code
