SELECT Donor_Feat_G21.Poly,
Sum(Donor_Feat_G21.NeedAssist) as NeedAssist,
Sum(Donor_Feat_G21.TotP) as ToTP,
Shape.geometry
FROM Shape,Donor_Feat_G21
WHERE Donor_Feat_G21.Poly=Shape.p
GROUP BY Donor_Feat_G21.Poly
