#!/usr/bin/python
from collections import OrderedDict
from StringIO import StringIO
import argparse
import csv
import sys
import re

LINEPARSE = re.compile("(^[0-9]+_[0-9]+\t[0-9]+\t)(globals|subjects|summary|session)\t(.*\t$)")
IFS = '\r\n'

def clean_line(line):
    while '\t-\t' in line:
        line = line.replace('\t-\t', '\t\t')
    return line[:-1]

def tdl_to_csv(filename, list_of_strings, delim='\t'):
    """
    Write a delimited list of strings to a csv file.
    First row must be the header.
    """
    header = list_of_strings[0].split(delim)
    data = [ dict(zip(header, line.split(delim))) for line in list_of_strings[1:] ]
    data = [OrderedDict(zip(header,header))] + data
    o = csv.DictWriter(open(filename, 'w'), header)
    o.writerows(data)

def xls_to_csv(fname):
    """
    A method to split ztree data into csv files with headers
    """
    f = open(fname, 'r')
    lines = f.read().split(IFS)
    tables = {}
    for line in lines:
        try:
            key = ''.join( [ LINEPARSE.match(line).group(1), 
                             LINEPARSE.match(line).group(2) ] )
            try:
                tables[key].index(''.join( 
                                           [ "timestamp\tsession\t", 
                                             clean_line(LINEPARSE.match(line).group(3)) ] 
                                         )
                                 )
            except ValueError:
                tables[key] += [ ''.join( [ LINEPARSE.match(line).group(1), 
                                            clean_line(LINEPARSE.match(line).group(3)) ] ) ]
            except KeyError:
                tables[key] = [ ''.join( [ "timestamp\tsession\t", 
                                           clean_line(LINEPARSE.match(line).group(3)) ] ) ]
        except AttributeError:
            pass
    for key in tables:
        tdl_to_csv('%s.csv' % key.replace('\t', '_'), tables[key])

def sbj_to_csv(fname, timestamp):
    """
    A method for writing ztree questionnaire data to csv
    """
    f = open(fname, 'r')
    lines = [ line.split('\t') for line in f.read().split(IFS) ]
    maxlen = max( [ len(line) for line in lines ] )
    times = ['timestamp'] + [timestamp]*(maxlen - 1)
    lines = [times] + [ line for line in lines if len(line) == maxlen ]
    lines = zip(*lines) # this transposes the data
    lines = [ '\t'.join(line) for line in lines ]
    tdl_to_csv('%s_questionnaire.csv' % timestamp, lines)

if __name__ == '__main__':
    description = 'A simple utility for prepping ztree data for db insertion'
    datafile_help = 'The zTree datafile'
    q_help = 'The zTree questionnaire file and timestamp. Timestamp format is %%y%%m%%d_%%H%%M.'
    q_meta = ('questionnaire_file', 'timestamp')
    p = argparse.ArgumentParser(description=description)
    p.add_argument('datafile', help=datafile_help)
    p.add_argument('-q', nargs=2, metavar=q_meta, help=q_help)
    args = p.parse_args()

    xls_to_csv(args.datafile)
    if args.q:
        sbj_to_csv(*args.q)
