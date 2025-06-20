from flask import Flask, request, jsonify, render_template
import sqlite3

# ✅ Define the Flask app FIRST
app = Flask(__name__)

# ✅ Establish DB connection
conn = sqlite3.connect("consumer_data.db", check_same_thread=False)

# ✅ Route for homepage
@app.route('/')
def home():
    return render_template('index.html')

# ✅ Route for consumer search
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

    # Required fields in order
    required_fields = [
        "Circle", "Division", "Sub-Division", "SRType", "MIStatus",
        "Applicant Name", "Address", "District", "Phase", "Load"
    ]

    columns = [column[0] for column in cursor.description]
    data = dict(zip(columns, row))

    # Filter only required fields
    filtered_data = {field: data[field] for field in required_fields if field in data}

    return jsonify(filtered_data)

# ✅ Only use this for local development (Render uses Gunicorn)
if __name__ == '__main__':
    app.run(debug=True)
