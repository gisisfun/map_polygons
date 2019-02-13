SELECT 
MB.MB_CODE11 as MB_CODE11, 
CAST(mb_counts.Persons_Usually_Resident AS INT) as Persons, 
MB.geometry
FROM MB
INNER JOIN MB_Counts
ON MB.MB_CODE11=MB_Counts.Mesh_Block_ID
