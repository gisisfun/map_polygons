SELECT Feat.Poly,Feat.Feat_Src,
Feat.Feat_Code,
(Donor_G21.P_Tot_prvided_unpaid_assist*Feat.Feat_Prop) as PUnPAssist,
(Donor_G21.P_Tot_Tot*Feat.Feat_Prop) as TotP,
Feat.geometry
FROM Donor_G21,Feat
WHERE Donor_G21.SA1_7DIGITCODE_2016=Feat.Feat_Code
