from GLOBALS import *
from functions import *
from impl_graph_from_map import build_graph_from_png
from impl_CA_star import calc_ca_star
from impl_dsa import calc_dsa
from impl_mgm import calc_mgm
from impl_CBS import calc_cbs
from metrics import plot_metrics
from impl_save_metrics import save_metrics, load_metrics

def print_time(title='time'):
    # time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"{title}", current_time)


def create_plot_dict():
    # {alg_name: {n_agents: [list of metrics for every run]}}
    return {alg_name: {i: [] for i in range(from_n_agents, to_n_agents + 1)} for alg_name in algs_to_run}


def main():
    if with_seed:
        np.random.seed(seed)
        random.seed(seed)
        print(f'seed: {seed}')

    # for plots
    soc_dict = create_plot_dict()
    running_time_dict = create_plot_dict()
    memory_dict = create_plot_dict()
    closed_nodes_dict = create_plot_dict()
    success_rate_dict = create_plot_dict()

    nodes, nodes_dict = build_graph_from_png(IMAGE_NAME)
    print_time('Start time')

    # n agents
    for n_agents in range(from_n_agents, to_n_agents + 1):

        # k different runs
        for i_problem in range(k_runs):

            start_nodes, goal_nodes = get_random_start_and_goal_positions(nodes, n_agents)

            # each algorithm
            for alg_name in algs_to_run:

                print(f'\rn_agents: ({n_agents}/{to_n_agents}), run: ({i_problem}/{k_runs}), alg: {alg_name}', end='')
                start = time.time()
                alg = algs_dict[alg_name]
                if alg_name in ['dsa', 'mgm']:
                    paths, solution_bool = alg(n_agents, nodes, nodes_dict, start_nodes, goal_nodes, ls_iters)
                else:
                    paths, solution_bool = alg(n_agents, nodes, nodes_dict, start_nodes, goal_nodes)
                end = time.time()

                # for plots
                success_rate_dict[alg_name][n_agents].append(solution_bool)
                running_time_dict[alg_name][n_agents].append(end - start)
                if solution_bool:
                    # paths: {'agent name': [(x, y, t), ...], ...}
                    soc_dict[alg_name][n_agents].append(sum([len(path) for path in list(paths.values())]))
                else:
                    print(f'\n[ERROR]: {alg_name} failed to solve!')
    print(f'seed: {seed}')
    print_time('Finish time')
    file_name = save_metrics(from_n_agents, to_n_agents, soc_dict, success_rate_dict, running_time_dict)
    from_n, to_n, soc_dict, success_rate_dict, running_time_dict = load_metrics(file_name)
    plot_metrics(from_n, to_n, soc_dict, success_rate_dict, running_time_dict)


if __name__ == '__main__':
    from_n_agents = 2
    # to_n_agents = 13
    to_n_agents = 3
    k_runs = 3
    ls_iters = 5

    IMAGE_NAME = '19_20_warehouse.png'
    with_seed = True
    # seed = 211
    seed = random.randint(0, 10000)

    # algorithms
    algs_to_run = ['ca_star', 'dsa', 'mgm', 'cbs']
    # algs_to_run = ['mgm']
    algs_dict = {
        'dsa': calc_dsa,
        'mgm': calc_mgm,
        'ca_star': calc_ca_star,
        'cbs': calc_cbs,
    }

    main()
