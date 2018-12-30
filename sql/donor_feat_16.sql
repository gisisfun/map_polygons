SELECT Feat.Poly,Feat.Feat_Src,
Feat.Feat_Code,


(Donor_SA1.P_Tot_Need_for_assistance*Feat.Feat_Prop) as NeedAssist,
(Donor_SA1.P_Tot_Tot*Feat.Feat_Prop) as TotP,
Feat.geometry
FROM Donor_SA1,Feat
WHERE Donor_SA1.Feat_Code=Feat.Feat_Code
