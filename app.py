from flask import Flask, request, jsonify
import csv
import os
from flask_cors import CORS
from finalmodel import model_reply

app = Flask(__name__)
CORS(app)

@app.route('/save-csv', methods=['POST'])
def save_csv():
    data = request.json
    student_id = data.get('student_id')
    building = data.get('building')
    category = data.get('category')
    description = data.get('description')

    # Specify the CSV file path
    result = model_reply(student_id, building, category, description)

    # Return a response
    return jsonify({'message': result}), 200

    # Check if the file exists to write the header only once
    '''file_exists = os.path.isfile(csv_file_path)

    with open(csv_file_path, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write header if file did not exist
        if not file_exists:
            csv_writer.writerow(['Student ID', 'Building', 'Category', 'Description'])
        
        # Write the data row
        csv_writer.writerow([student_id, building, category, description])

    return jsonify({'message': 'Data saved successfully'}), 200'''

if __name__ == '__main__':
    app.run(port=8080, debug=True)
