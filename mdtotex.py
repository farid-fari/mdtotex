"""Converts markdown files to LaTeX files with
basic formatting only.

Suitable only for python 3.6 and higher."""

import sys
import os
import re

# Checks if the previous files exists and opens it
filename = sys.argv[1]
if not os.path.exists(filename):
    raise FileNotFoundError("Couldn't find target")
f = open(filename, 'r', encoding='utf-8')

# Generates the new filename and opens it,
# if it does not already exist
newfile = os.path.splitext(filename)
newfile = newfile[0] + ".tex"
if os.path.exists(newfile):
    raise FileExistsError("Target file exists")
n = open(newfile, 'w', encoding='utf-8')
print(f"Writing to {newfile}...")

# Initial text
n.write(r'\documentclass{article}' + '\n')
## Noone wants indented paragraphs in md
n.write(r'\setlength{\parindent}{0pt}' + '\n')
# To save accents and the such
n.write(r'\usepackage[utf8]{inputenc}' + '\n')
n.write(r'\begin{document}' + '\n\n')

# Currently in itemized environment
itemize = False
# Currently in table environment
# second value remembers headers
# third the number of columns
table = [False, "", 0]

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
        if tables and re.search(r'^\s*$', tables[0]):
            del tables[0]
        if tables and re.search(r'^\s*$', tables[-1]):
            del tables[-1]
        cols = len(tables)

        if not table[0] and cols >= 2:
            # No table currently, looking
            # for dashes
            a = True
            for k in tables[1:-1]:
                if not re.search(r'^ *-{3} *', k):
                    a = False
            if a and table[1] and cols == table[2]:
                # We got the dashes and header and
                # the right amount of columns
                table[0] = True
                head = table[1].split('|')
                borders = ['', '']
                if head and re.search(r'^\s*$', head[0]):
                    del head[0]
                    borders[0] = '|'
                if head and re.search(r'^\s*$', head[-1]):
                    del head[-1]
                    borders[1] = '|'

                spec = ['l' for e in head]
                spec = ' | '.join(spec)
                n.write(r'\begin{tabular}{ ' + borders[0] + spec + borders[1] + ' }' + '\n')
                n.write(' & '.join(head) + r'\\' + '\n')
                n.write(r'\hline' + '\n')
                table[1] = ""
                # We're not writing the dashes ever
                l = ""
            elif not table[1]:
                table[1] = l
                table[2] = len(tables)
                # We're keeping the headers for later
                l = ""
            else:
                # False alert on the headers: either
                # wrong cols or not enough dashes
                n.write(table[1])
                table[1] = ""

        elif table[0]:
            if len(tables) == table[2]:
                n.write(' & '.join(tables) + r'\\' + '\n')
                # Don't write raw MD
                l = ""
            else:
                # End of the table
                table = [False, "", 0]
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
if table[0]:
    # End of tabular environment at end of doc
    n.write(r'\end{tabular}')
    table = [False, "", 0]

# End of the document
n.write('\n' + r'\end{document}' + '\n')

f.close()
n.close()
