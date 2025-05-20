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

    # Create a dict of column_name: value
    columns = [column[0] for column in cursor.description]
    result = dict(zip(columns, row))

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
