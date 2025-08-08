# wriTeX: A LuaLaTeX articles template and Portfolio

A highly versatile and customisable LuaLaTeX template for writing modular articles and compiling them into a single portfolio.

### Requirements

#### On Windows

##### Recommended Set-up with Visual Studio Code:

- Install the LaTeX distribution [Miktex](https://miktex.org/download)
- Install the Pearl distribution [Strawberry](https://strawberryperl.com/)
- Install the Latex Workshop extension
- Ideally, set the compilation output path in **settings.json** to

```
"latex-workshop.latex.outDir": "%DIR%/auxiliary_files"
```

and add "-outdir=%OUTDIR%" as an argument in "latex-workshop.latex.recipes".

> You may need to restart Visual Studio Code or your machine.

### Suggested Usage:

You can pull the contents of this repository to the root one of your as follows:

- First, you add this repository as a remote to your own:

```
git remote add {desired name of remote}  {address of remote}
git remote add writex  https://github.com/RicardoSantiagoAraujo/wriTeX.git
```

- You can then simply pull from **writex** by specifying the remote. Use the option flag if you get an unrelated histories error.

```
git pull {name of remote} {branch to pull from} [--allow-unrelated-histories]
git pull writex main
```

- Alternatively, pull **writex** contents into target subfolder (replace "pull" with "add" the very first time if folder does not yet exist). The optional flag avoids copying the whole commit history;
```
git subtree pull [--squash] --prefix=<subfolder-path> <chosen-name> main
git subtree pull --squash --prefix=writex writex main
```
 
 Ideally, you wouldn't touch any of the existing files... instead, you should add new articles as needed based on the **wrtx_article_template**, as well as a create a new version of the portfolio based on the **wrtx_portfolio_template**.

### Troubleshooting compilation

- Use lualatex to compile
- Ensure required fonts are installed on the computer (even if there is a fallback system in place)
- Some packages might need to be installed, so ensure you have an internet connection
