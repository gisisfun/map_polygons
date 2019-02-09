SELECT 
MB.MB_CODE16 as MB_CODE16, 
mb_counts.Person as Persons, 
MB.geometry
FROM MB
INNER JOIN MB_Counts
ON MB.MB_CODE16=MB_Counts.MB_CODE_2016
