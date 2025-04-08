# routes.py
"""
API routes module for handling file uploads.

Contains the blueprint definition and route handlers for the upload endpoint.
"""

from flask import Blueprint, request, jsonify, current_app
from services import FileProcessingService
from database import get_all_tables
from exceptions import InvalidFileError, DataProcessingError


upload_blueprint = Blueprint('upload', __name__)

@upload_blueprint.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload requests.
    
    Processes POST requests with text files containing tweet data.
    
    Args:
        file (FileStorage): Uploaded text file via multipart/form-data
        
    Returns:
        JSON response with operation status:
        - Success: 200 OK with processing statistics
        - Client error: 400 Bad Request with error details
        - Server error: 500 Internal Server Error
        
    Example:
        curl -X POST -F "file=@data.txt" http://localhost:5001/upload
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        processor = FileProcessingService(file.filename)
        result = processor.process_file(file)
        return jsonify(result), 200

    except (InvalidFileError, DataProcessingError) as e:
        current_app.logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@upload_blueprint.route('/tables', methods=['GET'])
def get_tables():
    """Get list of all tweet tables in database.

    Returns:
        JSON response with list of table names or error message

    Example:
        curl http://localhost:5001/tables
    """
    try:
        tables = get_all_tables()
        return jsonify({'tables': tables}), 200
    except Exception as e:
        current_app.logger.error(f"Error retrieving tables: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to retrieve tables'}), 500