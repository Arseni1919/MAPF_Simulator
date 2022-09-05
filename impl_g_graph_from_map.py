import matplotlib.image
import matplotlib.pyplot as plt
import numpy as np

from simulator_objects import Node
from a_star import a_star
from functions import *
from GLOBALS import *
from map_dimensions import map_dimensions_dict


def set_nei(name_1, name_2, nodes_dict):
    if name_1 in nodes_dict and name_2 in nodes_dict and name_1 != name_2:
        node1 = nodes_dict[name_1]
        node2 = nodes_dict[name_2]
        dist = distance_nodes(node1, node2)
        if dist == 1:
            node1.neighbours.append(node2.ID)
            node2.neighbours.append(node1.ID)


def build_graph_from_png(img_png, path='maps', show_map=False):
    img_tensor = torchvision.io.read_image(f'{path}/{img_png}', ImageReadMode.GRAY)
    if img_png in map_dimensions_dict:
        img_np = T.Resize(size=map_dimensions_dict[img_png])(img_tensor).squeeze().numpy()
    else:
        img_np = img_tensor.squeeze().numpy()
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

    # print('finished rows')

    for i_y in range(y_size):
        for i_x in range(x_size):
            name_2 = f'{i_x}_{i_y}'
            set_nei(name_1, name_2, nodes_dict)
            name_1 = name_2

    # print('finished columns')

    return nodes, nodes_dict


def clear_nodes(nodes):
    for node in nodes:
        node.parent = None
        node.g = 0
        node.h = 0
        node.t = 0


def create_direct_h_bfs_dist(image_name, nodes, nodes_dict):
    x_dim, y_dim = map_dimensions_dict[image_name]
    h_func = np.zeros((x_dim, y_dim, x_dim, y_dim))
    print(f'nodes: {len(nodes)}')
    for i_1, node1 in enumerate(nodes):

        if i_1 % 50:
            print(f'\r->{i_1 + 1}', end='')
        # run BFS
        clear_nodes(nodes)
        open_list = [node1]
        closed_list = []
        while len(open_list) > 0:
            curr_node = open_list.pop(0)
            if curr_node not in closed_list:
                # update h_func
                h_func[node1.x][node1.y][curr_node.x][curr_node.y] = curr_node.g
                # h_func[curr_node.x][curr_node.y][node1.x][node1.y] = curr_node.g
                # add new members to open list
                for nei_name in curr_node.neighbours:
                    nei_node = nodes_dict[nei_name]
                    nei_node.g = curr_node.g + 1
                    open_list.append(nei_node)
                # add current node to the closed list
                closed_list.append(curr_node)
    return h_func


def build_h_func(nodes, nodes_dict, image_name):
    # h_func[f'{node1.x}_{node1.y}'][f'{node2.x}_{node2.y}']
    print('Starting to create h_func..')
    outfile = f'heuristics/{image_name[:-4]}.npy'
    if exists(outfile):
        print('Finished h_func.')
        return np.load(outfile)

    # init h_func with BFS
    h_func = create_direct_h_bfs_dist(image_name, nodes, nodes_dict)

    np.save(outfile, h_func)
    print('\nFinished h_func.')
    return h_func


def main():

    # image_name = 'den520d.png'
    # image_name = 'hrt201d.png'
    # image_name = 'Berlin_1_256.png'
    # image_name = '10_10_random.png'
    image_name = 'lak108d.png'
    image_name = 'lak109d.png'
    image_name = 'lak110d.png'
    image_name = 'hrt201d.png'
    image_name = 'den520d.png'
    image_name = 'lak505d.png'
    image_name = '9_10_no_obstacles.png'
    image_name = '19_20_warehouse.png'
    image_name = 'rmtst.png'
    nodes, nodes_dict = build_graph_from_png(image_name)
    dim_x, dim_y = map_dimensions_dict[image_name]
    node_start, node_goal = np.random.choice(nodes, size=2)
    result = a_star(start=node_start, goal=node_goal, nodes=nodes)
    print('finished calculating path')

    # PLOT RESULTS:
    mat = np.zeros((dim_x, dim_y))
    for node in nodes:
        mat[node.x, node.y] = 1
    plt.imshow(mat.T, origin="lower")
    plt.tight_layout()

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


    # plot nodes
    # x_list = [node.x for node in nodes]
    # y_list = [node.y for node in nodes]
    # print(f'max y: {max(y_list)}\n|\n|\n__ __ __ max x: {max(x_list)}')
    # print(f'n nodes: {len(nodes)}')
    # plt.scatter(x_list, y_list, marker='s', color='gray', s=2.0, alpha=0.1)

    # plot edges
    # for node in nodes:
    #     for nei in node.neighbours:
    #         plt.plot([node.x, nodes_dict[nei].x], [node.y, nodes_dict[nei].y], linestyle='-', c='gray', alpha=0.1)



if __name__ == '__main__':
    main()
