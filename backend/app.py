import os
from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests


def get_db_connection():
    """Create a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'user'),
            password=os.getenv('MYSQL_PASSWORD', '011007'),
            database=os.getenv('MYSQL_DB', 'counter_db')
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/api/click', methods=['POST'])
def handle_click():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        # Increment counter in the database
        cursor.execute("UPDATE counter SET count = count + 1 WHERE id = 1")
        connection.commit()
        # Fetch updated count
        cursor.execute("SELECT count FROM counter WHERE id = 1")
        count = cursor.fetchone()[0]
        return jsonify({'count': count})
    except Error as e:
        print(f"Error executing query: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/count', methods=['GET'])
def get_count():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT count FROM counter WHERE id = 1")
        count = cursor.fetchone()[0]
        return jsonify({'count': count})
    except Error as e:
        print(f"Error executing query: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(port=5000)