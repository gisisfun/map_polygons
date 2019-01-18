SELECT Feat.Poly,Feat.Feat_Src,
Feat.Feat_Code,
(Donor_B21.Persons_Total_Provided_unpaid_assistance*Feat.Feat_Prop) as PUnPAssist,
(Donor_B21.Persons_Total_Total*Feat.Feat_Prop) as TotP,
Feat.geometry
FROM Donor_B21,Feat
WHERE Donor_B21.region_id=Feat.Feat_Code
