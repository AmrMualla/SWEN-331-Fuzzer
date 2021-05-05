"""
    Fuzzer Project
    SWEN-331
    Kyle McCoy
"""

import argparse
import sys
import app.discover as discover
import app.test as test


def main():
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--custom-auth', nargs='?', type=str)
    parent_parser.add_argument('url')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Commands', description='The commands that the fuzzer can run.',
                                       dest='cmd')

    # Discover Options
    discover_parser = subparsers.add_parser('discover', parents=[parent_parser])
    discover_parser.add_argument('--common-words', nargs='?', default="common_words.txt", type=str, required=True)
    discover_parser.add_argument('--extensions', nargs='?', default="default_extensions.txt", type=str, required=False)

    # Test Options
    test_parser = subparsers.add_parser('test', parents=[parent_parser])
    test_parser.add_argument('--common-words', nargs='?', default="common_words.txt", type=str, required=True)
    test_parser.add_argument('--extensions', nargs='?', default="default_extensions.txt", type=str, required=False)
    test_parser.add_argument('--vectors', nargs='?', default="default_vectors.txt", type=str, required=True)
    test_parser.add_argument('--sanitized-chars', nargs='?', default="sanitized.txt", type=str, required=False)
    test_parser.add_argument('--sensitive', nargs='?', default="sensitive.txt", type=str, required=True)
    test_parser.add_argument('--slow', nargs='?', type=int, default=500, required=False)

    # Run Fuzzer with Arguments
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.cmd == 'discover':
            print("Running discover on base url: " + args.url + "\n")
            discover.discover(args, True)
        if args.cmd == 'test':
            print("Running test on base url: " + args.url + "\n")
            param_dict, form_dict, session = discover.discover(args, False)
            test.test(param_dict, form_dict, session, args)


if __name__ == '__main__':
    main()
