import roomDefinition as roomDef
import algorithm as alg
import motor
import pandas as pd
from collections import OrderedDict
import numpy as np


def drone_route():

    x1, y1, z1, x2, y2, z2, nodes = roomDef.graphofroom(x=17, y=18, z=8, connectivity='full', net_size=0)
    print('Space Defined')

    coord_pairs = pd.DataFrame(OrderedDict((('x1', pd.Series(x1)), ('y1', pd.Series(y1)), ('z1', pd.Series(z1)),
                                            ('x2', pd.Series(x2)), ('y2', pd.Series(y2)), ('z2', pd.Series(z2)))))

    coord_pairs = coord_pairs.sort_values(['x1', 'y1', 'z1'], ascending=[True, True, True])

    # 1,2,1 -> 2,4,2 -> 3,6,3
    # 2,5,5 -> 4,10,10 -> 6, 15,15

    start = (0, 0, 0)
    goal = (16, 9, 0)

    rt_alg = alg.astar(start, goal, coord_pairs)
    rt_alg = rt_alg + [start]
    rt_alg = rt_alg[::-1]
    print('RUTA REALIZADA')
    print(rt_alg)

    alg.graphroute(rt_alg, goal, nodes, start)
    return rt_alg


def vector_from_route(route):
    x = np.shape(route)[0]
    pair_space = []
    list_of_vectors = []

    for i in range(x - 1):
        pair_space.append([np.array(route[i]), np.array(route[i + 1])])

    pair_space = np.reshape(pair_space, (-1, 2, 3))

    for j in range(np.shape(pair_space)[0]):
        list_of_vectors.append(motor.vector_creator(pair_space[j][0], pair_space[j][1]))

    x_v = np.shape(list_of_vectors)[0]

    return x_v, list_of_vectors


if __name__ == "__main__":

    print('Reading Space Setting Files')
    route_drone = drone_route()
    x_dim, lov = vector_from_route(route_drone)

    # MOTOR DECLARATION
    motor_1 = motor.Motor(motor=1, speed=0, mod='None')
    motor_2 = motor.Motor(motor=2, speed=0, mod='None')
    motor_3 = motor.Motor(motor=3, speed=0, mod='None')
    motor_4 = motor.Motor(motor=4, speed=0, mod='None')

    motor.speed_state(motor_1=motor_1,
                      motor_2=motor_2,
                      motor_3=motor_3,
                      motor_4=motor_4,
                      x_v=x_dim,
                      list_of_vectors=lov)
