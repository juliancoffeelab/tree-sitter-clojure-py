from importlib.resources import files
from pathlib import Path


def language() -> object:
    raise NotImplementedError(
        "Native tree-sitter binding is not wired yet; package scaffold is ready."
    )


def queries_dir() -> Path:
    return Path(files("tree_sitter_clojure").joinpath("queries"))
