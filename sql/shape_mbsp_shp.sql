SELECT Identifier,
cast(longitude as float) as longitude,
cast(latitude as float) as latitude,
MBSP_Database.geometry
FROM MBSP_Database
