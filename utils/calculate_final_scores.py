

from shapely.geometry import Point
from shapely.ops import nearest_points, split

def calculate_final_scores(track, agents):

    final_scores = []

    for agent in agents:
        
        ag_end = Point(agent.position)
        pos_on_line, _ = nearest_points(track.center_line_shapely,ag_end,)
        sub_line = split(track.center_line_shapely, pos_on_line)
        final_scores.append(sub_line[0].length)

    print(final_scores)