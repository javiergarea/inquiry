from elasticsearch_dsl import Search, Q
from search_engine.elastic_connection import ElasticConnection


class InquiryService:

    def __init__(self):
        self.es = ElasticConnection().connection

    def search_by_keywords(self, keywords):
        search = Search(using=self.es,
                   index="arxiv-index").query("match",
                                              pdf=keywords)
        search = search.source(['title','authors', 'subject', 'other_subjects'])
        search = search.highlight_options(order='score')
        search = search.highlight('pdf', fragment_size=200)
        suggestion = search.suggest('suggestion', keywords, term={'field': 'pdf'})
        request = search.execute()
        for hit in request:
            response = hit.to_dict()
            response.update({'fragment': hit.meta.highlight.pdf}) 
            yield response

    def search_by_fields(self, title, authors, subject, abstract, content):
        search = Search(using=self.es, index="arxiv-index")
        query_title = Q("match", title=title)
        query_authors = Q("match", authors=authors)
        query_subject = Q("match", subject=subject)
        query_abstract = Q("match", abstract=abstract)
        query_content = Q("match", pdf=content)
        final_query = Q('bool',
              should=[query_title, query_authors, query_subject, query_abstract, query_content],
              minimum_should_match=1
        )
        search = search.query(final_query)
        search = search.highlight_options(order='score')
        search = search.highlight('pdf', fragment_size=200)
        request = search.execute()

        for hit in request:
            response = hit.to_dict()
            response.update({'fragment': hit.meta.highlight.pdf}) 
            yield response
