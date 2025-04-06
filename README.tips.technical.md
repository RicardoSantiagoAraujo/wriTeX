### command for word count:
```
perl texcount.pl articles/{article_name}/elements/body.tex
```

### command for letter count (does not include spaces):
```
perl texcount.pl -char articles/{article_name}/elements/body.tex
```

### pandoc: command to convert to docx (MUST run in this file's root):
Beware that pandco will not be able to handle custom macros, so is not an appropriate solution for complex latex documents as is the case with arTeX.
```
pandoc -s --bibliography ../../articles_common_files/bibliography.bib --citeproc --csl ../../articles_common_files/{your_bib_style}.csl --biblatex *.tex -M reference-section-title=References -o main.docx
```

