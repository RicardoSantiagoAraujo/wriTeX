# arTeX: A LuaLaTeX articles template and Portfolio
A highly versatile and customisable LuaLaTeX template for writing modular articles and compiling them into a single portfolio.

### Requirements
#### On Windows
##### Recommended Set-up with Visual Studio Code:
- Install the LaTeX distribution [Miktex](https://miktex.org/download)
- Install the Pearl distribution [Strawberry](https://strawberryperl.com/)
- Install the Latex Workshop extension
- Ideally, set the compilation output path in **settings.json** to

````
"latex-workshop.latex.outDir": "%DIR%/auxiliary_files"
````

and add "-outdir=%OUTDIR%" as an argument in "latex-workshop.latex.recipes".


> You may need to restart Visual Studio Code or your machine.


###  Universal tips for body:
- Reduce sentences!!!
- pyramid structure: from the particular to the general!!!
- Subdivide into smaller titled sections: bonus point of section title is lifted from the text
- Some suspence is OK, but the chapeau should include the who/what/where/when directly. Leave the suspence for the why/how
- Avoid the passive voice... it is more difficult to read


### Troubleshooting compilation
- Use lualatex to install
- Ensure required fonts are installed on the computer (even if there is a fallback system in place)
- Some packages might need to be installed, so ensure you have an internet connection

### command for word count:
```
perl texcount.pl articles/{article_name}/elements/body.tex
```

### command for letter count (does not include spaces):
```
perl texcount.pl -char articles/{article_name}/elements/body.tex
```

### pandoc: command to convert to docx (MUST run in this file's root):
```
pandoc -s --bibliography ../../articles_common_files/bibliography.bib --citeproc --csl ../../articles_common_files/{your_bib_style}.csl --biblatex *.tex -M reference-section-title=References -o main.docx
```

###  Bibliography
####  Tips
- With newer versions of biblatex (≥2.0) and biber (≥0.9.8) you can define your entries as normal and use the "IDS" field for extra citations keys:

```
@BOOK{key,
  IDS = {key2, key3, ..., keyn},
  .
  .
}
```

#### Clearing Biber cache:
https://tex.stackexchange.com/questions/140814/biblatex-biber-fails-with-a-strange-error-about-missing-recode-data-xml-file

If citations are coming out empty ([citation_code]), you might need to clear the biber cache: Biber creates binaries in a cache folder, and sometimes that can get corrupted. In order to solve the problem, you need to manually delete the cache folders.
You can find the location of the cache folder by looking at the .blg file, or by using the command.
```
biber --cache
```
On Linux and Mac, this can be combined to delete the offending folder in one command:
```
rm -rf `biber --cache`
```

Additionally, try this (if you get an error, "cd" into folder location of the "auxiliary_files" folder):
```
biber path/to/latex/output/files/without/extension
```