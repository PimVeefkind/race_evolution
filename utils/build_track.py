from shapely.geometry import Polygon
from shapely.affinity import rotate, scale, translate
import matplotlib.pyplot as plt
import numpy as np

def rotate_and_translate(coords,corner,orientation):

    x,y = coords[0],coords[1]

    poly_rot = rotate(corner,np.pi/2*orientation,origin = (x,y+1),use_radians=True)
    
    if orientation == 1:
        return translate(poly_rot, xoff=0,yoff=-1)
    elif orientation == 2:
        return translate(poly_rot, xoff=1,yoff=-1)
    elif orientation == 3:
        return translate(poly_rot, xoff=1,yoff= 0)
    else:
        return poly_rot

def straight(coords, prev, narrowness):

    n = narrowness
    x = coords[0]
    y = coords[1]

    poly = Polygon([(x,y+n),(x+1,y+n),(x+1,y+1-n),(x,y+1-n),(x,y+n)])

    return(rotate(poly,np.pi/2*prev,origin = 'center',use_radians=True))

def corner(coords, narrowness):

    n = narrowness
    x = coords[0]
    y = coords[1]

    def quarter_circle(coords,r, n_points = 20):

        x = coords[0]
        y = coords[1]
        points = []
        for n in range(int(n_points+1)):

            points.append((x+r*np.sin(np.pi/2*n/n_points),\
                           y+r*(1-np.cos(np.pi/2*n/n_points))))

        return points

    poly = Polygon(quarter_circle((x,y+n),1-n)+quarter_circle((x,y+1-n),n)[::-1]\
                    + [(x,y+n)])
    
    return(poly)


def construct_circuit(n_elements = 5, narrowness = 0.2):

    orientation = 0
    coords = [0,0]
    track = straight(coords, 0, narrowness)

    coords = [1,0]
    for i in range(n_elements-1):
        
        random_numb = np.random.choice([-1,0,1], p = [1/4,1/2,1/4])
        if random_numb == -1:
            right_corner = scale(corner(coords,narrowness),\
                xfact=1,yfact=-1, origin = (coords[0]+1/2,coords[1]+1/2))
            rotated_corner = rotate_and_translate(coords,right_corner,orientation)
            track = track.union(rotated_corner)

        if random_numb == 0:
            track = track.union(straight(coords, orientation,narrowness))

        if random_numb == 1:
            left_corner = corner(coords,narrowness)
            rotated_corner = rotate_and_translate(coords,left_corner,orientation)
            track = track.union(rotated_corner)

        orientation = (orientation + random_numb)%4

        if orientation == 0:
            coords[0] += 1
        elif orientation == 1:
            coords[1] += 1
        elif orientation == 2:
            coords[0] += -1
        elif orientation == 3:
            coords[1] += -1

    return track

if __name__ == "__main__":

    track = construct_circuit(n_elements=15)
    print(type(track)== type(Polygon([])))
    
    fig, ax = plt.subplots()

    ax.plot(*track.exterior.xy)
    ax.set_aspect('equal', adjustable='box')

    plt.show()

        




