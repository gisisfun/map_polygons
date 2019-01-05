SELECT Shape.p as Poly,Count(*) as MBSPplaces,
Shape.geometry
FROM Shape,MBSP
WHERE ST_Within(MBSP.geometry,Shape.geometry) 
GROUP BY Poly
