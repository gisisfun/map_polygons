SELECT Shape11.Poly,
Shape11.NeedAssist as NeedA11,
Shape11.TotP as ToTP11,
Shape16.NeedAssist as NeedA16,
Shape16.TotP as ToTP16,
Shape.est_area,
Shape11.geometry
FROM Shape11,Shape16,Shape
WHERE Shape11.Poly=Shape16.Poly and Shape11.Poly=Shape.p

