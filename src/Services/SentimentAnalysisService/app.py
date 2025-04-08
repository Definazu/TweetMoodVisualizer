# app.py
from flask import Flask, jsonify
from controllers import AnalysisController
from config import Config
from state_locator import StateLocator
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
try:
    config = Config()
    print("\n🔧 Configuration check:")
    print(f"Database path: {config.db_path} ({'exists' if config.db_path.exists() else 'missing'})")
    print(f"Sentiments path: {config.sentiments_path} ({'exists' if config.sentiments_path.exists() else 'missing'})")
    print(f"States path: {config.states_path} ({'exists' if config.states_path.exists() else 'missing'})")
except FileNotFoundError as e:
    print(f"❌ Configuration error: {e}")
    exit(1)

@app.route('/analyze/<table_name>', methods=['GET'])
def analyze(table_name):
    try:
        controller = AnalysisController(config)
        return jsonify(controller.process(table_name))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n📍 Running system checks...")
    locator = StateLocator(config.states_path)  # Теперь этот класс распознаётся
    locator.test_locations()
    
    from sentiment_analyzer import SentimentAnalyzer
    analyzer = SentimentAnalyzer(config.sentiments_path)
    analyzer.stats()
    
    print("\n🚀 Starting Flask server...")
    app.run(debug=True)