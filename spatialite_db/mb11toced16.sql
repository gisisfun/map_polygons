SELECT 
MB11.MB_CODE11,
CED16.CED_CODE16,
CED16.CED_NAME16,
ST_Area(ST_Intersection(MB11.geometry,CED16.geometry))/ST_Area(MB11.geometry) as Area_Prop
FROM MB11,CED16
WHERE ST_Intersects(MB11.geometry,CED16.geometry)
