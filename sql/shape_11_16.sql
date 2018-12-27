SELECT Shape11.Poly,
Shape11.NeedAssist as NeedA11,
Shape11.TotP as ToTP11,
Shape16.NeedAssist as NeedA16,
Shape16.TotP as ToTP16
FROM Shape11,Shape16
WHERE Shape11.Poly=Shape16.Poly

