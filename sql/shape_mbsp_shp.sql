SELECT Identifier,
cast(longitude as float) as longitude,
cast(latitude as float) as latitude,
MBSP.geometry
FROM MBSP
