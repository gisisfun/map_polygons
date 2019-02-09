SELECT 
MB_OT.MB_CODE16 as MB_CODE16, 
mb_counts.Person as Persons, 
MB_OT.geometry
FROM MB_OT
INNER JOIN MB_Counts
ON MB_OT.MB_CODE16=MB_Counts.MB_CODE_2016
