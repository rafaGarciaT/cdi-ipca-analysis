import logging
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Formatter customizado com cores para console"""

    COLORS = {
        'DEBUG': Fore.WHITE,
        'INFO': Fore.WHITE,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Adiciona cores ao nível do log para saída no console.

        Args:
            record (logging.LogRecord): O registro de log a ser formatado.

        Returns:
            str: A string formatada do registro de log, com cores aplicadas ao nível.
        """
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


class Logger:
    """Classe de logger personalizada para o pipeline, com suporte a logs em arquivo e console colorido.

    Attributes:
        logger (logging.Logger): O objeto logger do Python utilizado para registrar mensagens de log.
    """
    def __init__(self, name: str, log_dir: Path = None) -> None:
        """Inicializa o logger, configurando os handlers para arquivo e console.

        Args:
            name (str): O nome do logger, geralmente o nome do módulo ou classe que o utiliza.
            log_dir (Path, optional): O diretório onde os arquivos de log serão armazenados. Se não for fornecido, será criado um diretório "logs" no local do script.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            if log_dir is None:
                log_dir = Path("logs")

            log_dir.mkdir(exist_ok=True)

            log_file = log_dir / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            console_handler = logging.StreamHandler()

            formatter = logging.Formatter(
                '[%(levelname)s] %(asctime)s -- %(name)-10s -- %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            console_formatter = ColoredFormatter(
                '[%(levelname)s] %(asctime)s -- %(name)-10s -- %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            file_handler.setFormatter(formatter)
            console_handler.setFormatter(console_formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def debug(self, message: str):
        self.logger.debug(message)
