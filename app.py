from language_translation import translate
from text_detection.pdf_to_png_converter import convert_pdf_to_png
from text_detection import easy_ocr
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app, origins=['https://localhost:3000', 'https://127.0.0.1:3000'])

# Upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['OPTIONS', 'POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    files = request.files.getlist('file')
    uploaded_files = []

    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_files.append(filename)

    # Process uploaded files here, e.g., perform OCR, translation, etc.
    # Example: result = process_files(uploaded_files)
    # Replace process_files with your own logic

    # Return response with uploaded files or processed results
    return jsonify({'uploaded_files': uploaded_files})

if __name__ == "__main__":
    app.run(debug=True, host="")