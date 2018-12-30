SELECT CAST(Src.SA1_7DIG16 AS INT) as SA1_7DIG16, CAST(Src.SA1_MAIN16 AS INT) as SA1_MAIN16, 
CAST(Donor_G21.P_Tot_prvided_unpaid_assist AS INT) as UnpAssist,
CAST(Donor_G21.P_Tot_Tot AS INT) as UnpAssTot,
CAST(Donor_G18.P_Tot_Need_for_assistance AS INT) as NeedAssist,
CAST(Donor_G18.P_Tot_Tot AS INT) as TotP,
Src.geometry
FROM Donor_G18,Donor_B21,Src
WHERE Src.SA1_7DIG16=Donor_G18.SA1_7DIGITCODE_2016 and Donor_G18.SA1_7DIGITCODE_2016=Donor_G21.SA1_7DIGITCODE_2016
