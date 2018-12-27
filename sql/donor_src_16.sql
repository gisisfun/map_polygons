SELECT CAST(Src.SA1_7DIG16 AS INT) as SA1_7DIG16, CAST(Src.SA1_MAIN16 AS INT) as SA1_MAIN16, 
CAST(Donor.P_Tot_Need_for_assistance AS INT) as NeedAssist,
CAST(Donor.P_Tot_Tot AS INT) as TotP,
Src.geometry
FROM Donor,Src
WHERE Src.SA1_7DIG16=Donor.SA1_7DIGITCODE_2016
