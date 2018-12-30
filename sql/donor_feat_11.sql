SELECT Feat.Poly,Feat.Feat_Src,
Feat.Feat_Code,
(Donor_SA1.Persons_Total_Provided_unpaid_assistance*Feat.Feat_Prop) as UnpAssist,
(Donor_SA1.Persons_Total_Total*Feat.Feat_Prop) as UnpAssTot,
(Donor_SA1.Persons_Total_Has_need_for_assistance*Feat.Feat_Prop) as NeedAssist,
(Donor_SA1.Persons_Total_Total*Feat.Feat_Prop) as TotP,
Feat.geometry
FROM Donor_SA1,Feat
WHERE Donor_SA1.Feat_Code=Feat.Feat_Code
