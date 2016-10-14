import os


class SpimiMerger:
    def __init__(self, files_list, output_file_prefix, output_directory='out'):
        """
        SPIMI merger.
        :param files_list: the list of 'block' files to be merged
        """
        self.files_list = files_list
        output_file_prefix = output_file_prefix
        output_directory = output_directory
        output_file_name = '{}master.{}'.format(output_file_prefix, 'txt')
        self.output_file_path = os.path.join(output_directory, output_file_name)

    def merge(self):
        self.intersect()

    def intersect(self):
        # Open files
        file_handles = [open(f, 'r') for f in self.files_list]
        output_file_handle = open(self.output_file_path, 'w')

        # Read first line of each opened file
        next_lines = [f.readline() for f in file_handles]
        while next_lines:
            next_line_to_write_obj = SpimiBlockLine(list(), None, list())
            for block_file_index, file_line in enumerate(next_lines):
                line_obj = SpimiBlockLine.from_line_string([block_file_index], file_line)
                # Select line if initial line
                if next_line_to_write_obj.term is None:
                    next_line_to_write_obj = line_obj
                # Merge postings lists if terms equal
                elif line_obj.term == next_line_to_write_obj.term:
                    next_line_to_write_obj = line_obj.merge(next_line_to_write_obj)
                # Replace larger term & list if new term precedes it
                elif line_obj.term < next_line_to_write_obj.term:
                    next_line_to_write_obj = line_obj

            # TODO comment this confusingness
            self.write_line_to_output_file(next_line_to_write_obj, output_file_handle)
            next_line_file_index_list = next_line_to_write_obj.block_file_index_list
            new_next_lines = [file_handles[index].readline() for index in next_line_file_index_list]

            # next_line is empty string if end of file is reached
            for index, new_line in enumerate(new_next_lines):
                if not new_line:
                    # Remove from file_handles & next_lines lists
                    del(next_lines[next_line_file_index_list[index]])
                    del(file_handles[next_line_file_index_list[index]])
                else:
                    next_lines[next_line_file_index_list[index]] = new_line

    @staticmethod
    def write_line_to_output_file(line_obj, output_file_handle):
        """
        Write the line object to a file
        :param line_obj:
        :param output_file_handle:
        :return:
        """
        output_file_handle.write(str(line_obj))


class SpimiBlockLine:
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
        return SpimiBlockLine(new_block_file_index_list, self.term, new_postings_list)

    def __str__(self):
        return '{} {}\n'.format(self.term, ' '.join([str(doc_id) for doc_id in self.postings_list]))
