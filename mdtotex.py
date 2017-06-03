"""Converts markdown files to LaTeX files with
basic formatting only.

Suitable only for python 3.6+."""

import sys
import os
import re

# Checks if the previous files exists and opens it
filename = sys.argv[1]
if not os.path.exists(filename):
    raise FileNotFoundError("Couldn't find target")
f = open(filename, 'r')

# Generates the new filename and opens it,
# if it does not already exist
newfile = os.path.splitext(filename)
newfile = newfile[0] + ".tex"
if os.path.exists(newfile):
    raise FileExistsError("Target file exists")
n = open(newfile, 'w')
print(f"Writing to {newfile}...")

# Initial text
n.write(r'\documentclass{article}' + '\n')
## Noone wants indented paragraphs in md
n.write(r'\setlength{\parindent}{0pt}')
n.write(r'\begin{document}' + '\n\n')

for l in f.readlines():
    # Amount of open brackets, parenthesis and square
    # brackets respectively
    o = [0, 0, 0]

    # Title detection
    title = re.search(r"^\#{1,6}", l)
    if title:
        importance = len(title.group(0))
        titlefmts = ['', 'part*', 'section*', 'subsection*',
                     'subsubsection*', 'paragraph', 'subparagraph']
        n.write("\\" + titlefmts[importance] + "{")
        o[0] += 1
        l = re.sub(r"^\#{1,6}[ ]?", "", l)
        # Escape any remaining hashes
        l = re.sub("#", r'\\#', l)

    # Bold text detection
    l = re.sub(r"\*\*(.*?)\*\*", r'\\textbf{\1}', l)
    # Italic text detection
    l = re.sub(r"\*(.*?)\*", r'\\textit{\1}', l)

    n.write(l.rstrip())

    if title:
        n.write("}")
        if importance >= 5:
            # Paragraphs and subparagraphs
            # don't newline
            n.write(r'\mbox{}\newline')
        o[0] -= 1

    n.write('\n')

    if sum(o) != 0:
        raise AssertionError("Bracket problem")

# End of the document
n.write('\n' + r'\end{document}' + '\n')

f.close()
n.close()
