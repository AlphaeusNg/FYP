import zipfile
from io import BytesIO
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pathlib import Path
import os
from flask_server.image_modifier_class import ImageObject

# Set the current working directory to the directory of this script
os.chdir(os.path.dirname(__file__))

# Initialize Flask app
app = Flask(__name__)

# Configuration paths
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed_images'
DOWNLOAD_FOLDER = 'downloadZip'

# Create necessary directories if they don't exist
for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER, DOWNLOAD_FOLDER]:
    Path(folder).mkdir(parents=True, exist_ok=True)

# Configure Flask app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['STORAGE'] = True
CORS(app, origins=['https://localhost:3000', 'https://127.0.0.1:3000'])

# Route to process uploaded images
@app.route('/upload', methods=['POST'])
def process_images():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    files = request.files.getlist('file')
    translated_lang_code = [request.form.get('translated_lang_code', 'zh')]  # Default to Chinese if not specified
    original_lang_code = [request.form.get('original_lang_code', 'en')]  # Default to English if not specified
    processed_images = []

    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file:
            filename = secure_filename(file.filename)
            file_path = Path(app.config['UPLOAD_FOLDER']) / filename
            file.save(file_path)

            image_file = ImageObject(image_path=file_path)
            image_file.process_image(original_lang_code=original_lang_code, translated_lang_code=translated_lang_code)
            
            processed_image_path = Path(app.config['PROCESSED_FOLDER']) / file.filename
            processed_images.append(image_file.save_image(processed_image_path))
    
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

# Route to download the zip file
@app.route('/downloadZip')
def download_zip():
    zip_file_path = Path(app.config['DOWNLOAD_FOLDER']) / 'translated_images.zip'
    return send_file(zip_file_path, as_attachment=True, download_name='translated_images.zip')

# Route to delete uploaded files, processed images, and downloaded zip file
@app.route('/deleteFiles', methods=['POST'])
def delete_files():
    try:
        if not app.config['STORAGE']:
            # Delete uploaded files
            delete_files_in_directory(app.config['UPLOAD_FOLDER'])
            # Delete processed images
            delete_files_in_directory(app.config['PROCESSED_FOLDER'])
            # Delete downloaded zip file
            delete_files_in_directory(app.config['DOWNLOAD_FOLDER'])
            return jsonify({'message': 'Files deleted successfully'})
        
        else:
            return jsonify({'error': 'Storage is enabled. Cannot delete files.'})        
    
    except Exception as e:
        return jsonify({'error': str(e)})

def delete_files_in_directory(directory):
    """
    Helper function to delete files in a given directory.
    """
    for file_path in Path(directory).iterdir():
        if file_path.is_file():
            file_path.unlink()

if __name__ == "__main__":
    app.run(debug=False, host="")
