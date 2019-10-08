import numpy as np
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
print(len(fred.array_hex))


#print(fred.Intersect_List[0],fred.new[0][0],fred.new[0][1])
#print(fred.Intersect_List[250],fred.new[0][498],fred.new[1][499])
#print(fred.Intersect_List[498],fred.new[1][0],fred.new[1][1])
#print(fred.Intersect_List[499],fred.new[1][2],fred.new[1][3])
##index divided by 501(502 col count) and remainder
#print(fred.Intersect_List[1],fred.new[0][2],fred.new[0][3])
#print(fred.Intersect_List[2],fred.new[0][4],fred.new[0][5])
#
#print(fred.Intersect_List[107],fred.new[0][214],fred.new[0][215])
#print(fred.Intersect_List[456],fred.new[1,411],fred.new[1,412])
##print(fred.Intersect_List[249],fred.new[1,247],fred.new[1,248])
##print(fred.Intersect_List[250],fred.new[1,248],fred.new[1,249])
##print('250',fred.Intersect_List[251],fred.new[2,0],fred.new[2,1])
#print(fred.new.shape)
