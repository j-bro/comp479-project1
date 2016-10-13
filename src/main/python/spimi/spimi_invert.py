import sys


class SpimiInverter:
    def __init__(self, tokens, output_file_prefix='block_out', block_size_limit=1000000):
        self.tokens_iter = iter(tokens)
        self.output_file_prefix = output_file_prefix
        self.block_size_limit = block_size_limit
        self.block_num = 0

    def run(self):
        output_files = list()
        while True:
            dictionary = dict()
            while sys.getsizeof(dictionary) / 1024 / 1024 <= self.block_size_limit:
                try:
                    token = self.tokens_iter.next()
                except StopIteration:
                    print("Finished iterating through token list")
                    break
                if token[0] not in dictionary:
                    postings_list = self._add_to_dictionary(dictionary, token[0])
                else:
                    postings_list = self._get_postings_list(dictionary, token[0])

                self._add_to_postings_list(postings_list, token[1])

            self.block_num += 1
            sorted_terms = self._sort_terms(dictionary)
            file_path = self._write_block_to_disk(sorted_terms, dictionary)
            output_files.append(file_path)

        return output_files

    @staticmethod
    def _add_to_dictionary(dictionary, term):
        dictionary[term] = list()
        return dictionary[term]

    @staticmethod
    def _get_postings_list(dictionary, term):
        return dictionary[term]

    @staticmethod
    def _add_to_postings_list(postings_list, doc_id):
        postings_list.append(doc_id)

    @staticmethod
    def _sort_terms(dictionary):
        return [term for term in sorted(dictionary.keys())]

    def _write_block_to_disk(self, sorted_terms, dictionary):
        file_path = '{}-{}'.format(self.output_file_prefix, self.block_num)
        with open(file_path, 'w') as f:
            for term in sorted_terms:
                output_line = '{} {}\n'.format(term, ' '.join([str(doc_id) for doc_id in dictionary[term]]))
                f.write(output_line)
        return file_path
