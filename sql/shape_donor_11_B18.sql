SELECT Donor_Feat_B18.Poly,
Sum(Donor_Feat_B18.NeedAssist) as NeedAssist,
Sum(Donor_Feat_B18.TotP) as ToTP,
Shape.geometry
FROM Shape,Donor_Feat_B18
WHERE Donor_Feat_B18.Poly=Shape.p
GROUP BY Donor_Feat_B18.Poly
