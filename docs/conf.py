"""Sphinx configuration."""
from datetime import datetime


project = "Ecs Tasks Ops"
author = "Pablo Palazon"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
autodoc_typehints = "description"
