# mdtotex

A quick script to convert you markdown files to LaTeX files, without using (too many) extra latex packages. The main advantage over Pandoc and other conversion tools is how lightweight this script is (Pandoc makes package-heavy xetex files).

## Usage

    python mdtotex.py -p package1,package2 -a "Firstname Lastname" -l language --nomargin path/to/markdownfile.md

The packages and author parameters are optional, and will add `usepackage` and `author` commands in the file. Parameters in package inclusion aren't supported yet, though if that's what you need then you're probably better off writing `.tex` files directly.
You can also specify parameters later in the file for some packages (e.g. `\geometry{...}`).

The `--nomargin` option uses the `geometry` package to thin the (huge) default latex margins, which is more in tune with what markdown is used for.

The `-l` option specifies a language to be used with `babel` (which must therefore be installed for LaTeX).
It also enables the `T1` font encoding so that any accents are properly managed.

If the first line is a `# Title`, it will be used to make a document title (`\maketitle`) along with the author parameter if it was passed. Therefore, the author parameter is only used if you include a title.

It will output a file of the same name in the same directory but with the `.tex` extension. You will have to build the pdf yourself with `pdflatex` for instance.

### Requires **Python 3.6+**.

The `nomargin` and `-l` options require `geometry` and `babel` packages.

## Changelog

### v0.4 (22 July 2018)

Added language, margin and table of contents options.
Manages font encoding in foreign languages.

Tables now use double lines after header and single lines on rows, more in line with the way markdown renderers usually work.

### v0.3 (12 November 2017)

Added title, author and package options.

### v0.2 (22 June 2017)

Support for tables and `inline code` added.

### v0.1 (4 June 2017)

Initial version, supports titles, code blocks, bullet lists, *italics* and **bold**.
