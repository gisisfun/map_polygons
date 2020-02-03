SELECT CAST(Tabular_Area_Data.Poly as INT) as Poly,
CAST(Tabular_Area_Data.NeedA11 AS FLOAT) as NeedA11,
CAST(Tabular_Area_Data.NeedAT11 AS FLOAT) as NeedAT11,
CAST(Tabular_Area_Data.PUnPA11 AS FLOAT) as NeedPA11,
CAST(Tabular_Area_Data.PUnPAT11 AS FLOAT) as NeedPAT11,
CAST(Tabular_Area_Data.PUnPCC11 AS FLOAT) as NeedPCC11,
CAST(Tabular_Area_Data.PUnPCCT11 AS FLOAT) as NeedPCCT11,
CAST(Tabular_Area_Data.NeedA16 AS FLOAT) as NeedA16,
CAST(Tabular_Area_Data.NeedAT16 AS FLOAT) as NeedAT16,
CAST(Tabular_Area_Data.PUnPA16 AS FLOAT) as NeedPA16,
CAST(Tabular_Area_Data.PUnPAT16 AS FLOAT) as NeedPAT16,
CAST(Tabular_Area_Data.PUnPCC16 AS FLOAT) as NeedPCC16,
CAST(Tabular_Area_Data.PUnPCCT16 AS FLOAT) as NeedPCCT16,
CAST(Tabular_Area_Data.places AS FLOAT) as places,
CAST(Tabular_Area_Data.AGIL AS FLOAT) as AGIL,
CAST(Tabular_Area_Data.MBSP AS FLOAT) as MBSP,
Tabular_Area_Data.p_NB as P_NB,
CAST(Tabular_Area_Data.row AS FLOAT) as row,
CAST(Tabular_Area_Data.col AS FLOAT) as col,
CAST(Tabular_Area_Data.est_area AS FLOAT) as est_area,
Shape_Aust.geometry
FROM Shape_Aust 
LEFT JOIN Tabular_Area_Data
ON Shape_Aust.p=CAST(Tabular_Area_Data.Poly as INT)

