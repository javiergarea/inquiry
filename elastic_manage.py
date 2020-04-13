import argparse
from search_engine.elastic_connection import ElasticConnection
from search_engine.indexer import Indexer


def main(es_connection):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i', '--index', type=str,
                           help='path to index')
    argparser.add_argument('-d', '--delete-index', action='store_true',
                           help='delete current existing indexes')
    args = argparser.parse_args()

    if not (args.index or args.delete_index):
        print("Wrong argument sequence: You must specify at least one argument.")
        exit()
    if (args.index and args.delete_index):
        print("Wrong argument sequence: Use the function one at a time.")
        exit()

    indexer = Indexer(es_connection)

    if args.index:
        indexer.index_docs(args.index)
    else:
        indexer.delete_index()


if __name__ == "__main__":
    main(ElasticConnection().connection)
