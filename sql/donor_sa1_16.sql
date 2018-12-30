SELECT Donor_G21.SA1_7DIGITCODE_2016 as Feat_Code,
(Donor_G21.P_Tot_prvided_unpaid_assist) as UnpAssist,
(Donor_G21.P_Tot_Tot) as UnpAssTot,
(Donor_G18.P_Tot_Need_for_assistance) as NeedAssist,
(Donor_G18.P_Tot_Tot) as TotP
FROM Donor_G18,Donor_G21
WHERE Donor_G18.SA1_7DIGITCODE_2016=Donor_G21.SA1_7DIGITCODE_2016
