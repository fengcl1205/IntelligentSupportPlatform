from commonUtil import path_helper as ph
from commonUtil import log_helper
import os
from indexes.elasticsearch_helper import ElasticsearchHelper as Eh
from indexes.entity import std_range_item as sri
from indexes import constants_manager as cm


def data_sources():
    res = list()
    res = ['面对手机的屏幕', '每人一句贺词', '大家品美食', '古往今来', '在金秋桂花旁', '浓浓的亲情']
    return res


def es_init():
    try:
        project_base_path = ph.get_local_project_path(os.path.dirname(os.path.abspath(__file__)), 1)
        path_config = os.path.join(project_base_path, 'config/normal.yaml')
        host = cm.get_es_host(path_config)
        port = cm.get_es_port(path_config)
        index_name = cm.get_es_index_name(path_config)
        index_type = cm.get_es_doc_type(path_config)
        es_obj = Eh(index_name, index_type, user_name=None, password=None, port=port, ip=host)

        log_helper.log_out('info', 'start Retrieve initialization')
        # 创建索引结构
        es_obj.create_index(sri.StdRangeItem())
        datas = list()
        # 业务数据来源
        business_data = data_sources()
        for ele in business_data:
            _sri = sri.StdRangeItem()
            _sri.std_name = ele
            datas.append(_sri)
        # 批量插入数据
        es_obj.batch_index_data(datas)
        log_helper.log_out('info', 'Retrieve initialization Success')

    except Exception as e:
        log_helper.log_out('error', 'File: ' + e.__traceback__.tb_frame.f_globals['__file__']
                           + ', lineon: ' + str(e.__traceback__.tb_lineno) + ', error info: ' + str(e))

'''
def es_search(query_content):
    project_base_path = ph.get_local_project_path(os.path.dirname(os.path.abspath(__file__)), 1)
    path_config = os.path.join(project_base_path, 'config/normal.yaml')
    host = cm.get_es_host(path_config)
    port = cm.get_es_port(path_config)
    index_name = cm.get_es_index_name(path_config)
    index_type = cm.get_es_doc_type(path_config)
    # _index_mappings = []
    from elasticsearch import Elasticsearch
    es = Elasticsearch([host], port=port)
    doc = {
        "query": {
            "match": {
                "std_name": query_content
            }
        }
    }
    _searched = es.search(index=index_name, doc_type=index_type, body=doc)
    path = 'D:/GitRepository/IntelligentSupportPlatform/data/range_items/res.txt'
    # file = open(path, 'w', encoding='utf-8')
    if not _searched['hits']['hits']:
        return None
    res = list()
    for hit in _searched['hits']['hits']:
        res.append(hit['_source']['std_name'])
        return res
        # print hit['_source']0
        # print(query_content, '  ' +hit['_source']['range_item'])
    #     ss = hit['_source']['range_item']
    #     # file.write(query_content +'    ' + ss + ' \n')
    #     file.write(query_content+ ' \n')
    # file.close()
'''


def es_search(search_text):
    ss = ''
    project_base_path = ph.get_local_project_path(os.path.dirname(os.path.abspath(__file__)), 1)
    path_config = os.path.join(project_base_path, 'config/normal.yaml')
    host = cm.get_es_host(path_config)
    port = cm.get_es_port(path_config)
    index_name = cm.get_es_index_name(path_config)
    index_type = cm.get_es_doc_type(path_config)
    es_obj = Eh(index_name, index_type, user_name=None, password=None, port=port, ip=host)
    _sri = sri.StdRangeItem()
    filters = list()
    from elasticsearch_dsl import Q
    # filters.append(Q('term', range_code=range_code))
    # filters.append(Q('term', range_version=range_version))
    matchings = list()
    matchings.append(Q('match', std_name=search_text))
    search_res = es_obj.search_data(_sri, filters, matchings)
    return search_res

# es_init()

# ss = es_search('大家品')
# print(ss)

