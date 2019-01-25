SELECT CAST(Shape11.Poly as INT) as Poly,
Shape11.NeedA11,
Shape11.NeedAT11,
Shape11.PUnPA11,
Shape11.PUnPAT11,
Shape11.PUnPCC11,
Shape11.PUnPCCT11,
Shape16.NeedA16,
Shape16.NeedAT16,
Shape16.PUnPA16,
Shape16.PUnPAT16,
Shape16.PUnPCC16,
Shape16.PUnPCCT16,
place.places,
AGIL.AGILplaces,
service.services,
bstation.bstations,
road.roads,
MBSP.MBSPplaces,
Shape.est_area,
Shape.geometry
FROM Shape 
LEFT JOIN Shape11
ON Shape.p=CAST(Shape11.Poly as INT)
LEFT JOIN Shape16
ON Shape.p=CAST(Shape16.Poly as INT)
LEFT JOIN MBSP 
ON Shape.p = CAST(MBSP.Poly as INT)
LEFT JOIN bstation
ON Shape.p = CAST(bstation.Poly as INT)
LEFT JOIN road
ON Shape.p = CAST(road.Poly as INT)
LEFT JOIN service
ON Shape.p = CAST(service.Poly as INT)
LEFT JOIN place
ON Shape.p = CAST(place.Poly as INT)
LEFT JOIN AGIL
ON Shape.p = CAST(AGIL.Poly as INT)

