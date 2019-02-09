SELECT 
MB_NT.MB_CODE16 as MB_CODE16, 
mb_counts.Person as Persons, 
MB_NT.geometry
FROM MB_NT
INNER JOIN MB_Counts
ON MB_NT.MB_CODE16=MB_Counts.MB_CODE_2016
