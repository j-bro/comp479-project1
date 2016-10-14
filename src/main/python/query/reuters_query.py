import sys
from argparse import ArgumentParser


from query_maker import QueryMaker

DICTIONARY_FILE = 'out/no_compression_master.txt'


def main(args):
    dictionary_file = args.dictionary if args.dictionary else DICTIONARY_FILE

    query_maker = QueryMaker(dictionary_file, args.keywords, args.query_type.lower())
    result = query_maker.make_query()

    print(str(query.get_result()))


def parse_args(sys_args):
    parser = ArgumentParser(description="Query the Reuters corpus.")
    parser.add_argument('query_type', metavar='(AND | OR)', choices=['AND', 'and', 'OR', 'or'])
    parser.add_argument('keywords', metavar='term', nargs='+')
    parser.add_argument('-d', '--dictionary', type=str)
    return parser.parse_args(sys_args)


if __name__ == '__main__':
    parsed_args = parse_args(sys.argv[1:])
    main(parsed_args)
