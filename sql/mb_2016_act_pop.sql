SELECT 
MB_ACT.MB_CODE16 as MB_CODE16, 
mb_counts.Person as Persons, 
MB_ACT.geometry
FROM MB_ACT
INNER JOIN MB_Counts
ON MB_ACT.MB_CODE16=MB_Counts.MB_CODE_2016