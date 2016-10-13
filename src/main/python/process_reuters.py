#!/usr/bin/python

from reuters_parser import ReutersParser
from fetch_reuters import fetch_reuters
from spimi import spimi_invert, spimi_merge


def main():
    # fetch_reuters()

    parser = ReutersParser('reuters21578')
    tokens_list = parser.parse()

    inverter = spimi_invert.SpimiInverter(tokens_list)
    output_files = inverter.run()

    merger = spimi_merge.SpimiMerger()
    merger.merge()


if __name__ == '__main__':
    main()
