SELECT Feat.Poly,Feat.Feat_Src,
Feat.Feat_Code,
(Donor_B18.Persons_Total_Has_need_for_assistance*Feat.Feat_Prop) as NeedAssist,
(Donor_B18.Persons_Total_Total*Feat.Feat_Prop) as TotP,
Feat.geometry
FROM Donor_B18,Feat
WHERE Donor_B18.region_id=Feat.Feat_Code
