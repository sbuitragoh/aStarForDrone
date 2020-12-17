import numpy as np
import decimal
import itertools


def graphofroom(**kwargs):

    x = kwargs['x']
    y = kwargs['y']
    z = kwargs['z']
    connectivity = kwargs['connectivity']
    net_size = kwargs['net_size']

    print('El area neta de trabajo es: ' + str(x) + ' x ' + str(y) + ' x ' + str(z) + ' metros.')

    x1 = []
    y1 = []
    z1 = []
    x2 = []
    y2 = []
    z2 = []

    x_decimal = np.abs(decimal.Decimal(str(x)).as_tuple().exponent)
    y_decimal = np.abs(decimal.Decimal(str(y)).as_tuple().exponent)
    z_decimal = np.abs(decimal.Decimal(str(z)).as_tuple().exponent)

    decimal_places = [x_decimal, y_decimal, z_decimal]
    max_multiplication = max(decimal_places)

    x_nodes = x * (10 ** max_multiplication)
    y_nodes = y * (10 ** max_multiplication)
    z_nodes = z * (10 ** max_multiplication)

    x_array = [i for i in range(x_nodes + net_size*x_nodes + 1)]
    y_array = [j for j in range(y_nodes + net_size*y_nodes + 1)]
    z_array = [k for k in range(z_nodes + net_size*z_nodes + 1)]

    perm_with_repetition = [p for p in itertools.product(x_array, y_array, z_array)]

    if connectivity == 'full':
        connection_box = [q for q in itertools.product([-1, 0, 1], repeat=3)]
    else:
        connection_box = [(0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, -1), (0, -1, 0), (-1, 0, 0)]

    simplified_nodes = boxesinroom(path='./path_boxes.txt', nodes=perm_with_repetition)

    for current_node in simplified_nodes:
        list_of_connected_nodes = []
        for current_connection in connection_box:
            node_connection = (current_node[0] + current_connection[0],
                               current_node[1] + current_connection[1],
                               current_node[2] + current_connection[2])

            if node_connection in simplified_nodes:
                if node_connection not in list_of_connected_nodes:
                    list_of_connected_nodes.append(node_connection)

        list_of_connected_nodes.sort(key=lambda node: node)

        for listed_node in list_of_connected_nodes:
            x1.append(current_node[0])
            y1.append(current_node[1])
            z1.append(current_node[2])
            x2.append(listed_node[0])
            y2.append(listed_node[1])
            z2.append(listed_node[2])

    return x1, y1, z1, x2, y2, z2, simplified_nodes


def boxesinroom(**kwargs):

    path = kwargs['path']
    nodes = kwargs['nodes']
    del_boxes = []
    box_points = []

    with open(path) as restrictions:
        for line in restrictions:
            pos = line.split(',')

            x_range = [i for i in range(int(pos[0]), int(pos[3]) + 1)]
            y_range = [j for j in range(int(pos[1]), int(pos[4]) + 1)]
            z_range = [k for k in range(int(pos[2]), int(pos[5]) + 1)]

            for point in itertools.product(x_range, y_range, z_range):
                box_points.append(point)

        for node in nodes:
            if node not in box_points:
                if node not in del_boxes:
                    del_boxes.append(node)

        print('')
    return del_boxes
