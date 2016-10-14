import os

from dictionary_file import DictionaryFile, DictionaryFileLine


class SpimiMerger:
    def __init__(self, files_list, output_file_prefix, output_directory='out'):
        """
        SPIMI merger.
        :param files_list: the list of 'block' files to be merged
        """
        self.files_list = files_list
        output_file_name = '{}master.{}'.format(output_file_prefix, 'txt')
        output_file_path = os.path.join(output_directory, output_file_name)
        self.output_file = DictionaryFile(output_file_path)

    def merge(self):
        self.intersect()

    def intersect(self):
        # Open files
        file_handles = [f.open_handle() for f in self.files_list]
        output_file_handle = self.output_file.open_handle(mode='w')

        # Read first line of each opened file
        next_lines = [f.readline() for f in file_handles]
        while next_lines:
            next_line_to_write_obj = DictionaryFileLine(list(), None, list())
            for block_file_index, file_line in enumerate(next_lines):
                line_obj = DictionaryFileLine.from_line_string([block_file_index], file_line)
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
            self.output_file.write_line(next_line_to_write_obj)
            next_line_file_index_list = next_line_to_write_obj.block_file_index_list
            new_next_lines = [file_handles[index].readline() for index in next_line_file_index_list]

            # next_line is empty string if end of file is reached
            for index, new_line in enumerate(new_next_lines):
                if not new_line:
                    # Remove from file_handles & next_lines lists (+ close handle)
                    del(next_lines[next_line_file_index_list[index]])
                    file_handles[next_line_file_index_list[index]].close()
                    del(file_handles[next_line_file_index_list[index]])
                else:
                    next_lines[next_line_file_index_list[index]] = new_line

        # Close output file
        self.output_file.close_handle()
        print("Finished writing merged output file")
        return self.output_file
