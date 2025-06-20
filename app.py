@app.route('/search', methods=['GET'])
def search():
    consumer_number = request.args.get('consumer_number')
    if not consumer_number:
        return jsonify({'error': 'Consumer Number required'}), 400

    try:
        query = "SELECT * FROM consumers WHERE `Consumer Number` = ?"
        cursor = conn.execute(query, (consumer_number,))
        row = cursor.fetchone()

        if not row:
            return jsonify({'message': 'No record found'}), 404

        # Get all column names
        columns = [column[0] for column in cursor.description]
        row_dict = dict(zip(columns, row))

        # Only return selected fields
        required_fields = [
            "Circle", "Division", "Sub-Division", "SRType", 
            "MIStatus", "Applicant Name", "Address", 
            "District", "Phase", "Load"
        ]

        result = {key: row_dict[key] for key in required_fields if key in row_dict}
        return jsonify(result)
    
    except Exception as e:
        print("❌ Error during search:", e)  # This will print full error
        return jsonify({'error': 'Internal server error'}), 500
