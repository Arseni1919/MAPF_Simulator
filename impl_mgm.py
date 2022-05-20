from GLOBALS import *
from impl_graph_from_map import build_graph_from_png
from functions import *
from impl_local_search_graph import create_local_search_nodes
from metrics import plot_metrics_for_one_run


def run_mgm(agents_nodes):
    print()
    # initial path (a star)
    for agent in agents_nodes:
        agent.init()
    for iteration in range(n_iterations):
        print(f'\riteration: {iteration}', end='')
        # send paths
        for agent in agents_nodes:
            agent.send_messages(iteration)
        # calculate local reduction
        for agent in agents_nodes:
            agent.mgm_send_lr_messages(iteration)
        # mgm decision
        for agent in agents_nodes:
            agent.mgm_update_path(iteration)

    # paths: {'agent name': [(x, y, t), ...], ...}
    print()
    paths = {agent.name: agent.path for agent in agents_nodes}
    paths, solution_bool = check_validity(paths)
    return paths, solution_bool


def main():
    if with_seed:
        np.random.seed(seed)
        random.seed(seed)
        print(f'seed: {seed}')

    nodes, nodes_dict = build_graph_from_png(IMAGE_NAME)
    start_nodes, goal_nodes = get_random_start_and_goal_positions(nodes, n_agents)
    agents_nodes = create_local_search_nodes(n_agents, start_nodes, goal_nodes, nodes, nodes_dict)
    paths, solution_bool = run_mgm(agents_nodes)  # paths: {'agent name': [(x, y, t), ...], ...}

    print('There is Solution!😄') if solution_bool else print('No Solution ❌')
    print(f'seed: {seed}')
    # plot_paths_moving(paths, nodes, nodes_dict, plot_field=True)
    plot_metrics_for_one_run(paths)


if __name__ == '__main__':
    n_agents = 10
    n_iterations = 5
    with_seed = True
    seed = 6812
    # seed = random.randint(0, 10000)
    # IMAGE_NAME = '9_10_no_obstacles.png'
    IMAGE_NAME = '19_20_warehouse.png'
    main()