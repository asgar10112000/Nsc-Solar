from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Connect to your SQLite database
conn = sqlite3.connect("consumer_data.db", check_same_thread=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    consumer_number = request.args.get('consumer_number')
    if not consumer_number:
        return jsonify({'error': 'Consumer Number required'}), 400

    query = "SELECT * FROM consumers WHERE `Consumer Number` = ?"
    cursor = conn.execute(query, (consumer_number,))
    row = cursor.fetchone()

    if not row:
        return jsonify({'message': 'No record found'}), 404

    # List of important fields to include in the response
    important_fields = [
        "Circle", "Division", "Sub-Division", "SRType",
        "MI Status", "Applicant Name", "Address",
        "District", "Phase", "Load"
    ]

    # Get all column names
    columns = [column[0] for column in cursor.description]
    row_dict = dict(zip(columns, row))

    # Filter to only important fields
    filtered_result = {key: row_dict[key] for key in important_fields if key in row_dict}

    return jsonify(filtered_result)

if __name__ == '__main__': 
    app.run(debug=True)
