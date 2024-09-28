from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import os
from flask_cors import CORS
from Models.test_models import model_reply

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/maintenance-request', methods=['GET', 'POST'])
def maintenance_request():
    if request.method == 'POST':
        # handle form submission
        student_id = request.form.get('student_id')
        building = request.form.get('building')
        category = request.form.get('category')
        description = request.form.get('description')
        
        result = model_reply(student_id, building, category, description)

        # process form and redirect to success
        #return jsonify({'message': result}), 200
        csv_file_path = 'maintenance_requests.csv'

        # Check if the file exists to write the header only once
        file_exists = os.path.isfile(csv_file_path)

        with open(csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
        
        # Write header if file did not exist
        if not file_exists:
            csv_writer.writerow(['Student ID', 'Building', 'Category', 'Description'])
        
        # Write the data row
        csv_writer.writerow([student_id, building, category, description])


        return redirect(url_for('success'))

    return render_template('maintenance_request.html')


@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)