import os
from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)


def get_db_connection():
    """Create a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'mysql'),
            user=os.getenv('MYSQL_USER', 'user'),
            password=os.getenv('MYSQL_PASSWORD', 'password'),
            database=os.getenv('MYSQL_DB', 'counter_db')
        )
        if connection.is_connected():
            logger.info("Successfully connected to MySQL")
            return connection
    except Error as e:
        logger.error(f"Error connecting to MySQL: {e}")
        return None

@app.route('/api/click', methods=['POST'])
def handle_click():
    logger.info("Received click request")
    connection = get_db_connection()
    if connection is None:
        logger.error("Database connection failed")
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        # Increment counter in the database
        cursor.execute("UPDATE counter SET count = count + 1 WHERE id = 1")
        connection.commit()
        # Fetch updated count
        cursor.execute("SELECT count FROM counter WHERE id = 1")
        count = cursor.fetchone()
        if count is None:
            return jsonify({'error': 'No counter found for id = 1'}), 500
        return jsonify({'count': count[0]})
    except Error as e:
        logger.error(f"Database error in handle_click: {e}")
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if connection.is_connected():
            connection.close()

@app.route('/api/count', methods=['GET'])
def get_count():
    logger.info("Received count request")
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
    app.run(port=8000)