"""
File organization and archiving.
"""

import logging
import shutil
from datetime import datetime
from pathlib import Path

logger = logging.getLogger('fincat.file_archiver')


def archive_file(filepath: Path, processed_folder: Path, success: bool = True) -> Path:
    """
    Move file to processed folder or errors folder.

    Args:
        filepath: Path to file to archive
        processed_folder: Base processed folder
        success: True for successful processing, False for errors

    Returns:
        Path where file was archived
    """
    # Determine destination folder
    if success:
        dest_folder = processed_folder
    else:
        dest_folder = processed_folder / 'errors'

    # Create destination folder
    dest_folder.mkdir(parents=True, exist_ok=True)

    # Determine destination path
    filename = filepath.name
    dest_path = dest_folder / filename

    # Handle duplicates by adding timestamp
    if dest_path.exists():
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        stem = dest_path.stem
        suffix = dest_path.suffix
        dest_path = dest_folder / f"{stem}_{timestamp}{suffix}"
        logger.debug(f"Destination exists, using: {dest_path.name}")

    # Move file
    shutil.move(str(filepath), str(dest_path))

    status = "✅" if success else "❌"
    relative_path = dest_path.relative_to(processed_folder.parent)
    logger.info(f"{status} Archived: {filepath.name} → {relative_path}")

    return dest_path
