

class DictionaryFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_handle = None

    def open_handle(self, mode='r'):
        self.file_handle = open(self.file_path, mode)
        return self.file_handle

    def write_line(self, line_obj):
        """
        Write the line object to a file
        :param line_obj:
        :return:
        """
        self.file_handle.write(str(line_obj))

    def close_handle(self):
        self.file_handle.close()


class DictionaryFileLine:
    def __init__(self, block_file_index_list, term, postings_list):
        self.block_file_index_list = block_file_index_list
        self.term = term
        self.postings_list = postings_list

    @classmethod
    def from_line_string(cls, block_file_index_list, line_string):
        """
        Parse the data in a block file line.
        :param block_file_index_list: the index of the document in which the line is found
        :param line_string: the line text to be parsed
        :return: An instance of SpimiBlockLinetuple containing (index, term, postings_list)
        """
        split_line = line_string.split(' ')
        return cls(block_file_index_list, split_line[0], [int(doc_id) for doc_id in split_line[1:]])

    def merge(self, other_block_line):
        new_block_file_index_list = sorted(self.block_file_index_list + other_block_line.block_file_index_list)
        new_postings_list = sorted(self.postings_list + other_block_line.postings_list)
        return DictionaryFileLine(new_block_file_index_list, self.term, new_postings_list)

    def __str__(self):
        return '{} {}\n'.format(self.term, ' '.join([str(doc_id) for doc_id in self.postings_list]))
