SELECT Donor_B18.region_id as Feat_Code,
(Donor_B21.Persons_Total_Provided_unpaid_assistance) as UnpAssist,
(Donor_B21.Persons_Total_Total) as UnpAssTot,
(Donor_B18.Persons_Total_Has_need_for_assistance) as NeedAssist,
(Donor_B18.Persons_Total_Total) as TotP
FROM Donor_B18,Donor_B21
WHERE Donor_B18.region_id=Donor_B21.region_id
