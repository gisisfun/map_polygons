
SELECT Feat_Aust.Poly as Poly,Feat_Aust.Feat_Cide as Feat_Code,'AGIL' as Feat_Type, Count(*) as AGILplaces,
Feat_Aust.geometry
FROM Feat_Aust 
LEFT JOIN 
AGIL ON ST_Within(AGIL.geometry,Feat_Aust.geometry) 
GROUP BY Poly,Feat_Code,Feat_Type
