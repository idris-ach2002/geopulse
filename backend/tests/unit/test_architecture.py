import ast
from pathlib import Path

FORBIDDEN_ROOT_MODULES = {
    "fastapi",
    "sqlalchemy",
    "redis",
    "kafka",
}


def _imports(source: str) -> set[str]:
    tree = ast.parse(source)
    modules: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split(".")[0])

        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".")[0])

    return modules


def test_domain_has_no_framework_dependencies() -> None:
    domain = Path(__file__).parents[2] / "src" / "geopulse" / "domain"

    for python_file in domain.rglob("*.py"):
        imported = _imports(python_file.read_text(encoding="utf-8"))
        forbidden = imported & FORBIDDEN_ROOT_MODULES

        assert not forbidden, f"{python_file} imports forbidden dependencies: {sorted(forbidden)}"
