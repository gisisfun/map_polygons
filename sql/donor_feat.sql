SELECT Feat.Poly,Feat.Feat_Src,
Feat.Feat_Code,
(Donor.Persons_Total_Has_need_for_assistance*Feat.Feat_Prop) as NeedAssist,
(Donor.Persons_Total_Total*Feat.Feat_Prop) as TotP,
Feat.geometry
FROM Donor,Feat
WHERE Donor.region_id=Feat.Feat_Code and Feat.Feat_Src='SA1_2011'
