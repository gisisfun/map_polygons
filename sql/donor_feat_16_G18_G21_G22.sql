SELECT Feat.Poly,
round(sum(Donor_G18.P_Tot_Need_for_assistance*Feat.Feat_Prop),1) as NeedA16,
round(sum(Donor_G18.P_Tot_Tot*Feat.Feat_Prop),1) as NeedAT16,
round(sum(Donor_G21.P_Tot_prvided_unpaid_assist*Feat.Feat_Prop),1) as PUnPA16,
round(sum(Donor_G21.P_Tot_Tot*Feat.Feat_Prop),1) as PUnPAT16,
round(sum(Donor_G22.P_Tot_CF_Total*Feat.Feat_Prop),1) as PUnPCC16,
round(sum(Donor_G22.P_Tot_Total*Feat.Feat_Prop),1) as PUnPCCT16
FROM Feat 
LEFT JOIN Donor_G18 ON Donor_G18.SA1_7DIGITCODE_2016=Feat.Feat_Code  
LEFT JOIN Donor_G21 ON Donor_G21.SA1_7DIGITCODE_2016=Feat.Feat_Code 
LEFT JOIN Donor_G22 ON Donor_G22.SA1_7DIGITCODE_2016=Feat.Feat_Code 
GROUP BY Feat.Poly
ORDER BY Feat.Poly
