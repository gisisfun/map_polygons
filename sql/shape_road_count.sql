SELECT Shape.p as Poly,Count(*) as roads,
Shape.geometry
FROM Shape,Road
WHERE ST_Within(Road.geometry,Shape.geometry) or ST_Intersects(Road.geometry,Shape.geometry)
GROUP BY Poly
