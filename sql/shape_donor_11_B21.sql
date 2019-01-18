SELECT Donor_Feat_B21.Poly,
Sum(Donor_Feat_B21.PUnPAssist) as PUnPAssist,
Sum(Donor_Feat_B21.TotP) as ToTP,
Shape.geometry
FROM Shape,Donor_Feat_B21
WHERE Donor_Feat_B21.Poly=Shape.p
GROUP BY Donor_Feat_B21.Poly
