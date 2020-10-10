# -*- coding=utf-8 -*-
import yaml


def get_data_from_yaml(yaml_path):
    with open(yaml_path, encoding='utf-8') as normal_file:
        res = yaml.load(normal_file, Loader=yaml.FullLoader)
    return res


def up_yml(yaml_path, file_names, update_values):
    with open(yaml_path, encoding='utf-8') as f:
        doc = yaml.load(f)

    for index in range(len(file_names)):
        doc[file_names[index]] = update_values[index]

    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(doc, f)
