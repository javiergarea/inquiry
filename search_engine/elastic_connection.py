from elasticsearch import Elasticsearch


class ElasticConnection(object):

    class __Connection:
        def __init__(self):
            self.connection = Elasticsearch([{'host': 'localhost', 'port': 9200}])

        def __str__(self):
            return str(self.connection)

    instance = None

    def __new__(cls):  # __new__ always a classmethod
        if not ElasticConnection.instance:
            ElasticConnection.instance = ElasticConnection.__Connection()
        return ElasticConnection.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
