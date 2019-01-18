SELECT Feat.Poly,Feat.Feat_Src,
Feat.Feat_Code,
(Donor_G18.P_Tot_Need_for_assistance*Feat.Feat_Prop) as NeedAssist,
(Donor_G18.P_Tot_Tot*Feat.Feat_Prop) as TotP,
Feat.geometry
FROM Donor_G18,Feat
WHERE Donor_G18.SA1_7DIGITCODE_2016=Feat.Feat_Code
