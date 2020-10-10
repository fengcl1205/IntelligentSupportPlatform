import os
from commonUtil import path_helper as ph


def query_range_list():
    data_list = list()
    base_path = ph.get_local_project_path(
        os.path.abspath(os.path.dirname(__file__)), 2)
    with open(os.path.join(base_path, 'rangeMatching/config', 'model_range_mapping.txt'), 'r', encoding='utf-8') as ps:
        range_types = ps.read().split('\n')
        for range_type in range_types:
            range_type = range_type.split('##')
            if len(range_type) != 4:
                continue
            data_dict = dict()
            data_dict['znname'] = range_type[0]
            data_dict['modelcode'] = range_type[1]
            data_dict['rangecode'] = range_type[2]
            data_dict['modellevel'] = range_type[3]
            data_list.append(data_dict)
    return data_list

