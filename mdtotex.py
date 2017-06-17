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
# Currently in table environment
# second value remembers headers
table = [False, [], 0]

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
        # Table detection
        tables = l.split('|')
        if tables[0] == '':
            del tables[0]
        if tables[-1] == '\n':
            del tables[-1]
        if not table[0] and len(tables) >= 2:
            # No table currently, looking
            # for dashes
            a = True
            for k in tables[1:-1]:
                if not re.search(r'^ *-{3} *', k):
                    a = False
            if a and table[1]:
                # We got the dashes and header
                table[0] = True
                table[2] = len(tables)
                spec = ['l' for e in table[1]]
                spec = ' | '.join(spec)
                n.write(r'\begin{tabular}{' + spec + '}' + '\n')
                n.write(' & '.join(table[1]) + r'\\' + '\n')
                n.write(r'\hline' + '\n')
                table[1] = []
                # We're not writing the dashes ever
                l = ""
            elif not table[1]:
                table[1] = tables
                # We're keeping the headers in case
                l = ""
            else:
                # False alert on the headers
                n.write(' | '.join(table[1]))
                table[1] = []
        elif table[0]:
            if len(tables) == table[2]:
                n.write(' & '.join(tables) + r'\\' + '\n')
                # Don't write raw MD
                l = ""
            else:
                # End of the table
                table = [False, [], 0]
                n.write(r'\end{tabular}' + '\n')

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
