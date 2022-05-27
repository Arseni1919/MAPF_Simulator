from GLOBALS import *


def distance_nodes(node1, node2):
    return np.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)


def distance_points(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def get_random_start_and_goal_positions(nodes, n_agents):
    sampled_list = random.sample(nodes, n_agents * 2)
    start_nodes = sampled_list[:n_agents]
    goal_nodes = sampled_list[n_agents:]
    # print(f'start nodes: {[node.ID for node in start_nodes]}')
    # print(f'goal nodes: {[node.ID for node in goal_nodes]}')
    return start_nodes, goal_nodes


def lengthen_paths(paths):
    long_paths = copy.deepcopy(paths)
    max_len = sum([len(v) for k, v in long_paths.items()])

    for agent_name, path in long_paths.items():
        if len(path) < max_len:
            difference = max_len - len(path)
            adding = []
            for i_diff in range(difference):
                new_time = path[-1][2] + i_diff + 1
                adding.append((path[-1][0], path[-1][1], new_time))
            path.extend(adding)
    return long_paths


def get_cost(paths, cost_type='soc'):

    if cost_type == 'soc':
        soc = 0
        for agent_name, path in paths.items():
            soc += len(path)
        return soc

    if cost_type == 'makespan':
        makespan_list = [len(path) for name, path in paths.items()]
        return max(makespan_list)

    if cost_type == 'fuel':
        fuel = 0
        for agent_name, path in paths.items():
            one_path = [(pos[0], pos[1]) for pos in path]
            one_fuel_path = list(set(one_path))
            fuel += len(one_fuel_path)
        return fuel

    return None


def get_collisions(paths):
    big_list = []
    for agent_name, path in paths.items():
        big_list.extend(path)
    counter_list = Counter(big_list)
    no_collisions_bool = len(big_list) == len(set(big_list))
    return counter_list, no_collisions_bool


def get_num_of_collisions(collisions_counter):
    collisions_dict = dict(collisions_counter)
    collisions_dict = {k: v for k, v in collisions_dict.items() if v > 1}
    n_col = sum(v for k, v in collisions_dict.items())
    return n_col


def pprint_counter(big_list, title):
    counter_list = Counter(big_list)
    counter_dict = dict(counter_list)
    counter_dict = {k: v for k, v in counter_dict.items() if v > 1}
    print(f'{title}:')
    pprint(counter_dict)


def check_validity(paths):
    long_paths = lengthen_paths(paths)
    # vertices
    big_vertex_list = []
    for agent_name, path in long_paths.items():
        big_vertex_list.extend(path)
    vertices_bool = len(big_vertex_list) == len(set(big_vertex_list))
    # pprint_counter(big_vertex_list, 'Vertex Conf')

    # edges
    big_edges_list = []
    for agent_name, path in paths.items():
        if len(path) > 1:
            curr_pos = path[0]
            agent_edges_list = []
            for next_pos in path[1:]:
                agent_edges_list.append((next_pos[0], next_pos[1], curr_pos[0], curr_pos[1], next_pos[2]))
                agent_edges_list.append((curr_pos[0], curr_pos[1], next_pos[0], next_pos[1], next_pos[2]))
                curr_pos = next_pos
            # for waiting nodes
            big_edges_list.extend(list(set(agent_edges_list)))
    edges_bool = len(big_edges_list) == len(set(big_edges_list))
    # pprint_counter(big_edges_list, 'Edges Confs')

    solution_bool = vertices_bool and edges_bool

    return paths, solution_bool


def plot_paths_static(paths, nodes, nodes_dict, plot_field=True):
    fig, ax = plt.subplots()
    markers = itertools.cycle(('o', '*', 'p', 'v', '^'))
    marker_dict = {agent_name: next(markers) for agent_name in paths}

    # field positions
    field_x_items = [node.x for node in nodes]
    field_y_items = [node.y for node in nodes]

    # plot field
    if plot_field:
        ax.scatter(field_x_items, field_y_items, marker='s', color='gray', s=100.0, alpha=0.1)
        for node in nodes:
            for nei in node.neighbours:
                ax.plot([node.x, nodes_dict[nei].x], [node.y, nodes_dict[nei].y], linestyle='-', c='gray',
                        alpha=0.1)

    # plot paths
    for agent_name, path in paths.items():
        x_items = [i[0] for i in path]
        y_items = [i[1] for i in path]
        ax.plot(x_items, y_items, linestyle='-', marker=marker_dict[agent_name], markersize=20.0, alpha=0.5)

    plt.show()


def plot_paths_moving(paths, nodes, nodes_dict, plot_field=True):
    max_length = max([len(path) for path in list(paths.values())])
    fig, ax = plt.subplots()
    markers = itertools.cycle(('o', '*', 'p', 'v', '^'))
    marker_dict = {agent_name: next(markers) for agent_name in paths}
    # rate, pause = 1, 1
    rate, pause = 3, 0.005
    # rate, pause = 5, 0.005
    # rate, pause = 10, 0.005

    # plot field
    field_x_items = [node.x for node in nodes]
    field_y_items = [node.y for node in nodes]

    for i_frame in range(max_length * rate):
        ax.clear()
        step = int(i_frame / rate)

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f'time: {step}')
        ax.set_xticks(list(range(max(field_x_items) + 1)))
        ax.set_yticks(list(range(max(field_y_items) + 1)))
        # plot field
        if plot_field:
            # nodes
            ax.scatter(field_x_items, field_y_items, marker='s', color='gray', s=100.0, alpha=0.1)
            # edges
            # for node in nodes:
            #     for nei in node.neighbours:
            #         ax.plot([node.x, nodes_dict[nei].x], [node.y, nodes_dict[nei].y], linestyle='-', c='gray', alpha=0.1)

        # plot paths
        for agent_name, path in paths.items():
            x_items = [i[0] for i in path]
            y_items = [i[1] for i in path]
            ax.plot(x_items, y_items, linestyle='-', marker=marker_dict[agent_name], markersize=20.0, alpha=0.5)

        # plot current position of an agent on a path
        for agent_name, path in paths.items():

            if step < len(path)-1:
                # x_pos = path[i_frame][0]
                # y_pos = path[i_frame][1]
                frac = (i_frame - step * rate)/rate
                x_pos = path[step][0] + frac * (path[step + 1][0] - path[step][0])
                y_pos = path[step][1] + frac * (path[step + 1][1] - path[step][1])
                # print(f'frac: {frac}, frame: {i_frame}, step {step}, rate {rate}')
                ax.text(x_pos, y_pos, f'{agent_name}',
                        dict(size=5), bbox={'facecolor': 'yellow', 'alpha': 1, 'pad': 2})
            else:
                ax.text(path[-1][0], path[-1][1], f'{agent_name}',
                        dict(size=5), bbox={'facecolor': 'yellow', 'alpha': 1, 'pad': 2})

        plt.pause(pause)
    plt.show()


def plot_paths_plotly(paths, nodes, nodes_dict):
    x_items, y_items = [], []
    for agent_name, path in paths.items():
        x_items = [i[0] for i in path]
        y_items = [i[1] for i in path]

    fig = go.Figure(
        data=[go.Scatter(x=x_items, y=y_items, mode='markers')],
        layout=go.Layout(
            xaxis=dict(range=[0, 5], autorange=False),
            yaxis=dict(range=[0, 5], autorange=False),
            title="MAPF Simulation",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None])
                         ]
            )
            ]
        ),
        frames=[go.Frame(data=[go.Scatter(x=[1, 2], y=[1, 2])]),
                go.Frame(data=[go.Scatter(x=[1, 4], y=[1, 4])]),
                go.Frame(data=[go.Scatter(x=[3, 4], y=[3, 4])],
                         layout=go.Layout(title_text="Finished"))]
    )

    fig.show()


