from shapely.geometry import Polygon, Point
from shapely.affinity import rotate, scale, translate
import matplotlib.pyplot as plt
import numpy as np

class Track():

    def __init__(self, n_elements, narrowness, screen_size):

        self.n_elements = n_elements
        self.narrowness = narrowness

        self.track = self.construct_track(screen_size)
        while self.track.geom_type != 'Polygon':
            self.track = self.construct_track(screen_size)
        
        self.exterior = self.track.exterior
        self.exterior_list = list(self.track.exterior.coords)


    def rotate_and_translate(self,corner):

        x,y = self.curr_coords

        poly_rot = rotate(corner,np.pi/2*self.orientation,origin = (x,y+1),use_radians=True)
    
        if self.orientation == 1:
            return translate(poly_rot, xoff=0,yoff=-1)
        elif self.orientation == 2:
            return translate(poly_rot, xoff=1,yoff=-1)
        elif self.orientation == 3:
            return translate(poly_rot, xoff=1,yoff= 0)
        else:
            return poly_rot

    def straight(self):

        n = self.narrowness
        x = self.curr_coords[0]
        y = self.curr_coords[1]

        if self.orientation == 0 or 1:
            poly = Polygon([(x,y+n),(x+1,y+n),(x+1,y+1-n),(x,y+1-n),(x,y+n)])
        else:
            poly = Polygon([(x,y+n),(x-1,y+n),(x-1,y+1-n),(x,y+1-n),(x,y+n)])

        return(rotate(poly,np.pi/2*self.orientation,origin = 'center',use_radians=True))

    def corner(self):

        n = self.narrowness
        x = self.curr_coords[0]
        y = self.curr_coords[1]

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

    def construct_track(self, screen_size):

        self.orientation = 0
        self.curr_coords = [0,0]
        track = self.straight()

        self.curr_coords = [1,0]
        for i in range(self.n_elements-1):
        
            random_numb = np.random.choice([-1,0,1], p = [1/4,1/2,1/4])
            if random_numb == -1:
                right_corner = scale(self.corner(),\
                    xfact=1,yfact=-1, origin = (self.curr_coords[0]+1/2,self.curr_coords[1]+1/2))
                rotated_corner = self.rotate_and_translate(right_corner)
                track = track.union(rotated_corner)

            if random_numb == 0:
                track = track.union(self.straight())

            if random_numb == 1:
                left_corner = self.corner()
                rotated_corner = self.rotate_and_translate(left_corner)
                track = track.union(rotated_corner)

            self.orientation = (self.orientation + random_numb)%4

            if self.orientation == 0:
                self.curr_coords[0] += 1
            elif self.orientation == 1:
                self.curr_coords[1] += 1
            elif self.orientation == 2:
                self.curr_coords[0] += -1
            elif self.orientation == 3:
                self.curr_coords[1] += -1

        track_bounds = track.bounds
        x_fact = screen_size[0]/(track_bounds[2]-track_bounds[0]) * 2/3
        y_fact = screen_size[1]/(track_bounds[3]-track_bounds[1]) * 2/3
        factor = min(x_fact,y_fact)

        track_centroid = track.centroid

        track = scale(track, xfact= factor, yfact= factor, origin='centroid')
        track = translate(track, xoff= screen_size[0]/2,yoff = screen_size[1]/2)

        self.starting_position = translate(scale(Point(0.05,0.5),xfact=factor, yfact=factor, origin = track_centroid),\
             xoff= screen_size[0]/2,yoff = screen_size[1]/2)
             
        return track


if __name__ == "__main__":

    track = Track(8, 0.2, np.array((800,600)))
    
    fig, ax = plt.subplots()

    ax.plot(*track.exterior.xy)
    ax.set_aspect('equal', adjustable='box')

    plt.show()

        




