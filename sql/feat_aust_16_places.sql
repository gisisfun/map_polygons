SELECT Feat_Aust_16.Poly as Poly,
Feat_Aust_16.Feat_Code as Feat_Code,
Feat_Aust_16.Feat_Prop as Feat_PropA,
Count(*) as places,
Feat_Aust_16.geometry
FROM Feat_Aust_16 
LEFT JOIN Place
ON ST_Within(Place.geometry,Feat_Aust_16.geometry) 
GROUP BY Poly,Feat_Code
