import numpy as np

from GLOBALS import *
from functions import distance_points, distance_nodes
from impl_save_metrics import load_metrics


def get_collisions(agents):
    count = 0
    for agent1 in agents:
        for agent2 in agents:
            dist = distance_nodes(agent1, agent2)
            if dist == 0:
                count += 1
    return count


def get_er_loss(er_real, er_hat):
    """loss = sum(abs(er - second_graph_dict))"""
    er_loss = 0
    er_hat_dict = {(pos.x, pos.y): pos for pos in er_hat}
    for er_pos in er_real:
        er_pos_req = er_pos.req
        er_pos_req_hat = er_hat_dict[(er_pos.x, er_pos.y)].req
        er_loss += abs(er_pos_req_hat - er_pos_req)
    return er_loss


def get_sum_jc(x, y, agents):
    creds = 0
    for agent in agents:
        if distance_points(x, y, agent.x, agent.y) <= agent.sr:
            creds += agent.cred
    return creds


def get_objective(er_real, agents):
    """objective of a new dcop_mst model"""
    objective = 0
    for er_pos in er_real:
        objective += max(0, er_pos.req - get_sum_jc(er_pos.x, er_pos.y, agents))
    return objective


def get_tags(alg_list, other_tags=None):
    tags = ['MAS_simulator']
    for alg in alg_list:
        tags.append(alg.name)
    if other_tags:
        for tag in other_tags:
            tags.append(tag)
    return tags


class NeptunePlotter:
    """
    Neptune + final plots
    """
    def __init__(self, plot_neptune=False, tags=None, name='check'):
        # NEPTUNE
        self.plot_neptune = plot_neptune
        self.tags = [] if tags is None else tags
        self.name = name
        self.run = {}
        self.neptune_initiated = False
        self.neptune_init()

        # FINAL PLOTS
        self.remained_coverage_dict = {}

    def neptune_init(self, params=None):
        if params is None:
            params = {}

        if self.plot_neptune:
            self.run = neptune.init(project='1919ars/MA-implementations',
                                    tags=self.tags,
                                    name=f'{self.name}')

            self.run['parameters'] = params
            self.neptune_initiated = True

    def neptune_plot(self, update_dict: dict):
        if self.plot_neptune:

            if not self.neptune_initiated:
                raise RuntimeError('~[ERROR]: Initiate NEPTUNE!')

            for k, v in update_dict.items():
                self.run[k].log(v)

    def neptune_close(self):
        if self.plot_neptune and self.neptune_initiated:
            self.run.stop()

    def update_metrics(self, update_dict: dict):
        pass

    def update_metrics_and_neptune(self, update_dict: dict):
        """use it if the dict is the same for both methods"""
        self.update_metrics(update_dict)
        self.neptune_plot(update_dict)


def plot_metrics(from_n_agents, to_n_agents, soc_dict, success_rate_dict, running_time_dict):
    """
    Metrics:
    - solution length (SoC - sum of costs)
    - running time
    - memory
    - number of open nodes during the search
    # {alg_name: {n_agents: [list of metrics for every run]}}
    """
    # to print:
    for alg_name, n_dict in success_rate_dict.items():
        print('---')
        for i in range(from_n_agents, to_n_agents + 1):
            print(f'{alg_name} for {i} agents: {sum(n_dict[str(i)]) / len(n_dict[str(i)]) * 100: .2f} %')

    # to plot
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))

    # SoC / makespan / fuel
    for alg_name, n_dict in soc_dict.items():
        x, y, std = [], [], []
        for i in range(from_n_agents, to_n_agents + 1):
            x.append(i)
            y.append(np.mean(n_dict[str(i)]))
            std.append(np.std(n_dict[str(i)]))

        x = np.array(x)
        y = np.array(y)
        std = np.array(std)
        ax1.plot(x, y, label=f'{alg_name}')
        ax1.fill_between(x, y + std, y - std, alpha=0.05)
        ax1.set_xticks(x)
    ax1.set_ylabel('sum of costs')
    ax1.set_title("SoC")
    ax1.legend()

    # running time
    for alg_name, n_dict in running_time_dict.items():
        x, y, std = [], [], []
        for i in range(from_n_agents, to_n_agents + 1):
            x.append(i)
            if alg_name in ['dsa', 'mgm']:
                time_to_run_each_problem = np.array(n_dict[str(i)]) / i
            else:
                time_to_run_each_problem = np.array(n_dict[str(i)])
            y.append(np.mean(time_to_run_each_problem))
            std.append(np.std(time_to_run_each_problem))

        x = np.array(x)
        y = np.array(y) * 1000
        ax2.plot(x, y, label=f'{alg_name}')
        # std = np.array(std) * 1000
        # ax2.fill_between(x, y + std, y - std, alpha=0.1)
        ax2.set_xticks(x)
    ax2.set_ylabel('running time')
    ax2.set_title("Running Time (milliseconds)")
    ax2.legend()

    # memory
    x = np.linspace(0, 2 * np.pi, 400)
    y = np.sin(x ** 2)
    ax3.plot(x + 1, y + 1)
    ax3.set_title("unrelated")

    # open nodes during the search
    x = np.linspace(0, 2 * np.pi, 400)
    y = np.sin(x ** 2)
    ax4.plot(x + 2, y + 2)
    ax4.set_title("also unrelated")

    # fig.tight_layout()
    plt.show()


def main():
    from_n, to_n, soc_dict, success_rate_dict, running_time_dict = load_metrics(file_name)
    plot_metrics(from_n, to_n, soc_dict, success_rate_dict, running_time_dict)


if __name__ == '__main__':
    # file_name = '2022-05-29 10:00:39.516168_k_runs__20_algs__ca_star__dsa__mgm_map__rmtst.json'
    # file_name = '2022-05-29 10:19:05.913659_k_runs__20_algs__ca_star__dsa__mgm_map__19_20_warehouse.json'
    # file_name = '2022-05-29 10:23:18.514116_k_runs__20_algs__ca_star__dsa__mgm__cbs_map__19_20_warehouse.json'
    # file_name = '2022-05-29 11:13:54.144687_k_runs__20_algs__ca_star__dsa__mgm__cbs_map__lak108d.json'
    file_name = '2022-07-17 12:29:07.288183_k_runs__20_algs__ca_star__dsa_map__den101d.json'

    file_name = f'logs_for_graphs/{file_name}'
    main()

