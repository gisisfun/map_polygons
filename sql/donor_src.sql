SELECT Src.SA1_7DIG11, Src.SA1_MAIN11, 
Donor.Persons_Total_Has_Need_For_Assistance as NeedAssist,
Donor.Persons_Total_Total asTotP,
Src.geometry
FROM Donor,Src
WHERE Src.Sa1_7DIG11=Donor.region_id
