from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import json
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_IMAGES = 10

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_metadata():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            return json.load(f)
    return []

def save_metadata(metadata):
    with open('data.json', 'w') as f:
        json.dump(metadata, f)

def cleanup_images():
    metadata = load_metadata()
    now = datetime.now()
    to_delete = []
    for entry in metadata:
        expiration = datetime.fromisoformat(entry['expiration'])
        if now > expiration:
            try:
                os.remove(os.path.join(UPLOAD_FOLDER, entry['filename']))
                print(f"Deleted image: {entry['filename']}")  # Log deletion
                to_delete.append(entry)
            except FileNotFoundError:
                pass

    for entry in to_delete:
        metadata.remove(entry)
    save_metadata(metadata)

def start_cleanup_thread():
    while True:
        cleanup_images()
        time.sleep(10)  # Check every 10 seconds

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    metadata = load_metadata()
    images = [entry for entry in metadata if os.path.exists(os.path.join(UPLOAD_FOLDER, entry['filename']))]
    return render_template('gallery.html', images=images)

@app.route('/api/images')
def api_images():
    metadata = load_metadata()
    return jsonify(metadata)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'comment' not in request.form:
        return jsonify({'error': 'No file or comment part'}), 400

    file = request.files['file']
    comment = request.form['comment']

    if comment and len(comment) > 100:
        return jsonify({'error': 'Comment too long (max 100 characters)'}), 400

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = datetime.now().isoformat().replace(':', '-') + '.' + file.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if len(file.read()) > MAX_FILE_SIZE:
            return jsonify({'error': 'File too large (max 5MB)'}), 400

        file.seek(0)
        file.save(filepath)

        expiration = datetime.now() + timedelta(seconds=15)  # 5 seconds visible, 10 seconds fade-out
        metadata = load_metadata()
        metadata.append({
            'filename': filename,
            'comment': comment,
            'expiration': expiration.isoformat()
        })

        if len(metadata) > MAX_IMAGES:
            oldest_entry = min(metadata, key=lambda x: datetime.fromisoformat(x['expiration']))
            try:
                os.remove(os.path.join(UPLOAD_FOLDER, oldest_entry['filename']))
            except FileNotFoundError:
                pass
            metadata.remove(oldest_entry)

        save_metadata(metadata)
        return jsonify({'success': 'File uploaded successfully'}), 200

    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        metadata = load_metadata()
        metadata = [entry for entry in metadata if entry['filename'] != filename]
        save_metadata(metadata)
        return jsonify({'message': f'{filename} deleted successfully'})
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    threading.Thread(target=start_cleanup_thread, daemon=True).start()
    app.run(port=5000)
