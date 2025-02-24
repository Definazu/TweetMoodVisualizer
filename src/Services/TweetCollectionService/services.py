# services.py (бизнес-логика)
from parsers import TweetParser
from repositories import TweetRepository
from exceptions import InvalidFileError, DataProcessingError
from database import Session

class FileProcessingService:
    def __init__(self):
        self.parser = TweetParser()
        self.session = Session()
        self.repository = TweetRepository(self.session)
    
    def process_file(self, file):
        try:
            lines = file.read().decode('utf-8').splitlines()
            if not lines:
                raise InvalidFileError("Empty file")
            
            for line in lines:
                tweet_data = self.parser.parse(line)
                self.repository.add_tweet(tweet_data)
            
            self.repository.commit()
            return {'message': f'Successfully processed {len(lines)} tweets'}
        
        except UnicodeDecodeError:
            raise InvalidFileError("Invalid file encoding")
        except Exception as e:
            raise DataProcessingError(str(e))
        finally:
            self.session.remove()
