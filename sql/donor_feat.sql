SELECT Feat.Poly,
Feat.SA1_7DIG11 as Feat_Code,
(Donor.Persons_Total_Has_need_for_assistance*Feat.Feat_Prop) as NeedAssist,
(Donor.Persons_Total_Total*Feat.Feat_Prop) as TotP,
Feat.geography
FROM Donor,Feat
WHERE Donor.region_id=Feat.Feat_Code and Feat.Feat_Src='SA1_2011'
