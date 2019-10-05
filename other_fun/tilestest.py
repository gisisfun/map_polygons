
from isotiles import (Tiles,Tools)

fred = Tiles.Fred()
print(fred.dump())
#H_List = fred.horizontal()
#V_List = fred.vertical()



#H_Len = len(H_List)
#V_Len = len(V_List)

#PatternGrid = np.tile(A = fred.Pattern, reps = [int(V_Len/4),int(((H_Len/3)/1.333333333333334))])
#print(V_Len,H_Len,PatternGrid.shape[0])

print('\n')
print('horizontal',fred.H_List[-1],'and',fred.H_List[fred.PatternGrid.shape[1]])
print('vertical',fred.V_List[-1],'and',fred.V_List[fred.PatternGrid.shape[0]])
print('\n')
#print(H_List[0],H_List[-1],H_List[PatternGrid.shape[1]])

print('length',fred.H_Len,fred.V_Len,fred.V_List[-1])
print('\n')
print(fred.Intersect_List[-1])

