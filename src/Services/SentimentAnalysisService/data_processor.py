# data_processor.py
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, db_manager, analyzer, locator):
        self.db_manager = db_manager
        self.analyzer = analyzer
        self.locator = locator

    def process_table(self, table_name):
        try:
            logger.info(f"📂 Processing table: {table_name}")
            tweets = self.db_manager.get_tweets(table_name)

            if not tweets:
                logger.warning("⚠️ Empty table")
                return {'error': 'Table is empty'}

            state_scores = defaultdict(list)
            counters = {
                'total': len(tweets),
                'missing_coords': 0,
                'no_sentiment': 0,
                'unknown_state': 0
            }

            for tweet in tweets:
                result = self._process_tweet(tweet, counters)
                if result:
                    state, score = result
                    state_scores[state].append(score)

            logger.info(f"""
                📊 Processing results:
                Total tweets: {counters['total']}
                Missing coordinates: {counters['missing_coords']}
                No sentiment: {counters['no_sentiment']}
                Unknown state: {counters['unknown_state']}
                Valid tweets: {sum(len(v) for v in state_scores.values())}
            """)

            # Логирование средних значений
            if state_scores:
                averages = {state: sum(scores)/len(scores) for state, scores in state_scores.items()}
                logger.info("📈 Calculated sentiment averages:")
                for state, avg in sorted(averages.items(), key=lambda x: x[1], reverse=True):
                    logger.info(f"  ▸ {state}: {avg:.4f}")

            return self._generate_output(state_scores) if state_scores else {}

        except Exception as e:
            logger.error(f"🔥 Processing error: {str(e)}")
            raise

    def _process_tweet(self, tweet, counters):
        try:
            lat, lon = tweet.latitude, tweet.longitude
            if None in (lat, lon):
                counters['missing_coords'] += 1
                return None

            score = self.analyzer.analyze(tweet.text)
            if score is None:
                counters['no_sentiment'] += 1
                return None

            state = self.locator.locate(lat, lon)
            if state == 'Unknown':
                counters['unknown_state'] += 1
                return None

            return state, score

        except Exception as e:
            logger.warning(f"⚠️ Error processing tweet: {str(e)}")
            return None

    def _generate_output(self, state_scores):
        averages = {state: sum(scores)/len(scores) for state, scores in state_scores.items()}
        min_score = min(averages.values())
        max_score = max(averages.values())
        range_score = max_score - min_score if max_score != min_score else 1

        logger.info("🌈 Final color mapping:")
        for state, score in sorted(averages.items()):
            logger.info(f"  ▸ {state}: {score:.4f} → {self._calculate_color(score, min_score, range_score)}")

        return {
            state: self._calculate_color(score, min_score, range_score)
            for state, score in averages.items()
        }

    def _calculate_color(self, score, min_score, range_score):
        """Convert sentiment score to color: blue(0) -> yellow(0.5) -> red(1)"""
        if range_score == 0:
            return '#ffff00'
        
        normalized = (score - min_score) / range_score
        
        # Первый сегмент: синий (0,0,255) -> голубой (0,255,255)
        if normalized <= 0.25:
            ratio = 4 * normalized
            return f'#00{int(255*ratio):02x}ff'
        
        # Второй сегмент: голубой (0,255,255) -> жёлтый (255,255,0)
        elif normalized <= 0.75:
            ratio = 2 * (normalized - 0.25)
            return f'#{int(255*ratio):02x}ff00'
        
        # Третий сегмент: жёлтый (255,255,0) -> красный (255,0,0)
        else:
            ratio = 2 * (normalized - 0.75)
            return f'#ff{int(255*(1-ratio)):02x}00'
