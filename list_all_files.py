#!/usr/bin/python
import argparse
import glob

def print_files(t, windows=False, s='/*', display=True):
    fs = []
    if t[-1] == '/': t = t[:-1]
    count = 1
    path = t + count*s
    f = glob.glob(path)
    while len(f) > 0:
        fs += f
        filepaths = '\n'.join(f)
        if display:
            if windows: print filepaths.replace('/', '\\')
            else: print filepaths
        count += 1
        path = t + count*s
        f = glob.glob(path)
    return fs
    
# For running from command line
if __name__ == "__main__":
    description = 'Print paths to all subfolders and files.'

    a = argparse.ArgumentParser(description=description)
    a.add_argument('-p', type=str, default='./', dest='top_level', 
                   help='The top-level path. Default is \'./\'.')
    a.add_argument('-w', dest='windows', action='store_true',
                   help='If set, changes forwardslashes to backslashes.')

    args = a.parse_args()
    print_files(args.top_level, args.windows)
