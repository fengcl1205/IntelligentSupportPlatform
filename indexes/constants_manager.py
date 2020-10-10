from functools import lru_cache
from commonUtil import yaml_helper as yh


# @lru_cache(maxsize=2)
def get_es_host(yaml_path):
    res = _get_yaml_file(yaml_path)
    return res['db']['es']['host']


# @lru_cache(maxsize=2)
def get_es_port(yaml_path):
    res = _get_yaml_file(yaml_path)
    return res['db']['es']['port']


# @lru_cache(maxsize=2)
def get_es_index_name(yaml_path):
    res = _get_yaml_file(yaml_path)
    return res['index']['range_matching']['index_name']


# @lru_cache(maxsize=500)
def get_es_doc_type(yaml_path):
    res = _get_yaml_file(yaml_path)
    return res['index']['range_matching']['doc_type']


# @lru_cache(maxsize=20)
def _get_yaml_file(yaml_path):
    res = yh.get_data_from_yaml(yaml_path)
    return res
