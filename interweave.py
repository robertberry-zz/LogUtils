#!/usr/bin/env python

import argparse
import dateutil.parser
import re

DEFAULT_DATE_REGEX = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"

class FileWrapper(object):
    def __init__(self, fp, date_parser):
        self.fp = fp
        self.date_parser = date_parser
        self.next()

    def next(self):
        self.current_line = self.fp.readline()
        
        if not self.finished:
            match = self.date_parser.search(self.current_line)

            if match:
                date_string = match.group(0)

                try:
                    self.current_time = dateutil.parser.parse(date_string)
                except ValueError, e:
                    raise RuntimeError("Could not parse date of format " + date_string)
            else:
                # just try to skip the line
                self.next()
                #raise RuntimeError("Could not match date in this line: " + self.current_line)

    @property
    def finished(self):
        return self.current_line == ""

def interweave(files, date_matcher):
    wrappers = [FileWrapper(f, date_matcher) for f in files]
    wrappers = [w for w in wrappers if not w.finished]

    while len(wrappers) > 0:
        next_wrapper = min(wrappers, key=lambda w: w.current_time)
        yield next_wrapper.current_line
        next_wrapper.next()
        wrappers = [w for w in wrappers if not w.finished]

def main():
    parser = argparse.ArgumentParser(description="Interweave some logs")
    parser.add_argument("--date_regex", default=DEFAULT_DATE_REGEX, \
                            help="Regex to extract date from log line")
    parser.add_argument("logs", nargs="+", help="Paths to logs")
    args = parser.parse_args()

    date_matcher = re.compile(args.date_regex)

    files = [open(path, "r") for path in args.logs]

    try:
        for line in interweave(files, date_matcher):
            print line,
    except IOError, e:
        if e.errno == 32:
            exit()
        else:
            raise e

if __name__ == "__main__":
    main()

