from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import uuid
import hashlib
from flask import send_from_directory

# Load environment variables from .env
load_dotenv()
SECRET_TOKEN = os.getenv("UPLOAD_TOKEN")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
PUBLIC_URL_BASE = os.getenv("PUBLIC_URL_BASE")

app = Flask(__name__)

# Directory to store uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    token = request.headers.get('X-Auth-Token')
    if token != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Create a unique filename using uuid and save.
    # filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    # filename = str(uuid.uuid4())[:8] + os.path.splitext(file.filename)[1]
    ext = ".tar.gz" if file.filename.endswith(".tar.gz") else os.path.splitext(file.filename)[1]
    filename = str(uuid.uuid4())[:8] + ext
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
    file.save(file_path)
    
    public_url = f"{PUBLIC_URL_BASE}/{filename}"    
    return jsonify({"public_url": public_url}), 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5011, threaded=True)

