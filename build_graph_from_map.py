import matplotlib.image
import matplotlib.pyplot as plt
from simulator_objects import Node
from a_star import a_star
from functions import *
from GLOBALS import *


def set_nei(name_1, name_2, nodes_dict):
    if name_1 in nodes_dict and name_2 in nodes_dict and name_1 != name_2:
        node1 = nodes_dict[name_1]
        node2 = nodes_dict[name_2]
        dist = distance_nodes(node1, node2)
        if dist == 1:
            node1.neighbours.append(node2.ID)
            node2.neighbours.append(node1.ID)


def build_graph_from_png(img_png, path='maps', show_map=False):
    img_np = torchvision.io.read_image(f'{path}/{img_png}', ImageReadMode.GRAY).squeeze().numpy()
    max_num = np.max(img_np)
    img_filtered_np = np.where(img_np < max_num, 0, 1)

    return build_graph_from_np(img_filtered_np, show_map)


def build_graph_from_np(img_np, show_map=False):
    # 0 - wall, 1 - free space
    nodes = []
    nodes_dict = {}

    if show_map:
        plt.imshow(img_np, cmap='gray')
        plt.show()
        # plt.pause(1)
        # plt.close()

    x_size, y_size = img_np.shape
    # CREATE NODES
    for i_x in range(x_size):
        for i_y in range(y_size):
            if img_np[i_x, i_y] == 1:
                node = Node(f'{i_x}_{i_y}', i_x, i_y, [])
                nodes.append(node)
                nodes_dict[node.ID] = node

    # CREATE NEIGHBOURS
    name_1, name_2 = '', ''
    for i_x in range(x_size):
        for i_y in range(y_size):
            name_2 = f'{i_x}_{i_y}'
            set_nei(name_1, name_2, nodes_dict)
            name_1 = name_2

    print('finished rows')

    for i_y in range(y_size):
        for i_x in range(x_size):
            name_2 = f'{i_x}_{i_y}'
            set_nei(name_1, name_2, nodes_dict)
            name_1 = name_2

    print('finished columns')

    return nodes


def main():
    # image_name = 'den520d.png'
    # image_name = 'hrt201d.png'
    # image_name = 'Berlin_1_256.png'
    image_name = '10_10_random.png'
    # nodes = build_graph_from_png(image_name, show_map=True)
    nodes = build_graph_from_png(image_name)
    # nodes = build_graph_from_np(img_np, show_map=False)

    node_start, node_goal = np.random.choice(nodes, size=2)

    result = a_star(start=node_start, goal=node_goal, nodes=nodes)

    # PLOT RESULTS:

    # plot field
    x_list = [node.x for node in nodes]
    y_list = [node.y for node in nodes]
    plt.scatter(x_list, y_list)

    # plot found path
    if result is not None:
        parent = result[0]
        successor = parent
        for node in result:
            parent = node
            # plt.text(node.x, node.y, f'{node.ID}', bbox={'facecolor': 'yellow', 'alpha': 1, 'pad': 10})
            plt.plot([successor.x, parent.x], [successor.y, parent.y], color='red')
            successor = node

    plt.show()


if __name__ == '__main__':
    main()
