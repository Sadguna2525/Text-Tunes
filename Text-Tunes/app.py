from flask import Flask, request, jsonify, render_template, url_for
from PyPDF2 import PdfReader
import pyttsx3
import os
from flask_cors import CORS
#CORS stands for Cross-Origin Resource Sharing. It is a security feature implemented in web browsers to control how resources on a web page 
#can be requested from another domain, ensuring that such requests are made only if explicitly allowed by the server.
app = Flask(__name__)
CORS(app)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text += page_text
            else:
                app.logger.debug(f"No text found on page {page_number}")
    return text

def text_to_speech(text, audio_path, voice_id='HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0', rate=200):
    engine = pyttsx3.init()
    engine.setProperty('voice', voice_id)
    engine.setProperty('rate', rate)
    engine.save_to_file(text, audio_path)
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename.endswith('.pdf'):
            pdf_path = os.path.join('static/uploads', file.filename)
            file.save(pdf_path)
            pdf_text = extract_text_from_pdf(pdf_path)

            if not pdf_text.strip():
                return jsonify({'error': 'No text found in the PDF'}), 400

            audio_filename = file.filename.rsplit('.', 1)[0] + '.mp3'
            audio_path = os.path.join('static/uploads', audio_filename)
            text_to_speech(pdf_text, audio_path)

            audio_url = url_for('static', filename=f'uploads/{audio_filename}', _external=True)
            return jsonify({'success': True, 'audio_url': audio_url})

        return jsonify({'error': 'Select a PDF file'}), 400
    except Exception as e:
        app.logger.error(f"Error processing file upload: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == "__main__":
    os.makedirs('static/uploads', exist_ok=True)
    app.run(debug=True)





