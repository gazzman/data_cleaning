#!/usr/bin/python
import argparse
import csv

from data_cleaning.list_all_files import print_files

series_dicts = {}
fields = ['path', 'title', 'series', 'source', 'release', 'sadj', 'freq', 
          'units', 'dates', 'updated']


# For running from command line
if __name__ == "__main__":
    description = 'Assess a collection of space-delimited FRED2.'

    a = argparse.ArgumentParser(description=description)
    a.add_argument('-p', type=str, default='./', dest='top_level', 
                   help='The top-level path. Default is \'./\'.')
    a.add_argument('-w', dest='windows', action='store_true',
                   help='If set, changes forwardslashes to backslashes.')

    args = a.parse_args()
    if args.top_level[-1] == '/': args.top_level = args.top_level[:-1]

    c = csv.DictWriter(open(args.top_level + '/descriptions.csv', 'wb'), fields)
    row = {}
    for field in fields:
        row[field] = field
    c.writerow(row)

    fr2s = print_files(args.top_level, windows=args.windows, display=False)
    print len(fr2s)
    for fr2 in fr2s:
        if fr2[-3:] == 'txt':
            row = {'path': fr2}
            with open(fr2, 'rb') as f:
                for field in fields[1:]:
                    row[field] = f.readline().partition(':')[2].strip()
                c.writerow(row)
