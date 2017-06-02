"""Converts markdown files to LaTeX files with
basic formatting only.

Suitable only for python 3.6+."""

import sys
import os
import re

# Checks if the previous files exists and opens it
filename = sys.argv[1]
if not os.path.exists(filename):
    raise FileNotFoundError
f = open(filename, 'r')

# Generates the new filename and opens it,
# if it does not already exist
newfile = os.path.splitext(filename)
newfile = newfile[0] + ".tex"
if os.path.exists(newfile):
    raise FileExistsError
n = open(newfile, 'w')
print(f"Writing to {newfile}...")

for l in f.readlines():
    # Amount of open brackets
    o = 0
    title = re.search(r"^\#{1,6}", l)
    if title:
        importance = len(title.group(0))
        titlefmts = ['', 'part', 'chapter', 'section',
                     'subsection', 'subsubsection', 'paragraph']
        n.write("\\" + titlefmts[importance] + "{")
        l = re.sub(r"^\#{1,6}[ ]?", "", l)

    n.write(l.rstrip())

    if title:
        n.write("}")

    n.write('\n')

f.close()
n.close()
