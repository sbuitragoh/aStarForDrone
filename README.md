# A* Algorithm for drones in closed spaces

In this project, there's an approximation of the behaviour of a drone in a closed space following a route given via A* Algorithm.
The motor's speed are only a state, not a specific value to link the chosen motor; it's still a pending work to link this values to a given drone and make the communication work. 

The 'path_to_boxes.txt' file makes the restrictions for the volume that represent the closed space in which the drone will flight. Each line gives the oposite coordinates of an imaginary box that will be removed from the whole graph structure. It's important to write first the coordinates that are closer to the origin, then the oposite of that box (being the first three digits x1, y1, z1 and the following x2, y2, z2).

