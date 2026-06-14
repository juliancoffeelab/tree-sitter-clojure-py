from importlib.resources import files
from pathlib import Path

from ._binding import language as _language

__all__ = ["language", "queries_dir"]


def language() -> object:
    return _language()


def queries_dir() -> Path:
    return Path(files("tree_sitter_clojure").joinpath("queries"))
