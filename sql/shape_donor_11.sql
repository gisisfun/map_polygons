SELECT Donor.Poly,
Sum(Donor.NeedAssist) as NeedAssist,
Sum(Donor.TotP) as ToTP,
Shape.geometry
FROM Shape,Donor
WHERE Donor.Poly=Shape.p
GROUP BY Donor.Poly
