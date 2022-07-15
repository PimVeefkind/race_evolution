import numpy as np

from shapely.geometry import Point, LineString
from shapely.ops import nearest_points, split

class Agent():

    def __init__(self,n, start_pos, timestep):

        self.id = n
        self.is_dead = False

        self.position = np.array(start_pos)
        self.velocity = np.random.rand(2)*np.array((3,np.random.choice((-1,1))))
        self.dt = timestep

        self.n_sight_lines = 8
        self.distances = np.zeros(self.n_sight_lines)
        self.sight_lines = [ [] for _ in range(self.n_sight_lines) ]
        

    def move(self, track):

        self.position += self.dt*self.velocity

        if not track.track.contains(Point(self.position)):
            self.is_dead = True
        
        else:
            self.calculate_surroundings(track)

    def on_center_line(self,track):

        ag_end = Point(self.position)
        pos_on_line, _ = nearest_points(track.center_line_shapely,ag_end)

        #print(list(pos_on_line.coords)[0], self.position,list(track.center_line_shapely.coords))
        return(list(pos_on_line.coords)[0])
        
        

    def calculate_surroundings(self,track):

        angles = np.arange(0,2*np.pi,2/self.n_sight_lines*np.pi)
        position = Point(self.position)

        for i,angle in enumerate(angles):

            direction = np.array((np.sin(angle),np.cos(angle)))
            aux_point = (self.position+2000*direction)
            aux_line = LineString([self.position,aux_point])
            intersections = track.track.exterior.intersection(aux_line)
            distance = position.distance(intersections)

            if intersections.geom_type == 'Point':
                self.sight_lines[i] = [self.position,list(intersections.coords)[0]]

            else:
                self.sight_lines[i] = [self.position,self.position+distance*direction]
            
            self.distances[i] = distance
            