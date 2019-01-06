SELECT Shape11_16.Poly,
Shape11_16.NeedA11,
Shape11_16.ToTP11,
Shape11_16.NeedA16,
Shape11_16.ToTP16,
Shape11_16.est_area,
Place.places, 
Shape11_16.geometry
FROM Shape11_16 LEFT JOIN Place
ON Shape11_16.Poly = Place.Poly

