SELECT CAST(Shape_Area11.Poly as INT) as Poly,
CAST(Shape_Area11.NeedA11 as FLOAT) as NeedA11,
CAST(Shape_Area11.NeedAT11 as FLOAT) as NeedAT11,
CAST(Shape_Area11.PUnPA11 as FLOAT) as PUnPA11,
CAST(Shape_Area11.PUnPAT11 as FLOAT) as PUnPAT11,
CAST(Shape_Area11.PUnPCC11 as FLOAT) as PUnPCC11,
CAST(Shape_Area11.PUnPCCT11 as FLOAT) as PUnPCC11,
CAST(Shape_Area16.NeedA16 as FLOAT) as NeedA16,
CAST(Shape_Area16.NeedAT16 as FLOAT) as NeedAT16,
CAST(Shape_Area16.PUnPA16 as FLOAT) as PUnPA16,
CAST(Shape_Area16.PUnPAT16 as FLOAT) as PUnPAT16,
CAST(Shape_Area16.PUnPCC16 as FLOAT) as PUnPCC16,
CAST(Shape_Area16.PUnPCCT16 as FLOAT) as PUnPCCT16,
place.places,
AGIL.AGILplaces,
service.services,
bstation.bstations,
road.roads,
MBSP.MBSPplaces,
Shape_Aust.est_area,
Shape_Aust.geometry
FROM Shape_Aust 
LEFT JOIN Shape_Area11
ON Shape.p=CAST(Shape_Area11.Poly as INT)
LEFT JOIN Shape_Area16
ON Shape.p=CAST(Shape_Area16.Poly as INT)
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

