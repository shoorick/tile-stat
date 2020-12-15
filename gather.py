#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import re
import sys

"""
Parse arguments
"""
def parse_arguments():
    parser = argparse.ArgumentParser(description='Gather and process data from web server log files')
    parser.add_argument('-o', '--output',
                        dest='file',
                        help='output raw data to file, format are choosing by extension (csv, xls, xlsx, htm, html, json)')
    parser.add_argument('-c', '--column',
                        dest='name',
                        help='process desired column (possible names are style, zoom)')
    parser.add_argument('source', nargs='+', type=argparse.FileType('r'))
    return parser.parse_args()

"""
Read log file and parse its lines
"""
def read_file(source):
    data = []

    for line in source:
        match = re.search(r'GET /(.+?)/(\d+)/(\d+)/(\d+)\.\S+', line)

        if match:
            groups = [match.group(1)]
            groups.extend(int(x) for x in match.groups()[1:4])
            data.append(groups)

    return data


if __name__ == '__main__':

    data = []
    args = parse_arguments()

    if args.source:
        for f in args.source:
            try:
                data.extend(read_file(f))
            except IOError as e:
                sys.stderr.write('Cannot open file: %s\n' % str(e))
    else:
        sys.stderr.write('Usage: %s [options] <source.log>\n' % sys.argv[0])
        sys.exit(1)

    if not data:
        sys.stderr.write('No data\n')
        sys.exit(2)

    df = pd.DataFrame(data, columns=['style', 'zoom', 'x', 'y'])
    print(df)

    output = args.file
    if output:
        if re.search(r'\.csv$', output, re.I):
            df.to_csv(output)
        elif re.search(r'\.html?$', output, re.I):
            df.to_html(output)
        elif re.search(r'\.js(on)?$', output, re.I):
            df.to_json(output)
        elif re.search(r'\.xlsx?$', output, re.I):
            df.to_excel(output)
        else:
            sys.stderr.write(f'Output file {output} has unknown type. '
                + 'Only CSV, HTML, and XSLX are available.\n')

    column = args.name
    if column and re.match(r'(style|zoom)$', column):
        count = df[column].value_counts().sort_index()
        print(count)
        count.plot.barh()
        plt.show()
