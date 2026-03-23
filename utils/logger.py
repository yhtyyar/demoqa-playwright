"""Модуль логирования."""

import logging

from config.settings import Settings


def setup_logger(name: str = "demoqa_tests") -> logging.Logger:
    """Настроить и вернуть логгер.

    Args:
        name: Имя логгера.

    Returns:
        Настроенный экземпляр Logger.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Файловый обработчик
    log_file = Settings.REPORTS_DIR / "test.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # Формат
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
