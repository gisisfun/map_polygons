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
CAST(Tabular_Place_Data.places AS FLOAT) as places,
CAST(Tabular_Place_Data.AGILplaces AS FLOAT) as AGILplaces,
CAST(Tabular_Place_Data.services AS FLOAT) as services ,
CAST(Tabular_Place_Data.bstations AS FLOAT) as bstations ,
CAST(Tabular_Place_Data.roads AS FLOAT) as roads,
CAST(Tabular_Place_Data.MBSPplaces AS FLOAT) as MBSPplaces,
CAST(Tabular_Place_Data.est_area AS FLOAT) as est_area,
Shape_Aust.geometry
FROM Shape_Aust 
LEFT JOIN Tabular_Place_Data
ON Shape_Aust.p=CAST(Tabular_Place_Data.Poly as INT)

