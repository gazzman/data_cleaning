#!/usr/bin/python
import argparse
import csv
import sys

if __name__ == "__main__":
    description = 'Cleanup the factors datafile obtained from '
    description += "http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html"
    description += " for ease of importing into other applications."

    a = argparse.ArgumentParser(description=description)
    a.add_argument('fname', help='The filename of the factors datafile.')

    args = a.parse_args()
    fname = args.fname
    with open(fname, 'r') as f:
        lines = f.read().split('\n')
    header = [x for x in lines if 'mkt-rf' in x.lower()][0]
    end = [x for x in lines if 'copyright' in x.lower()][0]
    start = lines.index(header)
    end = lines.index(end)
    lines[start] = 'Date ' + lines[start]
    with open('factors.csv', 'w') as f:
        for line in lines[start:end]: f.write('%s\n' % ','.join(line.split()))

