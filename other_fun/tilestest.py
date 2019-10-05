import numpy as np
from isotiles import (Tiles,Tools)

fred = Tiles.Fred()
print(fred.dump())
H_List = fred.horizontal()
V_List = fred.vertical()


H_Len = len(H_List)
V_Len = len(V_List)

PatternGrid = np.tile(A = fred.Pattern, reps = [int(V_Len/4),int(((H_Len/3)/1.334))])
print(V_Len,H_Len,PatternGrid.shape[0])


print(H_List[0],H_List[-1],H_List[PatternGrid.shape[1]])
print(V_List[0],V_List[-1],V_List[PatternGrid.shape[0]])

