from elasticsearch_dsl import Search, Q
from search_engine.elastic_connection import ElasticConnection
from elasticsearch_dsl import FacetedSearch, TermsFacet

class InquiryService:

    class SubjectSearch(FacetedSearch):
        # fields that should be searched
        fields = ['subject']

        facets = {
            # use bucket aggregations to define facets
            'subject': TermsFacet(field='subject')
        }

        def search(self):
            # override methods to add custom pieces
            s = super().search()
            query_title = Q("match", title=subject)
            return s.query()

    def __init__(self):
        self.es = ElasticConnection().connection

    def search_by_keywords(self, keywords, subject):
        search = Search(using=self.es, index="arxiv-index")
        query_pdf = Q("match", pdf=keywords)
        query_subject = Q()
        if subject:
            query_subject = Q("wildcard", subject="*"+subject+"*")
        final_query = Q('bool',
              must = [query_subject],
              should = [query_pdf],
              minimum_should_match = 1
        )
        search = search.query(final_query)

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

    def seach_by_subject(self, query, subject):
        sub_search = self.SubjectSearch(query, {'subject': subject})

        sub_search = sub_search.source(['title','authors', 'other_subjects'])
        sub_search = sub_search.highlight_options(order='score')
        sub_search = sub_search.highlight('pdf', fragment_size=200)
        suggestion = sub_search.suggest('suggestion', keywords, term={'field': 'pdf'})
        request = sub_search.execute()
        for hit in request:
            response = hit.to_dict()
            response.update({'fragment': hit.meta.highlight.pdf}) 
            yield response


