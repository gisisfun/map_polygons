SELECT 
MB_SA.MB_CODE16 as MB_CODE16, 
mb_counts.Person as Persons, 
MB_SA.geometry
FROM MB_SA
INNER JOIN MB_Counts
ON MB_SA.MB_CODE16=MB_Counts.MB_CODE_2016
