SELECT CAST(Src.SA1_7DIG11 AS INT) as SA1_7DIG11, CAST(Src.SA1_MAIN11 AS INT) as SA1_MAIN11, 
CAST(Donor_B21.Persons_Total_Provided_unpaid_assistance AS INT) as UnpAssist,
CAST(Donor_B21.Persons_Total_Total AS INT)  as UnpAssTot,
CAST(Donor_B18.Persons_Total_Has_Need_For_Assistance AS INT) as NeedAssist,
CAST(Donor_B18.Persons_Total_Total AS INT) as TotP,
Src.geometry
FROM Donor_B18,Donor_B21,Src
WHERE Src.SA1_7DIG11=Donor_B18.region_id and Donor_B18.region_id=Donor_B21.region_id
