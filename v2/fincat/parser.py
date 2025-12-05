"""
Excel file parsing for Hebrew credit card statements.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import xlrd
import openpyxl

logger = logging.getLogger('fincat.parser')


@dataclass
class Transaction:
    """Represents a single credit card transaction."""
    date: datetime
    card: str
    business_name: str
    amount: float
    currency: str
    installments: str
    details: str
    source_filename: str


class ExcelParser:
    """Parse XLS and XLSX files containing Hebrew credit card statements."""

    def __init__(self, config: dict):
        """Initialize parser with configuration."""
        self.config = config

    def parse(self, filepath: Path) -> List[Transaction]:
        """
        Parse XLS or XLSX file.

        Args:
            filepath: Path to Excel file

        Returns:
            List of Transaction objects
        """
        if filepath.suffix.lower() == '.xls':
            return self._parse_xls(filepath)
        else:
            return self._parse_xlsx(filepath)

    def _parse_xls(self, filepath: Path) -> List[Transaction]:
        """Parse legacy .xls format using xlrd."""
        try:
            workbook = xlrd.open_workbook(filepath)
            sheet = workbook.sheet_by_index(0)

            # Find header row and extract card number (search first 10 rows)
            header_row = None
            header_row_idx = 0
            card_number = "0000"  # Default if not found

            for i in range(min(10, sheet.nrows)):
                row = sheet.row_values(i)
                # Look for card number in rows like "כרטיס:1834"
                for cell in row:
                    if isinstance(cell, str) and 'כרטיס' in cell:
                        import re
                        match = re.search(r'(\d{4})', cell)
                        if match:
                            card_number = match.group(1)

                # Check if this row has column names (not empty, has Hebrew text)
                if any(isinstance(v, str) and v.strip() and any('\u0590' <= c <= '\u05FF' for c in v) for v in row):
                    try:
                        self._find_columns(row, require_card=False)  # Card column is optional
                        header_row = row
                        header_row_idx = i
                        break
                    except ValueError:
                        continue

            if header_row is None:
                raise ValueError("Could not find header row with required columns")

            # Find column indices (flexible)
            col_map = self._find_columns(header_row, require_card=False)

            transactions = []

            for row_idx in range(header_row_idx + 1, sheet.nrows):
                try:
                    # Extract values
                    date_val = sheet.cell_value(row_idx, col_map['date'])
                    # Use extracted card number or get from column if available
                    card = card_number if 'card' not in col_map else str(sheet.cell_value(row_idx, col_map['card']))[:4]
                    business = str(sheet.cell_value(row_idx, col_map['business']))
                    amount = float(sheet.cell_value(row_idx, col_map['amount']))

                    # Optional columns
                    currency = str(sheet.cell_value(row_idx, col_map.get('currency', col_map['amount'])))
                    if not currency or currency == str(amount):
                        currency = 'ILS'

                    details = str(sheet.cell_value(row_idx, col_map.get('details', col_map['business'])))

                    # Convert Excel date
                    date = xlrd.xldate_as_datetime(date_val, workbook.datemode)

                    # Parse installments
                    installments = self._parse_installments(details)

                    # Create transaction
                    transaction = Transaction(
                        date=date,
                        card=card,
                        business_name=business.strip(),
                        amount=amount,
                        currency=currency,
                        installments=installments,
                        details=details.strip(),
                        source_filename=filepath.name
                    )

                    transactions.append(transaction)

                except Exception as e:
                    logger.warning(f"Skipping row {row_idx} in {filepath.name}: {e}")
                    continue

            logger.info(f"Parsed {len(transactions)} transactions from {filepath.name} (XLS)")
            return transactions

        except Exception as e:
            logger.error(f"Failed to parse XLS file {filepath.name}: {e}")
            raise

    def _parse_xlsx(self, filepath: Path) -> List[Transaction]:
        """Parse modern .xlsx format using openpyxl."""
        try:
            workbook = openpyxl.load_workbook(filepath)
            sheet = workbook.active

            # Get header row
            header_row = [cell.value for cell in sheet[1]]
            col_map = self._find_columns(header_row)

            transactions = []

            for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                try:
                    # Extract values
                    date = row[col_map['date']]
                    card = str(row[col_map['card']])[:4]
                    business = str(row[col_map['business']])
                    amount = float(row[col_map['amount']])

                    # Optional columns
                    currency = str(row[col_map.get('currency', col_map['amount'])])
                    if not currency or currency == str(amount):
                        currency = 'ILS'

                    details = str(row[col_map.get('details', col_map['business'])])

                    # Handle date (might already be datetime)
                    if isinstance(date, datetime):
                        pass
                    elif isinstance(date, (int, float)):
                        # Excel serial date
                        date = datetime(1899, 12, 30) + timedelta(days=date)
                    else:
                        logger.warning(f"Unexpected date format in row {row_idx}: {date}")
                        continue

                    # Parse installments
                    installments = self._parse_installments(details)

                    # Create transaction
                    transaction = Transaction(
                        date=date,
                        card=card,
                        business_name=business.strip(),
                        amount=amount,
                        currency=currency,
                        installments=installments,
                        details=details.strip(),
                        source_filename=filepath.name
                    )

                    transactions.append(transaction)

                except Exception as e:
                    logger.warning(f"Skipping row {row_idx} in {filepath.name}: {e}")
                    continue

            logger.info(f"Parsed {len(transactions)} transactions from {filepath.name} (XLSX)")
            return transactions

        except Exception as e:
            logger.error(f"Failed to parse XLSX file {filepath.name}: {e}")
            raise

    def _find_columns(self, header_row: list, require_card: bool = True) -> dict:
        """
        Find column indices by header names (flexible matching).

        Args:
            header_row: List of header cell values
            require_card: Whether card column is required (default True)

        Returns:
            Dictionary mapping column type to index
        """
        col_map = {}

        # Define possible column names (Hebrew and English)
        column_names = {
            'date': ['תאריך', 'תאריך עסקה', 'date'],
            'card': ['כרטיס', 'מספר כרטיס', '4 ספרות', 'card'],
            'business': ['שם העסק', 'שם  העסק', 'עסק', 'שם בית העסק', 'business', 'business name'],
            'amount': ['סכום', 'סכום עסקה', 'סכום חיוב', 'סכום העסקה', 'amount'],
            'currency': ['מטבע', 'מט"ח', 'currency'],
            'details': ['פרטים', 'פרטים נוספים', 'פירוט', 'הערות', 'details', 'notes']
        }

        for idx, cell_value in enumerate(header_row):
            if cell_value is None:
                continue

            # Normalize: strip and collapse whitespace
            normalized = ' '.join(str(cell_value).strip().split()).lower()

            # Check each column type
            for col_type, possible_names in column_names.items():
                if any(name.lower() in normalized for name in possible_names):
                    if col_type not in col_map:  # Take first match
                        col_map[col_type] = idx

        # Validate required columns
        required = ['date', 'business', 'amount']
        if require_card:
            required.append('card')
        missing = [col for col in required if col not in col_map]

        if missing:
            raise ValueError(f"Missing required columns: {missing}. Found headers: {header_row}")

        logger.debug(f"Column mapping: {col_map}")
        return col_map

    def _parse_installments(self, details: str) -> str:
        """
        Parse installment information from details.

        Args:
            details: Transaction details string

        Returns:
            Installments as "X/Y" or empty string
        """
        import re

        # Look for pattern: "תשלום X מתוך Y"
        match = re.search(r'תשלום\s+(\d+)\s+מתוך\s+(\d+)', details)
        if match:
            return f"{match.group(1)}/{match.group(2)}"

        return ""


from datetime import timedelta
