SELECT Feat.Poly,
round(sum(Donor_G18.P_Tot_Need_for_assistance*Feat.Feat_Prop),1) as NeedA16,
round(sum(Donor_G18.P_Tot_Tot*Feat.Feat_Prop),1) as NeedAT16,
round(sum(Donor_G21.P_Tot_prvided_unpaid_assist*Feat.Feat_Prop),1) as PUnPA16,
round(sum(Donor_G21.P_Tot_Tot*Feat.Feat_Prop),1) as PUnPAT16,
round(sum(Donor_G22.P_Tot_CF_Total*Feat.Feat_Prop),1) as PUnPCC11,
round(sum(Donor_G22.P_Tot_Total*Feat.Feat_Prop),1) as PUnPCCT11
FROM Donor_G18,Donor_B21,Donor_B22,Feat
WHERE Donor_G18.region_id=Feat.Feat_Code 
and Donor_G21.region_id=Feat.Feat_Code  
and Donor_G22.region_id=Feat.Feat_Code 
GROUP BY Feat.Poly
ORDER BY Feat.Poly
