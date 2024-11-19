import os
import csv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='build', static_url_path='/')

CORS(app)

# Configuring the upload folder and CSV file location
app.config['UPLOAD_FOLDER'] = './upload'
app.config['CSV_FILE'] = './data.csv'

# Function to write data to CSV
def write_to_csv(name, age, filename):
    file_exists = os.path.isfile(app.config['CSV_FILE'])
    with open(app.config['CSV_FILE'], mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Name', 'Age', 'File Name'])
        writer.writerow([name, age, filename])

# Serve the React app's static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    age = request.form.get('age')
    file = request.files.get('file')
    
    if not name or not age:
        return jsonify({'Error': 'Missing required fields'}), 400 
    
    if not file:
        return jsonify({'Error': 'File is required'}), 400
    
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    write_to_csv(name, age, file.filename)
    
    return jsonify({'message': 'Submission successful', 'name': name, 'age': age}), 200

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
