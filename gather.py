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
    parser.add_argument('source')
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

    return pd.DataFrame(data, columns=['style', 'zoom', 'x', 'y'])


if __name__ == '__main__':

    args = parse_arguments()

    try:
        with open(args.source, 'r') as source:
            df = read_file(source)
    except IndexError:
        sys.stderr.write('Usage: %s [options] <source.log>\n' % sys.argv[0])
        sys.exit(1)
    except IOError as e:
        sys.stderr.write('Cannot open file: %s\n' % str(e))
        sys.exit(2)

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
