from GLOBALS import *


def distance_nodes(node1, node2):
    return np.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)


def distance_points(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


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
    rate, pause = 5, 0.005
    # rate, pause = 10, 0.005

    # plot field
    field_x_items = [node.x for node in nodes]
    field_y_items = [node.y for node in nodes]

    for i_frame in range(max_length * rate):
        ax.clear()

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
            step = int(i_frame / rate)
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


