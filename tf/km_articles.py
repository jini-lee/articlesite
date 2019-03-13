from tf.mongo_connector import get_mg_client
from konlpy.tag import Mecab

class KmArticles:
    kind_of_working = {
            'by_flow' : 101,
            'thematic' : 102
            }
    client = get_mg_client()
    def __init__(self, _date, _collection, _kind):
        self._date = _date
        self._collection = client[_collection] 
        self.kind_working = kind_of_working[_kind]


