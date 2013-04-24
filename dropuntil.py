#!/usr/bin/env python

import argparse
import re
import itertools

def main():
    parser = argparse.ArgumentParser(description="Interweave some logs")
    parser.add_argument("regexp", help="Reg exp to drop until")
    parser.add_argument("file", help="File to read")
    args = parser.parse_args()

    matcher = re.compile(args.regexp)

    with open(args.file, "r") as fp:
        try:
            for line in itertools.takewhile(lambda l: matcher.match(l), fp):
                print line,
        except IOError, e:
            if e.errno == 32:
                exit()
            else:
                raise e

if __name__ == "__main__":
    main()

