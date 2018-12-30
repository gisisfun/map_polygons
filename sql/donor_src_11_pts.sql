SELECT CAST(Src.SA1_7DIG11 AS INT) as SA1_7DIG11, CAST(Src.SA1_MAIN11 AS INT) as SA1_MAIN11, ST_GeneratePoints(Src.geometry,CAST(Donor_B21.Persons_Total_Provided_unpaid_assistance AS INT)),
'UnpAssist' as Type
FROM Donor_B21,Src
WHERE Src.SA1_7DIG11=Donor_B21.region_id
