import subprocess
from pathlib import Path


class TestDependencies:
    """Valida gerenciamento de dependências."""

    def test_no_security_vulnerabilities(self):
        """Não deve haver vulnerabilidades conhecidas."""
        result = subprocess.run(
            ["pip-audit"],
            capture_output=True
        )
        # pip-audit retorna 0 se não houver vulnerabilidades
        assert result.returncode == 0, \
            f"Vulnerabilidades encontradas:\n{result.stdout.decode()}"

    def test_no_unpinned_dependencies(self):
        """Dependências devem ter versões fixas."""

        requirements_path = Path(__file__).parent.parent.parent / "requirements.txt"

        with open(requirements_path) as f:
            lines = f.readlines()

        unpinned = [line.strip() for line in lines
                    if line.strip() and not any(op in line for op in ['==', '>=', '<='])]

        assert not unpinned, \
            f"Dependências sem versão fixada: {', '.join(unpinned)}"
