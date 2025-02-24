import re
from datetime import datetime
from exceptions import InvalidDataFormatError

class TweetParser:
    PATTERN = r'\[(-?\d+\.\d+),\s*(-?\d+\.\d+)\]\s+_\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(.*)'
    
    def parse(self, line: str) -> dict:
        match = re.match(self.PATTERN, line.strip())
        if not match:
            raise InvalidDataFormatError(f"Invalid data format: {line}")
        
        try:
            return {
                'latitude': float(match.group(1)),
                'longitude': float(match.group(2)),
                'created_at': datetime.strptime(match.group(3), '%Y-%m-%d %H:%M:%S'),
                'text': match.group(4)
            }
        except ValueError as e:
            raise InvalidDataFormatError(f"Error parsing values: {str(e)}")
