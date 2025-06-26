
import logging
from pathlib import Path

def setup_logging(name=__name__) -> logging.Logger:
    base_dir = Path(__file__).resolve().parent
    logging_file = base_dir / "logging.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Evita múltiplos handlers ao usar em vários arquivos
    if not logger.handlers:

        # Log para arquivo
        file_handler = logging.FileHandler(logging_file)
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        # (Opcional) Log no terminal
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
