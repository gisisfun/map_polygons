SELECT CAST(Src.SA1_7DIG11 AS INT) as SA1_7DIG11, CAST(Src.SA1_MAIN11 AS INT) as SA1_MAIN11, 
CAST(Donor.Persons_Total_Has_Need_For_Assistance AS INT) as NeedAssist,
CAST(Donor.Persons_Total_Total AS INT) as TotP,
Src.geometry
FROM Donor,Src
WHERE Src.SA1_7DIG11=Donor.region_id
