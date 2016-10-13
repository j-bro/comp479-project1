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
        file_handles = [open(f, 'r') for f in self.files_list]
        output_file_handle = open(self.output_file_path, 'w')
        self.intersect(file_handles, output_file_handle)


    def intersect(self, file_handles, output_file_handle):
        while True:
            next_lines = [f.readline() for f in file_handles]
            next_line_to_write_tuple = (-1, '', list())
            for index, file_line in enumerate(next_lines):
                line_tuple = self.parse_block_line(file_line)

                # Merge terms if equal
                if line_tuple[1] == next_line_to_write_tuple[1]:
                    # TODO merge
                # Replace larger term & list if new term precedes it
                elif line_tuple[1] < next_line_to_write_tuple[1]:
                    next_line_to_write_tuple = line_tuple

            self.write_line_to_output_file(next_line_to_write_tuple, output_file_handle)
            next_lines[next_line_to_write_tuple[0]] = file_handles[next_line_to_write_tuple[0]].readline()

        # while not block1.empty() and not block2.empty():
        #     term1 = get_term(block1)
        #     term2 = get_term(block2)
        #     if term1 == term2:
        #         pos = merge_postings()  # TODO
        #         ...
        #         term1 = next_term(block1)
        #         term2 = next_term(block2)
        #     else:
        #         if term1 < term2:
        #             add(term1, pos)
        #             term1 = next_term(block1)
        #         else:
        #             add(term2, pos)
        #             term2 = next_term(block2)

    @staticmethod
    def write_line_to_output_file(line, output_file_handle):
        """

        :param line:
        :param output_file_handle:
        :return:
        """
        output_file_handle.write(line)

    @staticmethod
    def parse_block_line(index, line):
        """
        Parse the data in a block file line.
        :param line: the line text to be parsed
        :return: A tuple containing (index, term, postings_list)
        """
        split_line = line.split(' ')
        return index, split_line[0], split_line[1:]

    @staticmethod
    def stringify_line_tuple(line_tuple):
        return '{} {}\n'.format(line_tuple[1], ' '.join([str(doc_id) for doc_id in line_tuple[2]]))
        # TODO test this