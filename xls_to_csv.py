#!/usr/bin/python
import argparse
import sys

from xlrd import open_workbook

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('fname')
    p.add_argument('--header', action='store_true')
    args = p.parse_args()

    wb = open_workbook(sys.argv[1])
    sh = wb.sheet_by_index(0)

    if args.header:
        print ','.join([ ('%s' % y).lower() for y in sh.row_values(0)])
    else:
        for x in xrange(1, sh.nrows):
            print ','.join([ "'%s'" % y for y in sh.row_values(x) if str(y) != '' ])
