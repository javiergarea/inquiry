import json
from search_engine.elastic_connection import ElasticConnection

JSONL_PATH = 'items.jsonl'


def index_docs(es):
    with open(JSONL_PATH, 'r') as json_file:
        json_list = list(json_file)
    docs = [json.loads(json_str) for json_str in json_list]
    for doc in docs:
        es.index(index='arxiv-index', id=doc.get('doc_id'), body=doc)


if __name__ == "__main__":
    elastic_connection = ElasticConnection().connection
    index_docs(elastic_connection)
