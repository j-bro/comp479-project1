
class Query:
    def __init__(self, keywords, dictionary_file_path):
        self.keywords = keywords
        self.dictionary_file_path = dictionary_file_path
        self.result = None

    def run_query(self):
        raise NotImplementedError('get_result() must be implemented in a subclass of Query.')


class AndQuery(Query):
    def __init__(self, keywords, dictionary_file_path):
        Query.__init__(self, keywords, dictionary_file_path)

    def run_query(self):
        self.result = None  # TODO use
        return self.result


class OrQuery(Query):
    def __init__(self, keywords, dictionary_file_path):
        Query.__init__(self, keywords, dictionary_file_path)

    def run_query(self):
        self.result = None  # TODO use
        return self.result
