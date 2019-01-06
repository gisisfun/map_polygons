SELECT Shape11_16_place_agil.Poly,
Shape11_16_place_agil.NeedA11,
Shape11_16_place_agil.ToTP11,
Shape11_16_place_agil.NeedA16,
Shape11_16_place_agil.ToTP16,
Shape11_16_place_agil.est_area,
Shape11_16_place_agil.places,
Shape11_16_place_agil.AGILplaces,
service.services,
Shape11_16_place_agil.geometry
FROM Shape11_16_place_agil LEFT JOIN service
ON Shape11_16_place_agil.Poly = service.Poly

