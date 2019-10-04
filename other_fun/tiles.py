import numpy as np
from geopy.distance import distance,geodesic

def point_radial_distance(self, brng, radial):
    return geodesic(kilometers=radial).destination(point=self, bearing=brng)


def horizontal(east,north,west,south,hor_seq,radial):
    #1/7 deriving vertical list of reference points from north to south for longitudes or x axis
    angle = 180
    new_north = north
    #print(east,new_north,south,'\n')
    i = 0
    longitudes = []
    longitudes.append([[north,west],[north,east]])

    while new_north >= south:
        if i > 3:
            i = 0
            
        latlong = [new_north,east]
        p = point_radial_distance(latlong,angle,radial * hor_seq[i]) 
        new_north = p[0]
        longitudes.append([[p[0],west],[p[0],east]])
        i += 1
    return longitudes


def vertical(east,north,west,south,vert_seq,radial):
    print('east {0} west {1}'.format(east,west))
    #2/7 deriving horizontal list of reference points from east to west for latitudes or y axis
    angle = 90

    i = 0
    new_west = west
    latitudes =[]
    latitudes.append([[north,west],[south,west]])
    while new_west <= east:
        if i > 3:
            i = 0

        latlong = [north,new_west]
        p = point_radial_distance(latlong,angle,radial*vert_seq[i])
        new_west = p[1]
        latitudes.append([[north,p[1]],[south,p[1]]])    
        i += 1
    return latitudes

def line_intersection(line1, line2):
    # source: https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-between-two-lines-in-python
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def intersections(hor_line_list, hor_max, vert_line_list, vert_max):
    print('\n3/7 deriving intersection point data between horizontal and \
    vertical lines')
    intersect_list = []
    for h in range(0, hor_max):
        for v in range(0, vert_max):
            intersect_point = line_intersection(hor_line_list[h],
            vert_line_list[v])
            intersect_data = [intersect_point[1], intersect_point[0]]
            intersect_list.append(intersect_data)

    print('derived {0} points of intersection'.format(len(intersect_list)))
    return intersect_list
vert_seq =[0.7071,1,0.7071,1]
hor_seq = [0.7071,0.7071,0.7071,0.7071]
v_list = vertical(145,-8,96,-45,vert_seq,50)
h_list = horizontal(145,-8,96,-45,hor_seq,50)
len_h = len(h_list)
len_v =len(v_list)
print(len_h,len_v)
#print(h_list)
a = np.array( [[0,1,1,0],[1,0,0,1],[0,1,1,0],[1,0,0,1]])

b = np.tile(A = a, reps = [len_v,len_h])
print(b.shape)
for i in range(0,b.shape[1]):
	if (i+1)% 4 is 0:
		print(i)
		b[i,0] = 0

c = b[:(b.shape[0]-1),:(b.shape[1]-4)]
print(c)

print(c.shape)
def coord(h,v,npa,hlist,vlist):
	return npa[h,v] ,hlist[h] ,vlist[v]
	
def offset(start, off, npa, hlist, vlist):
	thelines =[]
	voff = start + off
	hoff = start + (off* 2)
	
	list = [[voff, hoff + 1],
	[voff, hoff + 2],
	[voff + 1, hoff + 3],
	[voff + 2, hoff + 1],
	[voff + 2, hoff + 2],
	[voff + 1, hoff + 3]]
	#print(list)
	for m in list:
		(t,hor,vert) = coord(m[0],m[1],npa,hlist,vlist)
		print(t,hor,vert)
		thelines.append([hor,vert])
	
	return thelines
	
	
	
a = 0
print(coord(a,a + 1,c,h_list,v_list)[0])
print(coord(a,a + 2,c,h_list,v_list)[0])
print(coord(a + 1,a,c,h_list,v_list)[0])
print(coord(a + 2,a + 1,c,h_list,v_list)[0])
print(coord(a + 2,a + 2,c,h_list,v_list)[0])
print(coord(a + 1,a + 3,c,h_list,v_list)[0])
e = 2
f = 4
print('offset')
offset(a,4,c,h_list, v_list)


	