"""
Main entry point and orchestration for FinCat.
"""

import argparse
import logging
import sys
import time
from pathlib import Path

from .config import load_config
from .logger import setup_logging
from .file_watcher import FileWatcher
from .parser import ExcelParser
from .categorizer import Categorizer
from .excel_writer import ExcelWriter
from .file_archiver import archive_file
from .utils import (
    is_already_processed,
    mark_as_processed,
    load_processing_history,
    create_folders
)

logger = logging.getLogger('fincat.main')


def process_file(filepath: Path, config: dict, parser: ExcelParser,
                 categorizer: Categorizer, writer: ExcelWriter) -> bool:
    """
    Process a single file through the pipeline.

    Args:
        filepath: Path to the file to process
        config: Configuration dictionary
        parser: ExcelParser instance
        categorizer: Categorizer instance
        writer: ExcelWriter instance

    Returns:
        True if successful, False otherwise
    """
    start_time = time.time()
    logger.info(f"Processing {filepath.name}...")

    try:
        # Check if already processed
        data_folder = Path(config['folders']['data'])
        history = load_processing_history(data_folder)

        if is_already_processed(filepath, history):
            logger.info(f"Skipping {filepath.name} (already processed)")
            return True

        # Parse Excel file
        transactions = parser.parse(filepath)
        if not transactions:
            logger.warning(f"No transactions found in {filepath.name}")
            return False

        logger.info(f"Parsed {len(transactions)} transactions from {filepath.name}")

        # Categorize transactions
        categories = categorizer.categorize_transactions(transactions)

        # Write to master file
        writer.append_transactions(transactions, categories)

        # Mark as processed (before archiving, so file still exists)
        mark_as_processed(filepath, data_folder, len(transactions))

        # Archive file
        processed_folder = Path(config['folders']['processed'])
        archive_file(filepath, processed_folder, success=True)

        # Calculate stats
        duration = time.time() - start_time
        categorized_count = sum(1 for cat in categories.values() if cat != "לא סווג")
        accuracy = (categorized_count / len(transactions) * 100) if transactions else 0

        logger.info(
            f"✅ Processed {filepath.name}: {len(transactions)} transactions, "
            f"{categorized_count}/{len(transactions)} categorized ({accuracy:.0f}%), "
            f"{duration:.1f}s"
        )

        return True

    except Exception as e:
        logger.error(f"❌ Failed to process {filepath.name}: {e}", exc_info=True)

        # Move to errors folder
        processed_folder = Path(config['folders']['processed'])
        archive_file(filepath, processed_folder, success=False)

        # Create error log
        error_log = processed_folder / 'errors' / f"{filepath.stem}_error.txt"
        error_log.write_text(f"Error processing {filepath.name}:\n{str(e)}\n")

        return False


def process_all_files(config: dict):
    """Process all files in input folder once (manual mode)."""
    input_folder = Path(config['folders']['input'])

    # Find all XLS/XLSX files
    files = list(input_folder.glob('*.xls')) + list(input_folder.glob('*.xlsx'))

    if not files:
        logger.info("No files to process in input folder")
        return

    logger.info(f"Found {len(files)} file(s) to process")

    # Initialize components
    parser = ExcelParser(config)
    categorizer = Categorizer(config)
    writer = ExcelWriter(config)

    # Process each file
    success_count = 0
    for filepath in files:
        if process_file(filepath, config, parser, categorizer, writer):
            success_count += 1

    logger.info(f"Processed {success_count}/{len(files)} files successfully")


def watch_folder(config: dict):
    """Watch input folder continuously and process files as they arrive."""
    logger.info("Starting FinCat in watch mode...")
    logger.info(f"Monitoring: {config['folders']['input']}")
    logger.info("Press Ctrl+C to stop")

    # Initialize components
    parser = ExcelParser(config)
    categorizer = Categorizer(config)
    writer = ExcelWriter(config)

    # Define callback
    def on_file_detected(filepath: Path):
        process_file(filepath, config, parser, categorizer, writer)

    # Start file watcher
    watcher = FileWatcher(config, on_file_detected)

    try:
        watcher.start()

        # Keep main thread alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("\nStopping FinCat...")
        watcher.stop()
        logger.info("FinCat stopped")


def main():
    """Main entry point."""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='FinCat - Hebrew Credit Card Automation'
    )
    parser.add_argument(
        '--manual',
        action='store_true',
        help='Process all files once and exit (default: watch mode)'
    )
    parser.add_argument(
        '--config',
        default='config/config.yaml',
        help='Path to config file (default: config/config.yaml)'
    )

    args = parser.parse_args()

    try:
        # Load configuration
        config = load_config(args.config)

        # Setup logging
        setup_logging(config)

        # Create folders
        create_folders(config)

        logger.info("FinCat v1.0.0 - Hebrew Credit Card Automation")

        # Run in appropriate mode
        if args.manual:
            logger.info("Running in manual mode (process once)")
            process_all_files(config)
        else:
            logger.info("Running in watch mode (continuous)")
            watch_folder(config)

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
