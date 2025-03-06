# sentiment_analyzer.py
import csv
from collections import defaultdict

class SentimentAnalyzer:
    def __init__(self, file_path):
        self.sentiment_scores = self._load_sentiments(file_path)

    def _load_sentiments(self, file_path):
        with open(file_path, 'r') as f:
            return {row['word']: float(row['score']) for row in csv.DictReader(f)}

    def analyze(self, text):
        words = text.lower().split()
        scores = [self.sentiment_scores[word] for word in words if word in self.sentiment_scores]
        return sum(scores)/len(scores) if scores else None