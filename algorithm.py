import heapq
import numpy as np
import matplotlib.pyplot as plt


def available_neighbours(coord_pairs, current_x, current_y, current_z):
    return list(zip(
        coord_pairs.loc[(coord_pairs.x1 == current_x) & (coord_pairs.y1 == current_y) & (coord_pairs.z1 == current_z)][
            ["x2"]].x2,
        coord_pairs.loc[(coord_pairs.x1 == current_x) & (coord_pairs.y1 == current_y) & (coord_pairs.z1 == current_z)][
            ["y2"]].y2,
        coord_pairs.loc[(coord_pairs.x1 == current_x) & (coord_pairs.y1 == current_y) & (coord_pairs.z1 == current_z)][
            ["z2"]].z2))


def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2)


def astar(start, goal, coord_pairs):
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))

    while oheap:

        current = heapq.heappop(oheap)[1]
        neighbours = available_neighbours(coord_pairs, current[0], current[1], current[2])

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)

        for neighbour in neighbours:

            tentative_g_score = gscore[current] + heuristic(current, neighbour)

            if neighbour in close_set and tentative_g_score >= gscore.get(neighbour, 0):
                continue

            if tentative_g_score < gscore.get(neighbour, 0) or neighbour not in [i[1] for i in oheap]:
                came_from[neighbour] = current
                gscore[neighbour] = tentative_g_score
                fscore[neighbour] = tentative_g_score + heuristic(neighbour, goal)
                heapq.heappush(oheap, (fscore[neighbour], neighbour))

    return False


def graphroute(route, goal, nodes, start):
    x_coords = []
    y_coords = []
    z_coords = []

    for i in (range(0, len(route))):
        x = route[i][0]
        y = route[i][1]
        z = route[i][2]

        x_coords.append(x)
        y_coords.append(y)
        z_coords.append(z)

    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)
    z_coords = np.array(z_coords)

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')

    #x_trace = []
    #y_trace = []
    #z_trace = []

    #for node in nodes:
    #    ax.scatter3D(node[0], node[1], node[2], marker="o", color="black", s=1)
        #x_trace.append(node[0])
        #y_trace.append(node[1])
        #z_trace.append(node[2])


    ax.scatter3D(goal[0], goal[1], goal[2], marker="*", color="green", s=100)
    ax.scatter3D(start[0], start[1], start[2], marker="*", color="red", s=100)
    ax.plot3D(x_coords, y_coords, z_coords, color="blue")
    #ax.plot3D(x_trace, y_trace, z_trace, alpha=0.5, color="gray")
    
    #plt.grid(color='gray', linestyle='-', linewidth=0.5)
    plt.show()

    return False