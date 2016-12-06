#!/usr/bin/env python

# Replace every instance of certain words with a given replacement;
# As an example say replace every word 'zero' with '0', 'temp' with 'bob', and say 'garbage' with 'nothing'.
replacements = {'zero':'0', 'temp':'bob', 'garbage':'nothing'}

# OPTION 1 ----------------------------------------------------------------------------------------------------------
# Use a temp file
with open('path/to/input/file') as infile, open('path/to/output/file', 'w') as outfile:
    for line in infile:
        for src, target in replacements.iteritems():
            line = line.replace(src, target)
        outfile.write(line)
        
# OPTION 2 ----------------------------------------------------------------------------------------------------------
# Read your entire source file into memory avoiding to use a temp file
lines = []
with open('path/to/input/file') as infile:
    for line in infile:
        for src, target in replacement.iteritems():
            line = line.replace(src, target)
        lines.append(line)
with open('path/to/input/file', 'w') as outfile:
    for line in lines:
        outfile.write(line)


# OPTION 3 ----------------------------------------------------------------------------------------------------------        
# The shortest way would probably be to use the fileinput module. 
# For example, the following adds line numbers to a file, in-place:

import fileinput

for line in fileinput.input('spam.txt', inplace=True):
    print(line.replace('old', 'new'), end='')
    
    
    
