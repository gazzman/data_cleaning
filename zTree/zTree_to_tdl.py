#!/usr/bin/python
import argparse
import csv
import sys
import re

LINEPARSE = re.compile("(^[0-9]+_[0-9]+\t[0-9]+\t)(globals|subjects|summary|session)\t(.*)")
IFS = '\r\n'

def xls_to_tdl(fname):
    """
    A method to split ztree data into tab-delimited files with headers
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
                                             LINEPARSE.match(line).group(3) ] 
                                         )
                                 )
            except ValueError:
                tables[key] += [ ''.join( [ LINEPARSE.match(line).group(1), 
                                            LINEPARSE.match(line).group(3) ] ) ]
            except KeyError:
                tables[key] = [ ''.join( [ "timestamp\tsession\t", 
                                           LINEPARSE.match(line).group(3) ] ) ]
        except AttributeError:
            pass
    for key in tables:
        with open('%s.tdl' % key.replace('\t', '_'), 'w') as o:
            o.write('\n'.join(tables[key]))

def sbj_to_tdl(fname, timestamp):
    """
    A method for transposing ztree questionnaire data
    """
    f = open(fname, 'r')
    lines = [ line.split('\t') for line in f.read().split(IFS) ]
    maxlen = max( [ len(line) for line in lines ] )
    times = ['timestamp'] + [timestamp]*(maxlen - 1)
    lines = [times] + [ line for line in lines if len(line) == maxlen ]
    lines = zip(*lines)
    lines = [ '\t'.join(line) for line in lines ]
    with open('%s_questionnaire.tdl' % timestamp, 'w') as o:
        o.write('\n'.join(lines))

if __name__ == '__main__':
    description = 'A simple utility for prepping ztree data for db insertion'
    datafile_help = 'The zTree datafile'
    q_help = 'The zTree questionnaire file and timestamp. Timestamp format is %%y%%m%%d_%%H%%M.'
    q_meta = ('questionnaire_file', 'timestamp')
    p = argparse.ArgumentParser(description=description)
    p.add_argument('datafile', help=datafile_help)
    p.add_argument('-q', nargs=2, metavar=q_meta, help=q_help)
    args = p.parse_args()

    xls_to_tdl(args.datafile)
    if args.q:
        sbj_to_tdl(*args.q)
