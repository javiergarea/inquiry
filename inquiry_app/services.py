from elasticsearch_dsl import Search, Q
from search_engine.elastic_connection import ElasticConnection


class InquiryService:

    def __init__(self):
        self.es = ElasticConnection().connection

    def search_by_keywords(self, keywords):
        s = Search(using=self.es,
                   index="arxiv-index").query("match",
                                              pdf=keywords)
        s.execute()
        for hit in s:
            yield hit.title

    def search_by_fields(self, title, authors, subject, abstract, content):
        s = Search(using=self.es, index="arxiv-index")
        if authors:
            q = Q("multi_match", query=authors, fields=['authors'])
            s = s.query(q)
        if title:
            q = Q("multi_match", query=title, fields=['title'])
            s = s.query(q)
        if subject:
            q = Q("multi_match", query=subject, fields=['subject'])
            s = s.query(q)
        if abstract:
            q = Q("multi_match", query=abstract, fields=['abstract'])
            s = s.query(q)
        s.execute()

        for hit in s:
            yield hit.title
