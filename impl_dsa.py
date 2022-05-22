from GLOBALS import *
from impl_graph_from_map import build_graph_from_png
from functions import *
from impl_local_search_graph import create_local_search_nodes


def calc_dsa(num_of_agents, nodes, nodes_dict, start_nodes, goal_nodes, ls_iters):
    agents_nodes = create_local_search_nodes(num_of_agents, start_nodes, goal_nodes, nodes, nodes_dict)
    paths, solution_bool = run_dsa(agents_nodes, ls_iters)
    return paths, solution_bool


def run_dsa(agents_nodes, ls_iters=10):
    for agent in agents_nodes:
        agent.init()
    for iteration in range(ls_iters):
        # print(f'\riteration: {iteration}', end='')
        for agent in agents_nodes:
            agent.send_messages(iteration)
        for agent in agents_nodes:
            agent.dsa_update_path(iteration)

    # paths: {'agent name': [(x, y, t), ...], ...}
    # print()
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
    # agents_nodes = create_local_search_nodes(n_agents, start_nodes, goal_nodes, nodes, nodes_dict)
    # paths, solution_bool = run_dsa(agents_nodes)  # paths: {'agent name': [(x, y, t), ...], ...}
    paths, solution_bool = calc_dsa(n_agents, nodes, nodes_dict, start_nodes,  goal_nodes, n_iterations)
    print('There is Solution!😄') if solution_bool else print('No Solution ❌')
    print(f'seed: {seed}')
    # plot_paths(paths, nodes, nodes_dict, plot_field=False)
    plot_paths_moving(paths, nodes, nodes_dict, plot_field=True)


if __name__ == '__main__':
    n_agents = 13
    n_iterations = 10
    # with_seed = False
    with_seed = True
    # seed = 211
    seed = random.randint(0, 10000)
    # IMAGE_NAME = '9_10_no_obstacles.png'
    IMAGE_NAME = '19_20_warehouse.png'
    main()