SELECT CAST(Shape_Place11.Poly as INT) as Poly,
Shape_Place11.NeedA11,
Shape_Place11.NeedAT11,
Shape_Place11.PUnPA11,
Shape_Place11.PUnPAT11,
Shape_Place11.PUnPCC11,
Shape_Place11.PUnPCCT11,
Shape_Place16.NeedA16,
Shape_Place16.NeedAT16,
Shape_Place16.PUnPA16,
Shape_Place16.PUnPAT16,
Shape_Place16.PUnPCC16,
Shape_Place16.PUnPCCT16,
place.places,
AGIL.AGILplaces,
service.services,
bstation.bstations,
road.roads,
MBSP.MBSPplaces,
Shape.est_area,
Shape.geometry
FROM Shape 
LEFT JOIN Shape_Place11
ON Shape.p=CAST(Shape_Place11.Poly as INT)
LEFT JOIN Shape_Place16
ON Shape.p=CAST(Shape_Place16.Poly as INT)
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

