
class Query:
    def __init__(self, keywords, dictionary_file_path):
        self.keywords = keywords
        self.dictionary_file_path = dictionary_file_path

    def get_result(self):
        raise NotImplementedError('get_result() must be implemented in a subclass of Query.')


class AndQuery(Query):
    def __init__(self, keywords, dictionary_file_path):
        Query.__init__(self, keywords, dictionary_file_path)

    def get_result(self):
        pass


class OrQuery(Query):
    def __init__(self, keywords, dictionary_file_path):
        Query.__init__(self, keywords, dictionary_file_path)

    def get_result(self):
        pass
