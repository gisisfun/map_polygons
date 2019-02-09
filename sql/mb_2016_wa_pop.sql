SELECT 
MB_WA.MB_CODE16 as MB_CODE16, 
mb_counts.Person as Persons, 
MB_WA.geometry
FROM MB_WA
INNER JOIN MB_Counts
ON MB_WA.MB_CODE16=MB_Counts.MB_CODE_2016
