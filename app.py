import os
from image_modifier_class import image_object
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask import send_file

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
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            uploaded_files.append(filename)

            image = image_object(file_path)
            # Perform OCR on the uploaded file
            ocr_results = perform_ocr(file_path)

            # Translate the OCR results to English
            translated_results = perform_translation(ocr_results)

            # Print or process translated results as needed
            for translated_text in translated_results:
                print(translated_text)
            # Overlay translated text onto the image
            overlayed_image = overlay_text(image_path, translated_text_data)

               
    return send_file(image_path, mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(debug=True, host="")
