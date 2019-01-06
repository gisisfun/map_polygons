SELECT Shape.p as Poly,Count(*) as services,
Shape.geometry
FROM Shape,POI
WHERE ST_Within(POI.geometry,Shape.geometry) and 
(POI.fclass = 'school' OR POI.fclass= 'police' OR POI.fclass= 'doctors' OR POI.fclass= 'hospital' OR POI.fclass= 'fire_station')
GROUP BY Poly
