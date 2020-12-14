#!/usr/bin/env python

import argparse
import pandas as pd
import re
import sys

"""
Parse arguments
"""
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    return parser.parse_args()

"""
Read log file and parse its lines
"""
def read_file(source):
    data = pd.DataFrame() #columns=['style', 'zoom', 'x', 'y'])

    for line in source:
        match = re.search(r'GET /(.+?)/(\d+)/(\d+)/(\d+)\.\S+', line)

        if match:
            groups = match.groups()[:4]
            data = data.append([groups])

    print(data)


if __name__ == '__main__':

    args = parse_arguments()

    try:
        with open(args.source, 'r') as source:
            read_file(source)
    except IndexError:
        sys.stderr.write('Usage: %s <source.log>\n' % sys.argv[0])
        sys.exit(1)
    except IOError as e:
        sys.stderr.write('Cannot open file: %s\n' % str(e))
        sys.exit(2)
