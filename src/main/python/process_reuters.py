#!/usr/bin/python

from reuters_parser import ReutersParser
from fetch_reuters import fetch_reuters
from spimi import spimi_invert, spimi_merge


def main():
    # fetch_reuters()

    # Without compression
    parser = ReutersParser('reuters21578')
    tokens_list = parser.parse()

    inverter = spimi_invert.SpimiInverter(tokens_list, output_file_prefix='no_compression_')
    output_files = inverter.run()

    merger = spimi_merge.SpimiMerger(output_files, 'no_compression_')
    merger.merge()

    # With compression
    # parser = ReutersParser('reuters21578', stem=True, remove_stopwords=True)
    # tokens_list = parser.parse()
    #
    # inverter = spimi_invert.SpimiInverter(tokens_list, output_file_prefix='compression_')
    # output_files = inverter.run()
    #
    # merger = spimi_merge.SpimiMerger(output_files)
    # merger.merge()


if __name__ == '__main__':
    main()
