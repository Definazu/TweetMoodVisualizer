# exceptions.py
"""
Custom exceptions module for error handling.

Contains application-specific exception classes for different error scenarios.
"""

class InvalidFileError(Exception):
    """Raised when invalid file is uploaded."""
    pass

class InvalidDataFormatError(Exception):
    """Raised when data format validation fails."""
    pass

class DataProcessingError(Exception):
    """Raised when general data processing error occurs."""
    pass