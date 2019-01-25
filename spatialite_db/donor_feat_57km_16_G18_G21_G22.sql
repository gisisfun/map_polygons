CREATE TABLE donor_feat_57km_16_G18_G21_G22 AS
SELECT Feat.Poly as Poly,
round(sum(Donor_G18.P_Tot_Need_for_assistance*Feat.Feat_Prop),1) as NeedA16,
round(sum(Donor_G18.P_Tot_Tot*Feat.Feat_Prop),1) as NeedAT16,
round(sum(Donor_G21.P_Tot_prvided_unpaid_assist*Feat.Feat_Prop),1) as PUnPA16,
round(sum(Donor_G21.P_Tot_Tot*Feat.Feat_Prop),1) as PUnPAT16,
round(sum(Donor_G22.P_Tot_CF_Total*Feat.Feat_Prop),1) as PUnPCC16,
round(sum(Donor_G22.P_Tot_Total*Feat.Feat_Prop),1) as PUnPCCT16
FROM [feat_aust_57km_sa1_16] as Feat 
INNER JOIN [2016Census_G18_AUS_SA1] as Donor_G18 
ON Donor_G18.SA1_7DIGITCODE_2016=Feat.Feat_Code  
INNER JOIN [2016Census_G21_AUS_SA1] as Donor_G21 
ON Donor_G21.SA1_7DIGITCODE_2016=Feat.Feat_Code 
INNER JOIN [2016Census_G22B_AUS_SA1] as Donor_G22 
ON Donor_G22.SA1_7DIGITCODE_2016=Feat.Feat_Code 
GROUP BY Poly
ORDER BY Poly;
