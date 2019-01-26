
SELECT Feat_Aust.Poly as Poly,Feat_Aust.Feat_Cide as Feat_Code, Count(*) as Places.places,
Feat_Aust.geometry
FROM Feat_Aust 
INNER JOIN Places
ON ST_Within(Places.geometry,Feat_Aust.geometry) 
GROUP BY Poly,Feat_Code
