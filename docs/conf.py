"""Sphinx configuration."""
from datetime import datetime


project = "Ecs Tasks Ops"
author = "Pablo Palazon"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_autodoc_typehints"]
autodoc_typehints = "description"
