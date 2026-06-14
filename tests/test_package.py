from pathlib import Path

import pytest

import tree_sitter_clojure


def test_queries_dir_contains_highlights_query() -> None:
    queries_dir = tree_sitter_clojure.queries_dir()
    assert queries_dir.is_dir()
    assert (queries_dir / "highlights.scm").is_file()


def test_language_placeholder_is_explicit() -> None:
    with pytest.raises(NotImplementedError):
        tree_sitter_clojure.language()
