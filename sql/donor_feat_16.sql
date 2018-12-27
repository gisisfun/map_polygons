SELECT Feat.Poly,Feat.Feat_Src,
Feat.Feat_Code,
(Donor.P_Tot_Need_for_assistance*Feat.Feat_Prop) as NeedAssist,
(Donor.P_Tot_Tot*Feat.Feat_Prop) as TotP,
Feat.geometry
FROM Donor,Feat
WHERE Donor.SA1_7DIGITCODE_2016=Feat.Feat_Code
