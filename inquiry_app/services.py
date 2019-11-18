from elasticsearch_dsl import Search, Q
from search_engine.elastic_connection import ElasticConnection


class InquiryService:

    def __init__(self):
        self.es = ElasticConnection().connection

    def search_by_keywords(self, keywords, subject):
        search = Search(using=self.es, index="arxiv-index")
        query_content = Q("wildcard", abstract="*" + keywords + "*")
        query_subject = Q()
        query_other = Q()
        if subject and subject != 'all':
            query_subject = Q(
                "wildcard",
                subject="*" + subject + ".*",
                boost=0.5)
            query_other = Q("wildcard", other_subjects="*" + subject + ".*")
        final_query = Q('bool',
                        must=[query_content],
                        should=[query_subject, query_other],
                        minimum_should_match=1)
        search = search.query(final_query)

        search = search.source(
            ['title', 'authors', 'subject', 'other_subjects', 'abstract', 'pdf_url'])
        search = search.highlight_options(order='score')
        search = search.highlight('abstract', fragment_size=400)
        search = search.suggest('suggestion', keywords, term={'field': 'abstract'})

        request = search.execute()
        suggestions = [elem["text"] for elem in request.suggest.suggestion[0]["options"]]
        
        for hit in request:
            response = hit.to_dict()
            response.update({'fragment': hit.meta.highlight.abstract})
            response.update({'suggestion': suggestions})
            yield response

    def search_by_fields(self, title, authors, abstract, content, subject, start_date, end_date):
        search = Search(using=self.es, index="arxiv-index")
        query_title = Q()
        query_authors = Q()
        query_subject = Q()
        query_other = Q()
        query_abstract = Q()
        query_content = Q()

        if title:
            query_title = Q("wildcard", title="*" + title + "*")

        if authors:
            for author in authors.split(" "):
                query_authors = query_authors + \
                    Q("wildcard", authors="*" + author + "*")

        if subject and subject != 'all':
            query_subject = Q("wildcard", subject="*" + subject + ".*", boost=0.5)
            query_other = Q(
                "wildcard", other_subjects="*" + subject + ".*")

        if abstract:
            query_abstract = Q("match", abstract=abstract)
            search = search.highlight_options(order='score')
            search = search.highlight('abstract', fragment_size=400)

        if content:
            query_content = Q("match", pdf=content)

        # search = search.filter('range', submit_date={'gte': start_date , 'lte': end_date})

        final_query = Q('bool',
                        must=[query_title, query_authors, query_subject],
                        should=[query_abstract, query_content, query_other],
                        minimum_should_match=2)

        search = search.query(final_query)
        request = search.execute()
        for hit in request:
            response = hit.to_dict()
            if abstract:
                response.update({'fragment': hit.meta.highlight.abstract})
            else:
                response.update({'fragment': []})
            yield response
