import os
import shutil
from pathlib import Path


def clear_folder_contents(folder_path: str) -> None:
    folder = Path(folder_path)

    if not folder.exists():
        print(f"A pasta {folder_path} não existe.")
        return

    if not folder.is_dir():
        print(f"{folder_path} não é uma pasta.")
        return

    for item in folder.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception as e:
            print(f"Erro ao deletar {item}: {e}")


def clear_data_folders() -> None:
    folders_to_clear = [
        "data/processed",
        "data/raw/monthly_cdi",
        "data/raw/yearly_cdi",
        "data/raw/ipca"
    ]

    for folder in folders_to_clear:
        print(f"Limpando pasta: {folder}")
        clear_folder_contents(folder)

    print("Limpeza concluída.")
