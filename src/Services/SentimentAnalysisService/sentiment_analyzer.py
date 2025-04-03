# sentiment_analyzer.py
import csv
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self, file_path):
        self.sentiment_scores = self._load_sentiments(file_path)
        logger.info(f"📚 Loaded {len(self.sentiment_scores)} sentiment words")

    def _load_sentiments(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return {
                    row[0].strip(): float(row[1])
                    for row in csv.reader(f)
                    if len(row) >= 2
                }
        except Exception as e:
            logger.error(f"🔥 Error loading sentiments: {str(e)}")
            return {}

    def analyze(self, text):
        try:
            words = re.findall(r'\b\w+\b', text.lower())
            scores = [self.sentiment_scores[word] for word in words if word in self.sentiment_scores]
            return sum(scores) / len(scores) if scores else None
        except Exception as e:
            logger.warning(f"⚠️ Error analyzing text: {str(e)}")
            return None

    def stats(self):
        sample = list(self.sentiment_scores.items())[:5]
        logger.info("📊 Sentiment analyzer stats:")
        logger.info(f"Sample words: {', '.join(f'{k} ({v})' for k, v in sample)}")