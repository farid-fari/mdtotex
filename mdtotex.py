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

# Currently in itemized environment
itemize = False

for l in f.readlines():
    # Amount of open brackets, parenthesis and square
    # brackets respectively
    o = [0, 0, 0]

    # Title detection
    title = re.search(r"^ {0,3}(\#{1,6})", l)
    if title:
        importance = len(title.group(1))
        titlefmts = ['', 'part*', 'section*', 'subsection*',
                     'subsubsection*', 'paragraph', 'subparagraph']
        n.write("\\" + titlefmts[importance] + "{")
        o[0] += 1
        l = re.sub(r"^ {0,3}\#{1,6} ?", "", l)
        # Escape any remaining hashes
        l = re.sub("#", r'\\#', l)

    # Bullet list detection
    bullet = re.search(r'^ {0,3}[-*] ', l)
    if bullet:
        if not itemize:
            n.write('\n' + r'\begin{itemize}' + '\n')
            itemize = True
        l = re.sub(r'^ {0,3}[-*]', r'\item ', l)
    elif itemize:
        # End of itemized environment
        n.write('\n' + r'\end{itemize}' + '\n')
        itemize = False

    # Code detection - cancels all future detections
    code = re.search(r'^    ', l)
    if code:
        l = re.sub(r'^    ', '\n' + r'\\begin{verbatim}' + '\n', l)
    else:
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
    if code:
        n.write('\n' + r'\end{verbatim}' + '\n')

    n.write('\n')

    if sum(o) != 0:
        raise AssertionError("Bracket problem")

if itemize:
    # End of itemized environment at end of doc
    n.write(r'\end{itemize}')
    itemize = False

# End of the document
n.write('\n' + r'\end{document}' + '\n')

f.close()
n.close()
