SELECT 
MB.MB_CODE16 as MB_CODE16, 
CAST(mb_counts.Person AS INT) as Persons, 
(ST_Area(MB_.geometry)*12391.3) as MB_Area,
MB.geometry
FROM MB
INNER JOIN MB_Counts
ON MB.MB_CODE16=MB_Counts.MB_CODE_2016
