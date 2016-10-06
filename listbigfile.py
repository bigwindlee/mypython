#!/usr/bin/env python

'''
Traverse directory tree, list the top size files.
'''

import os, sys

TOP_COUNT_DEFAULT = 5

if not sys.argv[1:]:
    print('Usage:\n\t%s [pathname [topcount]]' % os.path.basename(sys.argv[0]))
    os._exit(1)

dstdir = sys.argv[1]
topcount = int(sys.argv[2]) if len(sys.argv) > 2 else TOP_COUNT_DEFAULT
allsizes = []

if not os.path.isdir(dstdir):
    print('Error: %s is not a directory.' % dstdir)
    os._exit(2)

for (dirname, subshere, fileshere) in os.walk(dstdir):
    for fname in fileshere:
        fullname = os.path.join(dirname, fname)
        fullsize = os.path.getsize(fullname)
        allsizes.append((fullsize, fullname))
        
allsizes.sort(reverse = True)

for item in allsizes[:topcount]:
    print('%d\t%s' % (item[0], item[1]))
    