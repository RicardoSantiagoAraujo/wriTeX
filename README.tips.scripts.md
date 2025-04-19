# artTeX scripts

This projects includes a bunch of functionalities incapsulated in the scripts module. These range from practical QOL features to powerful tools.
You can run any of the
The scripts module is divided into submodules, which you can run from the project root directory. Documentation for the scripts module is found inside the scripts/documentation directory.

## INIT

Creates a new article or portfolio based on the respective template.

### Usage:
#### For articles:
```
python -m scripts.init.article
```
#### For portfolios:
```
python -m scripts.init.article
```


## EXPAND

Creates an existing article into a single files for ease of sharing as a single file, with currently only a few limitations.

This feature does not work for portfolios.

### Usage:
```
python -m scripts.expand.article
```


## COMPILE

Compilation of an existing article or portfolio version.


### Usage:
```
python -m scripts.compile [document name] [compilation mode] [--watch] [--timer] [--help] [--verbose]
```


## CONVERT:

Convert latex document into an html version for web publication.
