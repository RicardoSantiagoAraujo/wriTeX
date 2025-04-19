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

#### Running Biber
Make sure to run it from directory where root tex file is located, and not to include file extension
```
biber path/to/output/files/without/extension
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