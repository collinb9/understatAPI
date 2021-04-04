# pylint: skip-file
import os
import sys
import understatapi
from datetime import datetime as dt

sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "understatapi")))

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

html_static_path = ["_static"]

autosummary_generate = True

autosectionlabel_prefix_document = True


def skip(app, what, name, obj, would_skip, options):
    """
    Define which methods should be skipped in the documentation
    """
    if what in ["function"]:
        return False
    if obj.__doc__ is None:
        return True
    if name in ["__init__"]:
        return False
    if name.startswith("__"):
        return True
    if name.startswith("_[a-z]"):
        return False
    return would_skip


def setup(app):
    app.connect("autodoc-skip-member", skip)
