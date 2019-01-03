SELECT Shape.p as Poly,Count(*) as AGILplaces,
Shape.geometry
FROM Shape,AGIL
WHERE ST_Within(AGIL.geometry,Shape.geometry) 
GROUP BY Poly
