from GLOBALS import *


def save_metrics(IMAGE_NAME, algs_to_run, k_runs, from_n_agents, to_n_agents, soc_dict, success_rate_dict, running_time_dict):
    big_dict = {
        'from_n_agents': from_n_agents,
        'to_n_agents': to_n_agents,
        'soc_dict': soc_dict,
        'success_rate_dict': success_rate_dict,
        'running_time_dict': running_time_dict,
    }

    time_now = datetime.now()
    algs_names = ''
    for alg_name in algs_to_run:
        algs_names += f'__{alg_name}'
    file_name = f"logs_for_graphs/{time_now}_k_runs__{k_runs}_algs{algs_names}_map__{IMAGE_NAME[:-4]}.json"
    out_file = open(file_name, "w")
    json.dump(big_dict, out_file, indent=4)
    out_file.close()
    return file_name


def load_metrics(file_name):

    file = open(f'{file_name}',)
    big_dict = json.load(file)

    from_n_agents = big_dict['from_n_agents']
    to_n_agents = big_dict['to_n_agents']
    soc_dict = big_dict['soc_dict']
    success_rate_dict = big_dict['success_rate_dict']
    running_time_dict = big_dict['running_time_dict']

    return from_n_agents, to_n_agents, soc_dict, success_rate_dict, running_time_dict


def main():
    pass


if __name__ == '__main__':
    main()
