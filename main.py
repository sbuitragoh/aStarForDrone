import roomDefinition as room
import algorithm as alg
import pandas as pd
from collections import OrderedDict

def droneRoute():
    # Call of the General Size of the Room
    # Prints on each step
    # sizeOfRoom(x,y,z) -> x,y,z in meters
    # graphSet(netSize)
    # wallSet(path='file_of_walls')
    # objectSet(path='file_of_objects')
    # interestSet(path='file of interest')
    x1, y1, z1, x2, y2, z2, nodes = room.graphofroom(x=5, y=5, z=5, connectivity='simple', net_size=2)
    print('Space Defined')

    coord_pairs = pd.DataFrame(OrderedDict((('x1', pd.Series(x1)), ('y1', pd.Series(y1)), ('z1', pd.Series(z1)),
                                            ('x2', pd.Series(x2)), ('y2', pd.Series(y2)), ('z2', pd.Series(z2)))))

    coord_pairs = coord_pairs.sort_values(['x1', 'y1', 'z1'], ascending=[True, True, True])

    # 1,2,1 -> 2,4,2 -> 3,6,3
    # 2,5,5 -> 4,10,10 -> 6, 15,15

    start = (3, 6, 3)
    goal = (6, 15, 15)

    route = alg.astar(start, goal, coord_pairs)
    route = route + [start]
    route = route[::-1]
    print('RUTA REALIZADA')
    print(route)

    alg.graphroute(route, goal, nodes, start)


if __name__ == "__main__":

    print('Reading Space Setting Files')
    droneRoute()

    print('')
