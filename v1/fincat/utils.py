"""
Utility functions for FinCat.
"""

import hashlib
import json
import time
from datetime import datetime
from pathlib import Path


def wait_for_file_stability(filepath: Path, check_interval: int = 1,
                            max_wait: int = 10) -> bool:
    """
    Wait until file size stops changing (file is fully written).

    Args:
        filepath: Path to file
        check_interval: Seconds between size checks
        max_wait: Maximum seconds to wait

    Returns:
        True if file stable, False if timeout
    """
    if not filepath.exists():
        return False

    previous_size = -1

    for _ in range(max_wait):
        try:
            current_size = filepath.stat().st_size

            if current_size == previous_size and current_size > 0:
                return True

            previous_size = current_size
            time.sleep(check_interval)

        except (OSError, IOError):
            # File might be temporarily inaccessible
            time.sleep(check_interval)
            continue

    return False


def calculate_checksum(filepath: Path) -> str:
    """
    Calculate SHA256 checksum of file.

    Args:
        filepath: Path to file

    Returns:
        Hex digest of file checksum
    """
    sha256 = hashlib.sha256()

    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


def load_processing_history(data_folder: Path) -> dict:
    """
    Load processing history from JSON file.

    Args:
        data_folder: Data folder path

    Returns:
        Processing history dictionary
    """
    history_file = data_folder / '.processing_history.json'

    if history_file.exists():
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    return {"processed_files": []}


def save_processing_history(data_folder: Path, history: dict):
    """
    Save processing history to JSON file.

    Args:
        data_folder: Data folder path
        history: Processing history dictionary
    """
    history_file = data_folder / '.processing_history.json'

    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def is_already_processed(filepath: Path, history: dict) -> bool:
    """
    Check if file has already been processed.

    Args:
        filepath: Path to file
        history: Processing history dictionary

    Returns:
        True if already processed, False otherwise
    """
    checksum = calculate_checksum(filepath)

    processed_checksums = [
        entry['checksum'] for entry in history.get('processed_files', [])
    ]

    return checksum in processed_checksums


def mark_as_processed(filepath: Path, data_folder: Path, transaction_count: int):
    """
    Mark file as processed in history.

    Args:
        filepath: Path to processed file
        data_folder: Data folder path
        transaction_count: Number of transactions processed
    """
    history = load_processing_history(data_folder)

    entry = {
        "filename": filepath.name,
        "checksum": calculate_checksum(filepath),
        "processed_at": datetime.now().isoformat(),
        "transaction_count": transaction_count,
        "status": "success"
    }

    history['processed_files'].append(entry)

    save_processing_history(data_folder, history)


def create_folders(config: dict):
    """
    Create all required folders if they don't exist.

    Args:
        config: Configuration dictionary
    """
    folders = [
        config['folders']['input'],
        config['folders']['processed'],
        config['folders']['data'],
        config['folders']['logs'],
        str(Path(config['folders']['processed']) / 'errors')
    ]

    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
