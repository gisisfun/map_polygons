SELECT Shape.p as Poly,Count(*) as places,
Shape.geometry
FROM Shape,Place
WHERE ST_Within(Place.geometry,Shape.geometry) and 
(Place.fclass = 'city' OR Place.fclass= 'town')
GROUP BY Poly
