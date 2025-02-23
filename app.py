from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home page with file upload form
@app.route('/')
def index():
    return render_template('index.html')

# Handle file upload and processing
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    if file and allowed_file(file.filename):
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the PDF using the Python notebook
        try:
            # Run the notebook as a script (assuming you've converted it to a .py file)
            subprocess.run(['python', 'BERTopic.py', file_path], check=True)
            
            # Return the processed CSV file for download
            output_csv_path = 'all_sentences.csv'
            return send_file(output_csv_path, as_attachment=True)
        except Exception as e:
            return f"Error processing file: {str(e)}", 500
    
    return "Invalid file type", 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)