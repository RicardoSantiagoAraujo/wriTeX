# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'arTeX scripts'
copyright = '2025, Ricardo Santiago Araújo'
author = 'Ricardo Santiago Araújo'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.duration', # to &see a short durations report at the end of the console output
    'sphinx.ext.doctest', # to perform unit tests with command 'make doctest'
    'sphinx.ext.autodoc', # reuse Python docstrings in the documentation, rather than having to write the information in two places.
    'sphinx.ext.autosummary', # generates documents that contain all the necessary autodoc directives.
    'sphinx.ext.napoleon',  # For Google/NumPy style docstrings
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


# -- Options for EPUB output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-epub-output

epub_show_urls = 'footnote'
