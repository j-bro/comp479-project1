#!/usr/bin/env python2

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # easy hack to import lib module
from argparse import ArgumentParser
from query.query_maker import QueryMaker

DICTIONARY_FILE = os.path.abspath('../out/no_compression_master.txt')


def main(args):
    dictionary_file = args.dictionary
    print(dictionary_file)

    query_maker = QueryMaker(dictionary_file, args.keywords, args.query_type.lower())
    query = query_maker.make_query()

    print("Document IDs matching query: {}".format(str(query.result)))


def parse_args(sys_args):
    parser = ArgumentParser(description="Query the Reuters corpus.")
    parser.add_argument('query_type', metavar='(AND | OR)', choices=['AND', 'and', 'OR', 'or'])
    parser.add_argument('keywords', metavar='term', nargs='+')
    parser.add_argument('-d', '--dictionary', type=str, default=DICTIONARY_FILE)
    return parser.parse_args(sys_args)


if __name__ == '__main__':
    parsed_args = parse_args(sys.argv[1:])
    main(parsed_args)
