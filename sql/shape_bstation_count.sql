SELECT Shape.p as Poly,Count(*) as bstations,
Shape.geometry
FROM Shape,POI
WHERE ST_Within(POI.geometry,Shape.geometry) and 
(POI.fclass= 'comms_tower')
GROUP BY Poly
