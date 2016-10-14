from query import AndQuery, OrQuery


class QueryMaker:
    def __init__(self, dictionary_file, keywords, query_type):
        self.dictionary_file = dictionary_file
        self.keywords = keywords

        if query_type == 'and':
            self.query = AndQuery(keywords, dictionary_file)
        elif query_type == 'or':
            self.query = OrQuery(keywords, dictionary_file)
        else:
            raise Exception("Unknown query type {}".format(query_type))

    def make_query(self):
        pass

