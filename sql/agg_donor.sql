SELECT Donor.Poly,  
Sum(Donor.NeedAssist), 
Sum(Donor.TotP), 
Aust.geometry
FROM Donor,Aust
WHERE Donor.Poly=Aust.Poly
GROUP BY Donor.Poly
