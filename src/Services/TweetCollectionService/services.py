# services.py
"""
Core business logic module for processing tweet files.

Contains the FileProcessingService class with data parsing and validation logic.
"""

import re
import os
from datetime import datetime
from typing import Dict
from database import Session, create_table, table_exists
from exceptions import InvalidDataFormatError

class FileProcessingService:
    """Main service class for processing tweet data files.
    
    Attributes:
        table_name (str): Sanitized name for the database table
        Tweet (DeclarativeMeta): SQLAlchemy model class for current table
        session (Session): Database session instance
    """
    
    def __init__(self, filename: str):
        """Initialize processing service for a specific file.
        
        Args:
            filename (str): Original name of the uploaded file
        """
        self.table_name = self._sanitize_filename(filename)
        self.Tweet = create_table(self.table_name)
        self.session = Session()

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to create valid SQL table name.
        
        Args:
            filename (str): Original filename with extension
            
        Returns:
            str: Valid SQL table name with:
            - Lowercase letters
            - Underscores instead of special characters
            - No file extensions
        """
        name = os.path.splitext(filename)[0]
        return re.sub(r'\W', '_', name).lower()

    def process_file(self, file) -> Dict:
        """Process uploaded file and store data in database.
        
        Args:
            file (FileStorage): Uploaded file object
            
        Returns:
            Dict: Processing results with:
            - status: Operation outcome
            - table: Created/updated table name
            - valid_records: Number of successfully processed records
            - errors: List of parsing errors
            
        Raises:
            InvalidDataFormatError: If file contains no valid records
            UnicodeDecodeError: If file has invalid encoding
        """
        valid_records = 0
        errors = []
        
        try:
            content = file.read().decode('utf-8')
            lines = content.splitlines()
            
            if table_exists(self.table_name):
                self.session.query(self.Tweet).delete()

            for line_num, line in enumerate(lines, 1):
                try:
                    tweet_data = self._parse_line(line)
                    self.session.add(self.Tweet(**tweet_data))
                    valid_records += 1
                except InvalidDataFormatError as e:
                    errors.append(f"Line {line_num}: {str(e)}")

            if valid_records == 0:
                raise InvalidDataFormatError("No valid records found")

            self.session.commit()
            return {
                'status': 'success',
                'table': self.table_name,
                'valid_records': valid_records,
                'errors': errors
            }

        except UnicodeDecodeError:
            raise InvalidDataFormatError("Invalid file encoding")
        except Exception:
            self.session.rollback()
            raise
        finally:
            Session.remove()

    def _parse_line(self, line: str) -> Dict:
        """Parse single line of tweet data.
        
        Args:
            line (str): Raw input line from file
            
        Returns:
            Dict: Parsed tweet data with keys:
            - latitude (float)
            - longitude (float)
            - created_at (datetime)
            - text (str)
            
        Raises:
            InvalidDataFormatError: For any parsing or validation failure
        """
        line = line.strip()
        pattern = r"""
            ^\[(-?\d+\.\d+),\s*(-?\d+\.\d+)\]\s+_
            \s+(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+(.*)$
        """
        match = re.match(pattern, line, re.VERBOSE)
        
        if not match:
            raise InvalidDataFormatError("Invalid line format")

        try:
            lat = float(match.group(1))
            lon = float(match.group(2))
            dt = datetime.strptime(match.group(3), '%Y-%m-%d %H:%M:%S')
            text = match.group(4).strip()

            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError("Invalid coordinates")
            
            if not text or len(text) > 500:
                raise ValueError("Invalid text content")

            return {
                'latitude': lat,
                'longitude': lon,
                'created_at': dt,
                'text': text
            }

        except ValueError as e:
            raise InvalidDataFormatError(str(e))