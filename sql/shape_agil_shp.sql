SELECT LCODE,
cast(LONGITUDE as float) as LATITUDE,
cast(LATITUDE as float) as LATITUDE,
AGIL_Locations.geometry
FROM AGIL_Locations
