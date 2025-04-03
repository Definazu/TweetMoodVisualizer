# controllers.py
from database import DatabaseManager
from sentiment_analyzer import SentimentAnalyzer
from state_locator import StateLocator
from data_processor import DataProcessor

class AnalysisController:
    def __init__(self, config):
        self.db_manager = DatabaseManager(config.db_path)
        self.analyzer = SentimentAnalyzer(config.sentiments_path)
        self.locator = StateLocator(config.states_path)
        self.processor = DataProcessor(self.db_manager, self.analyzer, self.locator)

    def process(self, table_name):
        try:
            if not self.db_manager.table_exists(table_name):
                return {'error': f'Table "{table_name}" not found in database'}
                
            result = self.processor.process_table(table_name)
            return result if result else {'error': 'No valid data found'}
        except Exception as e:
            return {'error': f'Processing error: {str(e)}'}