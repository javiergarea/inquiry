import json


INDEX_NAME = 'arxiv-index'


class Indexer():

    def __init__(self, es_connection):
        self.es_connection = es_connection

    def index_docs(self, jsonl_path):
        with open(jsonl_path, 'r') as json_file:
            json_list = list(json_file)

        docs = [{key: json.loads(jsonstr)[key] for key in json.loads(jsonstr).keys() &
                {'pdf_url', 'abstract_url', 'doc_id', 'title', 'authors', 'subject',
                 'other_subjects', 'pdf', 'abstract', 'submit_date'}} for jsonstr in json_list]

        for doc in docs:
            self.es_connection.index(index=INDEX_NAME, id=doc.get('doc_id'), body=doc)

    def delete_index(self):
        self.es_connection.indices.delete(index=INDEX_NAME, ignore=[400, 404])
