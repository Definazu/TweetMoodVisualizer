# app.py
from flask import Flask, jsonify
from controllers import AnalysisController
from config import Config

app = Flask(__name__)
config = Config()

@app.route('/analyze/<table_name>', methods=['GET'])
def analyze(table_name):
    controller = AnalysisController(config)
    result = controller.process(table_name)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)