SELECT Shape.p as Poly,Place.name as place,
ST_Centroid(Place.Geometry)
FROM Shape,Place
WHERE ST_Within(Place.geometry,Shape.geometry) and 
(Place.fclass = 'city' OR Place.fclass= 'town')

