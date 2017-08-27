# mdtotex

A quick script to convert you markdown files to LaTeX files, without using any extra latex packages. The main advantage over Pandoc and other conversion tools is how lightweight this script is (Pandoc makes package-heavy xetex files).

## Usage

    python mdtotex.py path/to/markdownfile.md

Will output a file of the same name in the same directory but with the `.tex` extension.

### Requires **Python 3.6**.

## Changelog

### v0.2 (22 June 2017)

Support for tables and inline code added.

### v0.1 (4 June 2017)

Initial version, supports titles, code blocks, bullet lists, *italics* and **bold**.
