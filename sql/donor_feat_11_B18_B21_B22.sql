SELECT Feat.Poly,
round(sum(Donor_B18.Persons_Total_Has_need_for_assistance*Feat.Feat_Prop),1) as NeedA11,
round(sum(Donor_B18.Persons_Total_Total*Feat.Feat_Prop),1) as NeedAT11,
round(sum(Donor_B21.Persons_Total_Provided_unpaid_assistance*Feat.Feat_Prop),1) as PUnPA11,
round(sum(Donor_B21.Persons_Total_Total*Feat.Feat_Prop),1) as PUnPT11,
round(sum(Donor_B22.Persons_Total_Cared_for_Own_child_children_and_other_child_children*Feat.Feat_Prop),1) as PUnPCC11,
round(sum(Donor_B22.Persons_Total_Total*Feat.Feat_Prop),1) as PUPCCT11
FROM Donor_B18,Donor_B21,Donor_B22,Feat
WHERE Donor_B18.region_id=Feat.Feat_Code 
and Donor_B21.region_id=Feat.Feat_Code
and Donor_B22.region_id=Feat.Feat_Code
GROUP BY Feat.Poly
ORDER BY Feat.Poly
