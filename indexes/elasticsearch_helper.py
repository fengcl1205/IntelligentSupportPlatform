from elasticsearch.helpers import bulk
from elasticsearch_dsl import Search
# from elasticsearch_dsl.connections import connections
import os
from elasticsearch import Elasticsearch
from indexes import constants_manager as cm
from commonUtil import path_helper as ph
from commonUtil import log_helper


class ElasticsearchHelper:
    def __init__(self, index_name, index_type, user_name=None, password=None, port=None, ip="127.0.0.1"):
        """
        :param index_name:
        :param index_type:
        :param user_name:
        :param password:
        :param port:
        :param ip:
        """
        try:
            self.index_name = index_name
            self.index_type = index_type
            self.ip = ip
            # 无用户名密码状态
            if not user_name:
                self.es = Elasticsearch([ip])
            else:
                # 用户名密码状态
                self.es = Elasticsearch([ip], http_auth=(user_name, password), port=port)
        except Exception as e:
            log_helper.log_out('error', 'File: ' + e.__traceback__.tb_frame.f_globals['__file__']
                               + ', lineon: ' + str(e.__traceback__.tb_lineno) + ', error info: ' + str(e))
            raise

    def judge_index_existence(self, index_name):
        try:
            if self.es.indices.exists(index=index_name) is True:
                return True
            else:
                return False
        except Exception as e:
            log_helper.log_out('error', 'File: ' + e.__traceback__.tb_frame.f_globals['__file__']
                               + ', lineon: ' + str(e.__traceback__.tb_lineno) + ', error info: ' + str(e))
            raise

    def create_index(self, cls_obj):
        try:
            if cls_obj is None:
                raise Exception('_index_mappings none')
            if self.judge_index_existence(self.index_name) is True:
                self.es.indices.delete(index=self.index_name)
                log_helper.log_out('info', 'deleting existing indexes')
            cls_obj.init()
        except Exception as e:
            log_helper.log_out('error', 'File: ' + e.__traceback__.tb_frame.f_globals['__file__']
                               + ', lineon: ' + str(e.__traceback__.tb_lineno) + ', error info: ' + str(e))
            raise

    def batch_index_data(self, cls_obj_arr):
        try:
            if cls_obj_arr is None:
                raise Exception('cls array none')
            if len(cls_obj_arr) == 0:
                raise Exception('cls array empty')
            actions = []
            for cls_obj in cls_obj_arr:
                action = dict()
                action['_index'] = self.index_name
                action['_type'] = self.index_type
                data = cls_obj.to_dict()
                action['_source'] = data
                actions.append(action)
            success, _ = bulk(self.es,
                              actions,
                              index=self.index_name,
                              raise_on_error=True)
            print('Performed %d actions' % success)
        except Exception as e:
            log_helper.log_out('error', 'File: ' + e.__traceback__.tb_frame.f_globals['__file__']
                               + ', lineon: ' + str(e.__traceback__.tb_lineno) + ', error info: ' + str(e))
            raise

    def delete_document(self, cls, index_name):
        try:
            if cls is None:
                raise Exception('cls none')

            if not self.es.indices.exists(index=index_name):
                print(index_name + ' dos not exists')
                return
            res = self.es.indices.delete(index=index_name)
            print(res)
        except Exception as e:
            log_helper.log_out('error', 'File: ' + e.__traceback__.tb_frame.f_globals['__file__']
                               + ', lineon: ' + str(e.__traceback__.tb_lineno) + ', error info: ' + str(e))
            raise

    def search_data(self, cls, filter_qs, match_qs):
        try:
            if cls is None:
                raise Exception('cls none')
            s = Search(using=self.es, index=self.index_name)

            if filter_qs is not None and len(filter_qs) > 0:
                for filter_q in filter_qs:
                    s = s.filter(filter_q)
            if match_qs is not None and len(match_qs) > 0:
                for match_q in match_qs:
                    s = s.query(match_q)
            res = s.execute()
            return res
        except Exception as e:
            log_helper.log_out('error', 'File: ' + e.__traceback__.tb_frame.f_globals['__file__']
                               + ', lineon: ' + str(e.__traceback__.tb_lineno) + ', error info: ' + str(e))
            raise
