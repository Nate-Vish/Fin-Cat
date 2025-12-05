"""
Logging setup and configuration.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(config: dict) -> logging.Logger:
    """
    Configure application logging.

    Args:
        config: Configuration dictionary

    Returns:
        Configured logger
    """
    # Create logs directory
    log_dir = Path(config['folders']['logs'])
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create rotating file handler
    log_file = log_dir / 'fincat.log'
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=config['logging']['max_size_mb'] * 1024 * 1024,
        backupCount=config['logging']['backup_count'],
        encoding='utf-8'
    )

    # Create console handler
    console_handler = logging.StreamHandler()

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger('fincat')
    root_logger.setLevel(getattr(logging, config['logging']['level']))
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return root_logger
