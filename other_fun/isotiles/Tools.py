from geopy.distance import distance,geodesic


def next_point(coords, brng, radial):
    return geodesic(kilometers=radial).destination(point=coords, bearing=brng)

    
        
