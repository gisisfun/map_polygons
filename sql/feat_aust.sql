SELECT 
 'R' as Feat_Type,
'SA1_2011' as Feat_Src,
Feat.SA1_7DIG11 as Feat_Code,
'' as Feat_Name,
Aust.p as Poly,  
(ST_Area(ST_Intersection(Feat.geometry,Aust.geometry))*12391.3)/(st_area(Feat.geometry)*12391.3) as Feat_Prop,  
ST_Intersection(Feat.geometry,Aust.geometry) 
FROM Feat,Aust 
WHERE ST_Intersects(Feat.geometry,Aust.geometry) 
and Feat_Prop is not NULL
ORDER by Feat_Code
