from pathlib import Path

from tree_sitter import Language, Parser, Query

import tree_sitter_clojure


def test_language_can_build_a_parser() -> None:
    language = Language(tree_sitter_clojure.language())
    parser = Parser(language)
    tree = parser.parse(b"(ns demo)\n(defn add [x y] (+ x y))\n")

    assert tree.root_node.type == "source"
    assert tree.root_node.named_child_count >= 2


def test_bundled_queries_compile() -> None:
    query_dir = tree_sitter_clojure.queries_dir()
    highlights = query_dir / "highlights.scm"
    language = Language(tree_sitter_clojure.language())

    query = Query(language, highlights.read_text())

    assert isinstance(query_dir, Path)
    assert highlights.exists()
    assert query.pattern_count > 0
