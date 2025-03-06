# data_processor.py
from collections import defaultdict

class DataProcessor:
    def __init__(self, db_manager, analyzer, locator):
        self.db_manager = db_manager
        self.analyzer = analyzer
        self.locator = locator

    def process_table(self, table_name):
        tweets = self.db_manager.get_tweets(table_name)
        state_scores = defaultdict(list)
        
        for tweet in tweets:
            score = self.analyzer.analyze(tweet.text)
            if score is not None:
                state = self.locator.locate(tweet.latitude, tweet.longitude)
                state_scores[state].append(score)
        
        return {
            state: sum(scores)/len(scores)
            for state, scores in state_scores.items()
        }