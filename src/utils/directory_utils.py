import shutil
from pathlib import Path
from src.utils.logger import Logger

logger = Logger("dir_utils")

def clear_folder_contents(folder_path: str) -> None:
    """Deleta todos os arquivos e subpastas dentro da pasta especificada."""
    folder = Path(folder_path)

    if not folder.exists():
        logger.warning(f"A pasta {folder_path} não existe.")
        return

    if not folder.is_dir():
        logger.warning(f"{folder_path} não é uma pasta.")
        return

    for item in folder.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception as e:
            logger.warning(f"Erro ao deletar {item}: {e}")


def clear_data_folders() -> None:
    """Limpa o conteúdo das pastas de dados brutos e processados."""
    folders_to_clear = [
        "data/processed",
        "data/raw/cdi",
        "data/raw/ipca"
    ]

    logger.info(f"Iniciando limpeza das pastas: {', '.join(folders_to_clear)}")

    for folder in folders_to_clear:
        clear_folder_contents(folder)

    logger.info(f"Limpeza concluida")
