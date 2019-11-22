from elasticsearch_dsl import Search, Q
from search_engine.elastic_connection import ElasticConnection


class InquiryService:

    def __init__(self):
        self.es = ElasticConnection().connection

    def _extend_query(self, search, keywords):
        search = search.suggest('suggestion', keywords, term={'field': 'abstract'})
        request = search.execute()
        suggestions = [elem['text'] for elem in request.suggest.suggestion[0]['options']]
        suggestion_query = []

        for suggestion in suggestions:
            suggestion_query.append(Q('wildcard', abstract='*' + suggestion + '*'))

        final_query = Q('bool',
                        should=suggestion_query,
                        minimum_should_match=0)

        search = search.query(final_query)

        return search

    def search_by_keywords(self, keywords, subject):
        search = Search(using=self.es, index='arxiv-index')
        query_content = Q()
        for keyword in keywords.split(' '):
            query_content = query_content + \
                Q('wildcard', abstract='*' + keyword + '*')
        query_subject = Q()
        query_other = Q()
        if subject and subject != 'all':
            query_subject = Q('wildcard', subject='*' + subject + '.*')
            query_other = Q('wildcard', other_subjects='*' + subject + '.*')
        final_query = Q('bool',
                        must=[query_content],
                        should=[query_subject, query_other],
                        minimum_should_match=1)
        search = search.query(final_query)
        search = search.source(['title', 'authors', 'subject', 'other_subjects',
                                'abstract', 'abstract_url', 'pdf_url', 'submit_date'])
        search = search.highlight_options(order='score')
        search = search.highlight('abstract', fragment_size=400)

        total = search.count()
        search = search[0:total]
        search = self._extend_query(search, keywords)
        request = search.execute()

        for hit in request:
            response = hit.to_dict()
            response.update({'fragment': hit.meta.highlight.abstract})
            yield response

    def search_by_fields(self, title, authors, abstract, content, subject):
        search = Search(using=self.es, index='arxiv-index')
        query_title = Q()
        query_authors = Q()
        query_subject = Q()
        query_other = Q()
        query_abstract = Q()
        query_content = Q()

        if title:
            for word in title.split(' '):
                query_title = query_title + \
                    Q('wildcard', title='*' + word + '*')

        if authors:
            for author in authors.split(' '):
                query_authors = query_authors + \
                    Q('wildcard', authors='*' + author + '*')

        if subject and subject != 'all':
            query_subject = Q('wildcard', subject='*' + subject + '.*')
            query_other = Q(
                'wildcard', other_subjects='*' + subject + '.*')

        if abstract:
            for word in abstract.split(' '):
                query_abstract = query_abstract + \
                    Q('wildcard', abstract='*' + word + '*')

        if content:
            for word in content.split(' '):
                query_content = query_content + \
                    Q('wildcard', pdf='*' + word + '*')

        final_query = Q('bool',
                        must=[query_title, query_authors, query_subject],
                        should=[query_abstract, query_content, query_other],
                        minimum_should_match=2)

        total = search.count()
        search = search[0:total]
        search = search.query(final_query)
        search = search.source(['title', 'authors', 'subject', 'other_subjects',
                                'abstract', 'abstract_url', 'pdf_url', 'submit_date'])

        if abstract:
            search = self._extend_query(search, abstract)
            search = search.highlight_options(order='score')
            search = search.highlight('abstract', fragment_size=400)
        request = search.execute()

        for hit in request:
            response = hit.to_dict()
            if 'highlight' in hit.meta:
                response.update({'fragment': hit.meta.highlight.abstract})
            else:
                response.update({'fragment': []})
            yield response
