SELECT Feat.Poly as Poly,
round(sum(Donor_B18.Persons_Total_Has_need_for_assistance*Feat.Feat_Prop),1) as NeedA11,
round(sum(Donor_B18.Persons_Total_Total*Feat.Feat_Prop),1) as NeedAT11,
round(sum(Donor_B21.Persons_Total_Provided_unpaid_assistance*Feat.Feat_Prop),1) as PUnPA11,
round(sum(Donor_B21.Persons_Total_Total*Feat.Feat_Prop),1) as PUnPAT11,
round(sum(Donor_B22.Persons_Total_Cared_for_Own_child_children_and_other_child_children*Feat.Feat_Prop),1) as PUnPCC11,
round(sum(Donor_B22.Persons_Total_Total*Feat.Feat_Prop),1) as PUnPCCT11
FROM Feat 
LEFT JOIN Donor_B18 ON Donor_B18.region_id=Feat.Feat_Code  
LEFT JOIN Donor_B21 ON Donor_B21.region_id=Feat.Feat_Code 
LEFT JOIN Donor_B22 ON Donor_B22.region_id=Feat.Feat_Code 
GROUP BY Poly
ORDER BY Poly
