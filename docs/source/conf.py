# pylint: skip-file
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join("..", "..", ".")))
import understatapi
from datetime import datetime as dt

project = "understatAPI"
copyright = f"{dt.today().year}, Brendan Collins"
author = "Brendan Collins"

release = understatapi.__version__
version = understatapi.__version__

source_suffix = [".rst", ".md"]

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.doctest",
    "sphinx_rtd_theme",
    "m2r2",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]

exclude_patterns = []

master_doc = "index"

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 2,
    "titles_only": False,
}
html_context = {
    "github_user_name": "collinb9",
    "github_repo_name": "collinb9/understatAPI",
    "project_name": "understatAPI",
}

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": True,
    "private-members": True,
    "special-members": "__init__",
    "show-inheritance": True,
}

html_static_path = ["_static"]

autosummary_generate = True

autosectionlabel_prefix_document = True


def skip(app, what, name, obj, would_skip, options):
    """
    Define which methods should be skipped in the documentation
    """
    if obj.__doc__ is None:
        return True
    return would_skip


def process_docstring(app, what, name, obj, options, lines):
    """
    Process docstring before creating docs
    """
    for i in range(len(lines)):
        if "#pylint" in lines[i]:
            lines[i] = ""


def setup(app):
    app.connect("autodoc-skip-member", skip)
    app.connect("autodoc-process-docstring", process_docstring)
