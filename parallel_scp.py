#!/usr/bin/env python

import argparse
import subprocess
from os.path import basename

def download_file(server, path):
    local_filename = "%s-%s" % (server, basename(path))
    subprocess.call(["scp", "%s:%s" % (server, path), local_filename])

def main():
    parser = argparse.ArgumentParser("Download same file from multiple " + \
                                         "servers")
    parser.add_argument("path", help="Path to file")
    parser.add_argument("servers", nargs="+", help="Servers to download from")
    args = parser.parse_args()

    for server in args.servers:
        download_file(server, args.path)

if __name__ == '__main__':
    main()
