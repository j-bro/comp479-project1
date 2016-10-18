import os

from query import AndQuery, OrQuery


class QueryMaker:
    """
    Class to simplify making & running queries.
    """
    def __init__(self, dictionary_file_path, keywords, query_type):
        if not os.path.exists(dictionary_file_path):
            raise Exception("Dictionary file does not exist! {}".format(dictionary_file_path))

        self.dictionary_file_path = dictionary_file_path
        self.keywords = keywords

        if query_type == 'and':
            self.query = AndQuery(keywords, dictionary_file_path)
        elif query_type == 'or':
            self.query = OrQuery(keywords, dictionary_file_path)
        else:
            raise Exception("Unknown query type {}".format(query_type))

    def make_query(self):
        """
        Run the created query.
        :return: the query object of the run query.
        """
        self.query.run_query()
        return self.query

