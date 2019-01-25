CREATE TABLE donor_feat_57km_11_B18_B21_B22 AS
SELECT Feat.Poly as Poly,
round(sum(Donor_B18.Persons_Total_Has_need_for_assistance*Feat.Feat_Prop),1) as NeedA11,
round(sum(Donor_B18.Persons_Total_Total*Feat.Feat_Prop),1) as NeedAT11,
round(sum(Donor_B21.Persons_Total_Provided_unpaid_assistance*Feat.Feat_Prop),1) as PUnPA11,
round(sum(Donor_B21.Persons_Total_Total*Feat.Feat_Prop),1) as PUnPT11,
round(sum(Donor_B22.Persons_Total_Cared_for_Own_child_children_and_other_child_children*Feat.Feat_Prop),1) as PUnPCC11,
round(sum(Donor_B22.Persons_Total_Total*Feat.Feat_Prop),1) as PUnPCCT11
FROM [feat_aust_57km_sa1_11] as Feat 
INNER JOIN [2011Census_B18_AUST_SA1_long] as Donor_B18 ON Donor_B18.region_id=Feat.Feat_Code  
INNER JOIN [2011Census_B21_AUST_SA1_long] as Donor_B21 ON Donor_B21.region_id=Feat.Feat_Code 
INNER JOIN [2011Census_B22B_AUST_SA1_long] as Donor_B22 ON Donor_B22.region_id=Feat.Feat_Code 
GROUP BY Poly
ORDER BY Poly;
