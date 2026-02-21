import ast
import os
from pathlib import Path


class TestDocumentation:
    """Valida presença de documentação."""

    def test_all_modules_have_docstrings(self):
        """Todos os módulos devem ter docstrings."""
        src_path = Path("src")
        missing_docstrings = []

        for py_file in src_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            with open(py_file) as f:
                tree = ast.parse(f.read())
                if not ast.get_docstring(tree):
                    missing_docstrings.append(str(py_file))

        assert not missing_docstrings, \
            f"Arquivos sem docstring: {', '.join(missing_docstrings)}"

    def test_all_classes_have_docstrings(self):
        """Todas as classes devem ter docstrings."""
        src_path = Path("src")
        missing_docstrings = []

        for py_file in src_path.rglob("*.py"):
            with open(py_file) as f:
                tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        if not ast.get_docstring(node):
                            missing_docstrings.append(
                                f"{py_file}::{node.name}"
                            )

        assert not missing_docstrings, \
            f"Classes sem docstring: {', '.join(missing_docstrings)}"
