#!/usr/bin/python
import argparse
import csv
import sys
import lxml.etree as etree

def tag_searcher(tag, tag_dict):
    children = tag.findall("*")
    if len(children) == 0: 
        try:
            tag_dict[tag.tag].append(tag.attrib)
        except KeyError:
            tag_dict[tag.tag] = [tag.attrib]
    else:
        for child in children:
            tag_searcher(child, tag_dict)

if __name__ == '__main__':
    description = 'A script that stores child tags and attributes in tables.'
    p = argparse.ArgumentParser(description=description)
    p.add_argument('xml_file', type=str, help='name of xml file')
    args = p.parse_args()

    with open(args.xml_file) as x:
        tree = etree.parse(x)
    tag_dict ={}
    tag_searcher(tree, tag_dict)

    for tag in tag_dict:
        with open('%s.csv' % tag, 'w') as f:
            csvfile = csv.DictWriter(f, tag_dict[tag][0].keys())
            f.write(','.join(csvfile.fieldnames) + '\n')
            csvfile.writerows(tag_dict[tag])
