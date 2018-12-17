SELECT Aust.p as Poly,   
Sum(Donor.Persons_Total_Has_need_for_assistance*(ST_Area(ST_Intersection(Feat.geometry,Aust.geometry))*12391.3)/(st_area(Feat.geometry)*12391.3)) as NeedAssist,
Sum(Donor.Persons_Total_Total*(ST_Area(ST_Intersection(Feat.geometry,Aust.geometry))*12391.3)/(st_area(Feat.geometry)*12391.3)) as TotP,
Aust.geometry 
FROM Feat,Aust,Donor 
WHERE ST_Intersects(Feat.geometry,Aust.geometry) and Donor.region_id=Feat.SA1_7DIG11 
GROUP BY Aust.p
