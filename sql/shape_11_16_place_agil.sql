SELECT Shape11_16_place.Poly,
Shape11_16_place.NeedA11,
Shape11_16_place.ToTP11,
Shape11_16_place.NeedA16,
Shape11_16_place.ToTP16,
Shape11_16_place.est_area,
Shape11_16_place.places,
AGIL.AGILplaces,
Shape11_16_place.geometry
FROM Shape11_16_place LEFT JOIN AGIL
ON Shape11_16_place.Poly = AGIL.Poly

