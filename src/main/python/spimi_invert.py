

class SpimiInverter:
    def __init__(self, tokens_iter, memory_size, output_file=None):
        self.tokens_iter = tokens_iter
        self.memory_size = memory_size
        self.output_file = output_file
        self.dictionary = dict()
        self.free_memory_available = True

    def run(self):
        while self.free_memory_available:
            token = self.tokens_iter.next()
            if token[0] not in self.dictionary:
                postings_list = self._add_to_dictionary(token[0])
            else:
                postings_list = self._get_postings_list(token[0])

            self._add_to_postings_list(postings_list, token[1])

        sorted_terms = self._sort_terms()
        self._write_block_to_disk(sorted_terms)

        return self.output_file

    def _add_to_dictionary(self, term):
        self.dictionary[term] = list()
        return self.dictionary[term]

    def _get_postings_list(self, term):
        return self.dictionary[term]

    @staticmethod
    def _add_to_postings_list(postings_list, doc_id):
        postings_list.append(doc_id)

    def _sort_terms(self):
        return [term for term in sorted(self.dictionary.keys())]

    def _write_block_to_disk(self, sorted_terms):
        with open(self.output_file, 'w') as f:
            for term in sorted_terms:
                output_line = '{} {}'.format(term, ' '.join(str(doc_id) for doc_id in self.dictionary[term]))
                f.write(output_line)

## FINAL STEP IS TO MERGE