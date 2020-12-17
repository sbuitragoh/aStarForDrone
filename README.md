# A* Algorithm for drones in closed spaces

In this project, there's an approximation of the behaviour of a drone in a closed space following a route given via A* Algorithm.
The motor's speed are only a state, not a specific value to link the chosen motor; it's still a pending work to link this values to a given drone and make the communication work. 

The 'path_to_boxes.txt' file makes the restrictions for the volume that represent the closed space in which the drone will flight. Each line gives the oposite coordinates of an imaginary box that will be removed from the whole graph structure. It's important to write first the coordinates that are closer to the origin, then the oposite of that box (being the first three digits x1, y1, z1 and the following x2, y2, z2).

This was developed as a Project for 'Automatización de Procesos de Manufactura' course in the Universidad Nacional de Colombia.

## Requirements

The work-station that was used in this implementation are the following:

    CPU: Intel(R) Core™ i7-4700HQ @ 2.40 GHz
    RAM: 8 GB
    GPU: NVIDIA GeForce 750M
    OS: Win 10 Home 20H2 19042.685

Also Python 3.7.9 was used with the following libraries:

    pandas 1.1.4
    math
    vg 1.9.0
    matplotlib 3.3.2
    heapq
    numpy 1.19.3
    decimal
    itertools

If the version is not referenced, it must be integrated in the given Python version. Still, it's important to verify these libraries.

Even if it shouldn't matter, the IDE used was PyCharm Community Edition 2020.2.4 x64.
