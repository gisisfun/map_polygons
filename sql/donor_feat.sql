SELECT 
 Feat.Poly,
'SA1_2016' as Feat_Src,
Feat.SA1_MAIN16 as Feat_Code,
'' as Feat_Name,
Feat.Poly,  
(ST_Area(ST_Intersection(Feat.geometry,A
feat.geography
FROM Donor,Feat
WHERE Donor.SA1_MAINCODE_2011=Feat.Feat.Code and Feat_Src='SA1_2011'
