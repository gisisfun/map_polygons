SELECT Feat.SA1_7DIG11, 
Donor.Persons_Total_Has_Need_For_Assistance as NeedAssist,
Donor.Persons_Total_Total asTotP,
Feat.geometry
FROM Feat,Aust 
WHERE ST_Intersects(Feat.geometry,Aust.geometry) 
