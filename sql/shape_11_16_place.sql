SELECT CAST(Tabular_Place_Data.Poly as INT) as Poly,
CAST(Tabular_Place_Data.NeedA11 AS FLOAT) as NeedA11,
CAST(Tabular_Place_Data.NeedAT11 AS FLOAT) as NeedAT11,
CAST(Tabular_Place_Data.PUnPA11 AS FLOAT) as NeedPA11,
CAST(Tabular_Place_Data.PUnPAT11 AS FLOAT) as NeedPAT11,
CAST(Tabular_Place_Data.PUnPCC11 AS FLOAT) as NeedPCC11,
CAST(Tabular_Place_Data.PUnPCCT11 AS FLOAT) as NeedPCCT11,
CAST(Tabular_Place_Data.NeedA16 AS FLOAT) as NeedA16,
CAST(Tabular_Place_Data.NeedAT16 AS FLOAT) as NeedAT16,
CAST(Tabular_Place_Data.PUnPA16 AS FLOAT) as NeedPA16,
CAST(Tabular_Place_Data.PUnPAT16 AS FLOAT) as NeedPAT16,
CAST(Tabular_Place_Data.PUnPCC16 AS FLOAT) as NeedPCC16,
CAST(Tabular_Place_Data.PUnPCCT16 AS FLOAT) as NeedPCCT16,
Tabular_Place_Data.places,
Tabular_Place_Data.AGILplaces,
Tabular_Place_Data.services,
Tabular_Place_Data.bstations,
Tabular_Place_Data.roads,
Tabular_Place_Data.MBSPplaces,
Tabular_Place_Data.est_area,
Shape_Aust.geometry
FROM Shape_Aust 
LEFT JOIN Tabular_Place_Data
ON Shape_Aust.p=CAST(Tabular_Place_Data.Poly as INT)

