SELECT Feat_Aust_11.Poly as Poly,
Feat_Aust_11.Feat_Code as Feat_Code,
Feat_Aust_11.Feat_Prop as Feat_PropA,
Count(*) as places,
Feat_Aust_11.geometry
FROM Feat_Aust_11 
LEFT JOIN Place
ON ST_Within(Place.geometry,Feat_Aust_11.geometry) 
GROUP BY Poly,Feat_Code
