"""Configuración de Sphinx para la documentación del proyecto."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

project = "Task & Client Manager"
author = "Penélope J. Nieves"
release = "1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
    "sphinxcontrib.mermaid",
]

templates_path = ["_templates"]
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_css_files = [
    "custom.css",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
