import zipfile
from io import BytesIO
from flask_server.image_modifier_class import image_object
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pathlib import Path
import os

os.chdir(os.path.dirname(__file__))
app = Flask(__name__)

# Configuration path 
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed_images'
DOWNLOAD_FOLDER = 'downloadZip'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
Path(PROCESSED_FOLDER).mkdir(parents=True, exist_ok=True)
Path(DOWNLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

CORS(app, origins=['https://localhost:3000', 'https://127.0.0.1:3000'])


@app.route('/upload', methods=['POST'])
def process_images():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    files = request.files.getlist('file')
    uploaded_files = []
    translate_to_language = request.form.get('translate_to_language')
    original_language = request.form.get('original_language')
    file_folder_paths = []
    processed_images = []

    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file:
            filename = secure_filename(file.filename)
            file_path = Path(app.config['UPLOAD_FOLDER']) / filename
            file.save(file_path)
            file_folder_paths.append(file_path)
            uploaded_files.append(filename)
    
    for file in file_folder_paths:
        image_file = image_object(image_path=file)
        image_file.process_image(original_language=original_language, translated_language=translate_to_language)
        processed_image_path = Path(app.config['PROCESSED_FOLDER']) / file.name
        image_file.save_image(processed_image_path)
        processed_images.append(processed_image_path)
    
    # Create a zip archive containing all processed images
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for processed_image in processed_images:
            zip_file.write(processed_image, processed_image.name)

    zip_buffer.seek(0)

    # Save the zip file to the downloadZip folder
    zip_path = Path(app.config['DOWNLOAD_FOLDER']) / 'translated_images.zip'
    with open(zip_path, 'wb') as f:
        f.write(zip_buffer.getvalue())

    response = {
        'message': 'Upload completed successfully.'
    }
    return jsonify(response)
    
@app.route('/downloadZip')
def download_zip():
    # Logic to generate or retrieve the zip file
    zip_file_path = Path(app.config['DOWNLOAD_FOLDER']) / 'translated_images.zip'
    return send_file(zip_file_path, as_attachment=True, download_name='translated_images.zip')

@app.route('/deleteFiles', methods=['POST'])
def delete_files():
    try:
        # Delete uploaded files
        for file_path in Path(app.config['UPLOAD_FOLDER']).iterdir():
            if file_path.is_file():
                file_path.unlink()
        
        # Delete processed images
        for file_path in Path(app.config['PROCESSED_FOLDER']).iterdir():
            if file_path.is_file():
                file_path.unlink()
        
        # Delete downloaded zip file
        for file_path in Path(app.config['DOWNLOAD_FOLDER']).iterdir():
            if file_path.is_file():
                file_path.unlink()
        
        return jsonify({'message': 'Files deleted successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=False, host="")
