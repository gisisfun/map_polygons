SELECT 
MB_.MB_CODE11 as MB_CODE11, 
CAST(MB_.Persons AS INT) as Persons, 
CAST(ST_Area(MB_.geometry)*12391.3 AS FlOAT) as MB_Area,
MB_.geometry
FROM MB_
WHERE MB_Area IS NOT NULL
