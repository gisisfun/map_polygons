SELECT Donor_Feat_G18.Poly,
Sum(Donor_Feat_G18.NeedAssist) as NeedAssist,
Sum(Donor.TotP) as ToTP,
Shape.geometry
FROM Shape,Donor_Feat_G18
WHERE Donor_Feat_G18.Poly=Shape.p
GROUP BY Donor_Feat_G18.Poly
