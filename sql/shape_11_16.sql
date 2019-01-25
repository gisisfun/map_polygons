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
Shape.est_area,
Shape.geometry
FROM Shape 
LEFT JOIN Shape11
ON Shape.p=CAST(Shape11.Poly as INT)
LEFT JOIN Shape16
ON Shape.p=CAST(Shape16.Poly as INT)

