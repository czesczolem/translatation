from elasticsearch_dsl import Search
import json

class Elasticsearcher:
    def __init__(self, es, index):
        self.es = es
        self.index = index

    def search(self, **kwargs):
        s = Search(index=self.index).using(self.es).query("match", kwargs)
        return s.execute()