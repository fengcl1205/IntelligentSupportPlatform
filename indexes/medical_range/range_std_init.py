import os
from indexes.elasticsearch_helper import ElasticsearchHelper as Eh
from commonUtil import path_helper as ph
from indexes import constants_manager as cm
from commonUtil import log_helper
import indexes.entity.std_range_item as Sri


class RangeCodeCls:
    def __init__(self):
        project_base_path = ph.get_local_project_path(os.path.dirname(os.path.abspath(__file__)), 3)
        self.path_config = os.path.join(project_base_path, 'config/normal.yaml')

    def init_structure(self):
        try:
            _es = Eh()
            _es.create_index(Sri.StdRangeItem(), cm.get_es_index_name(self.path_config))
        except Exception as e:
            log_helper.log_out('error', 'File: ' + e.__traceback__.tb_frame.f_globals['__file__']
                               + ', lineon: ' + str(e.__traceback__.tb_lineno) + ', error info: ' + str(e))
            raise

    def init_data(self):
        try:
            project_base_path = ph.get_local_project_path(os.path.dirname(os.path.abspath(__file__)), 1)
            range_standard_dir = os.path.join(project_base_path, 'data', 'range_items')
            for file in os.listdir(range_standard_dir):
                file_path = os.path.join(range_standard_dir, file)

                if os.path.isfile(file_path):
                    datas = list()
                    with open(file_path, 'r', encoding='utf-8') as range_file:
                        filename = os.path.basename(file_path)
                        range_datas = range_file.read().split('\n')
                        for range_data in range_datas:
                            range_data = range_data.split('##')
                            if len(range_data) < 3:
                                continue
                            _sri = Sri.StdRangeItem()
                            _sri.range_code = range_data[0]
                            _sri.range_version = filename[:-4]
                            _sri.std_code = range_data[1]

                            _sri.std_name = range_data[2]
                            datas.append(_sri)
                    Eh().batch_index_data(datas, cm.get_es_index_name(self.path_config),
                                          cm.get_es_doc_type(self.path_config))
        except Exception as e:
            log_helper.log_out('error', 'File: ' + e.__traceback__.tb_frame.f_globals['__file__']
                               + ', lineon: ' + str(e.__traceback__.tb_lineno) + ', error info: ' + str(e))
            raise
