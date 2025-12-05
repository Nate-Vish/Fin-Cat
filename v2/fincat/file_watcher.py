"""
File system monitoring using watchdog.
"""

import logging
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .utils import wait_for_file_stability

logger = logging.getLogger('fincat.file_watcher')


class XLSFileHandler(FileSystemEventHandler):
    """Handler for XLS/XLSX file events."""

    def __init__(self, callback, config):
        """
        Initialize handler.

        Args:
            callback: Function to call when file detected
            config: Configuration dictionary
        """
        super().__init__()
        self.callback = callback
        self.stability_wait = config['processing']['file_stability_wait']

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        filepath = Path(event.src_path)

        # Check if XLS or XLSX file
        if filepath.suffix.lower() not in ['.xls', '.xlsx']:
            return

        # Ignore hidden/temp files
        if filepath.name.startswith('.') or filepath.name.startswith('~'):
            return

        logger.info(f"Detected new file: {filepath.name}")

        # Wait for file to be fully written
        if wait_for_file_stability(filepath, check_interval=1, max_wait=self.stability_wait):
            logger.debug(f"File stable: {filepath.name}")
            self.callback(filepath)
        else:
            logger.warning(f"File may not be complete: {filepath.name}")
            self.callback(filepath)  # Try anyway


class FileWatcher:
    """Watch folder for new XLS/XLSX files."""

    def __init__(self, config: dict, callback):
        """
        Initialize file watcher.

        Args:
            config: Configuration dictionary
            callback: Function to call when file detected (receives Path)
        """
        self.config = config
        self.input_folder = Path(config['folders']['input'])
        self.input_folder.mkdir(parents=True, exist_ok=True)

        self.observer = Observer()
        self.handler = XLSFileHandler(callback, config)

    def start(self):
        """Start watching the input folder."""
        self.observer.schedule(
            self.handler,
            str(self.input_folder),
            recursive=False
        )
        self.observer.start()
        logger.info(f"Monitoring folder: {self.input_folder}")

    def stop(self):
        """Stop watching."""
        self.observer.stop()
        self.observer.join()
        logger.info("File monitoring stopped")
