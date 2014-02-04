#!/usr/bin/python
from collections import OrderedDict
import argparse
import csv

__version__ = ".02"
__author__ = "gazzman"
__copyright__ = "(C) 2012 gazzman GNU GPL 3."
__contributors__ = []

def merge_csvs(filenames, merged_csv):
    csvs = []
    headers = []
    for filename in filenames:
        csv_file = csv.DictReader(open(filename, 'r'))
        csvs += [csv_file]
        headers += [x for x in csvs[-1].fieldnames if not x in headers]

    with open(merged_csv, 'w') as f:
        mcsv = csv.DictWriter(f, headers)
        mcsv.writerow(OrderedDict(zip(headers, headers))) 
        for csv_file in csvs:
            for row in csv_file:
                mcsv.writerow(row)

# For running from command line
if __name__ == "__main__":
    description = 'Merge several csv files into one.'
    description += ' All csvs must have headers as their first rows.'

    merged_csv = 'merged.csv'
    help = 'name of merged csv file.'
    help += ' Defaults to \'' + merged_csv + '\'.'

    p = argparse.ArgumentParser(description=description)
    p.add_argument('csv_list_file', type=str, 
                   help='a text file containing the list of csvs to merge.')
    p.add_argument('-s', metavar='merged_csv', default=merged_csv, dest='merged_csv', 
                    help=help)
    p.add_argument('-v', '--version', action='version', 
                   version='%(prog)s ' + __version__)

    args = p.parse_args()

    filenames = []
    with open(args.csv_list_file) as f:
        for line in f:
            filename = line.strip()
            if len(filename) > 0:
                if filename[0] != '#': filenames += [filename]
    merge_csvs(filenames, args.merged_csv)
