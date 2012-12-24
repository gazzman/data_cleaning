#!/usr/bin/python
import argparse
import csv

__version__ = ".01"
__author__ = "gazzman"
__copyright__ = "(C) 2012 gazzman GNU GPL 3."
__contributors__ = []

def merge_csvs(first_csv, second_csv, merged_csv):
    csv1 = csv.DictReader(open(first_csv, 'r'))
    csv2 = csv.DictReader(open(second_csv, 'r'))

    headers = csv1.fieldnames
    headers += [x for x in csv2.fieldnames if not x in headers]
    with open(merged_csv, 'w') as f:
        f.write(','.join(headers) + '\n')
        mcsv = csv.DictWriter(f, headers)
        for row in csv1: mcsv.writerow(row)
        for row in csv2: mcsv.writerow(row)

# For running from command line
if __name__ == "__main__":
    description = 'Merge two csv files into one.'
    description += ' Both csvs must have headers as their first rows.'

    merged_csv = 'merged.csv'
    help = 'name of merged csv file.'
    help += ' Defaults to \'' + merged_csv + '\'.'

    p = argparse.ArgumentParser(description=description)
    p.add_argument('first_csv', type=str, 
                   help='the first csv file.')
    p.add_argument('second_csv', type=str, 
                   help='the second csv file.')
    p.add_argument('-s', metavar='merged_csv', default=merged_csv, dest='merged_csv', 
                    help=help)
    p.add_argument('-v', '--version', action='version', 
                   version='%(prog)s ' + __version__)

    args = p.parse_args()
    merge_csvs(args.first_csv, args.second_csv, args.merged_csv)
