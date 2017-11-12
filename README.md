# mdtotex

A quick script to convert you markdown files to LaTeX files, without using any extra latex packages. The main advantage over Pandoc and other conversion tools is how lightweight this script is (Pandoc makes package-heavy xetex files).

## Usage

    python mdtotex.py -p package1,package2,package3 -a Firstname\ Lastname path/to/markdownfile.md

The packages and author parameters are optional, and will add `usepackage` and `author` commands in the file. Parameters in package inclusion aren't supported yet, though if that's what you need then you're probably better off writing `.tex` files directly.

If the first line is a `# Title`, it will be used to make a document title (`maketitle`) along with the author parameter if it was passed. Therefore, the author parameter is only used if you include a title.

Will output a file of the same name in the same directory but with the `.tex` extension. You will have to build the pdf yourself with `pdflatex` or the such.

### Requires **Python 3.6+**.

## Changelog

### v0.3 (12 November 2017)

Added title, author and package options.

### v0.2 (22 June 2017)

Support for tables and inline code added.

### v0.1 (4 June 2017)

Initial version, supports titles, code blocks, bullet lists, *italics* and **bold**.
