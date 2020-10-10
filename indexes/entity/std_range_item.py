from elasticsearch_dsl import Document, Keyword, Text
from commonUtil import yaml_helper
import os
from commonUtil import path_helper as ph


project_base_path = ph.get_local_project_path(os.path.dirname(os.path.abspath(__file__)), 2)
path_config = yaml_helper.get_data_from_yaml(
    os.path.join(project_base_path, 'config/normal.yaml'))


class StdRangeItem(Document):
    # range_code = Keyword()
    # range_version = Keyword()
    # range_type = Keyword()
    std_code = Keyword()
    std_name = Text(analyzer='snowball')

    class Index:
        name = path_config['index']['range_matching']['index_name']

    # class Meta:
    #     index = path_config['index']['range_matching']['index_name']
    #     doc_type = path_config['index']['range_matching']['doc_type']
