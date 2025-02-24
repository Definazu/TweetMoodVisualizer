from flask import Blueprint, request, jsonify
from services import FileProcessingService
from exceptions import InvalidFileError, DataProcessingError

upload_blueprint = Blueprint('upload', __name__)

@upload_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        processor = FileProcessingService()
        result = processor.process_file(file)
        return jsonify(result), 200
    except (InvalidFileError, DataProcessingError) as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
