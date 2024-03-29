from spimi.dictionary import DictionaryFile
from list_helper import merge_lists, intersect_lists


class Query:
    """
    Query Model
    """
    def __init__(self, keywords, dictionary_file_path):
        self.keywords = sorted(keywords)
        self.dictionary_file = DictionaryFile(dictionary_file_path)
        self.result = None

    def run_query(self):
        raise NotImplementedError('run_query() must be implemented in a subclass of Query.')

    def get_dictionary_file_lines_for_keywords(self):
        """
        Get the dictionary lines (terms + postings lists) matching the specified keywords
        :param keywords: the keywords to look for
        :return: A list of the DictionaryFileLine objects related to the keywords read from the dictionary file.
        """
        keywords_iter = iter(self.keywords)
        next_keyword = keywords_iter.next()
        print("Searching for keyword {}".format(next_keyword))

        self.dictionary_file.open_handle()
        result_lines = list()
        while next_keyword:
            line = self.dictionary_file.read_line_to_obj()
            if not line:
                print("Reached end of dictionary file")
                break

            if line.term < next_keyword:
                continue
            elif line.term == next_keyword:
                print("Found postings list for term {}".format(next_keyword))
                result_lines.append(line)

            try:
                next_keyword = keywords_iter.next()
                print("Searching for keyword {}".format(next_keyword))
            except StopIteration:
                print("Finished searching for all keywords")
                break

        return result_lines


class AndQuery(Query):
    def __init__(self, keywords, dictionary_file_path):
        Query.__init__(self, keywords, dictionary_file_path)

    def run_query(self):
        """
        Store the results of this 'AND' query in self.results.
        """
        query_dictionary_file_lines = self.get_dictionary_file_lines_for_keywords()
        result_postings_list = intersect_lists([result.postings_list for result in query_dictionary_file_lines])
        self.result = result_postings_list
        print("Found {} matching documents".format(len(result_postings_list)))


class OrQuery(Query):
    def __init__(self, keywords, dictionary_file_path):
        Query.__init__(self, keywords, dictionary_file_path)

    def run_query(self):
        """
        Store the results of this 'OR' query in self.results.
        """
        query_dictionary_file_lines = self.get_dictionary_file_lines_for_keywords()
        result_postings_list = merge_lists([result.postings_list for result in query_dictionary_file_lines])
        self.result = result_postings_list
        print("Found {} matching documents".format(len(result_postings_list)))
