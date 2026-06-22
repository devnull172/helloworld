from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MySecurePass123',  # MySQL root password
    'database': ''
}

def get_db_connection():
    """Establish and return a database connection."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def name_exists(name):
    """Check if a name exists in the database."""
    connection = get_db_connection()
    if connection is None:
        return None, "Database connection failed"
    
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM names WHERE name = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None, None
    except Error as e:
        return None, f"Database error: {e}"

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/check", methods=['POST'])
def check_name():
    name = request.form.get('name', '').strip()
    
    if not name:
        return render_template('index.html', result="Please enter a name", found=False)
    
    exists, error = name_exists(name)
    
    if error:
        result = error
        found = False
    elif exists:
        result = f"✓ '{name}' found in database!"
        found = True
    else:
        result = f"✗ '{name}' not found in database."
        found = False
    
    return render_template('index.html', result=result, found=found)

if __name__ == '__main__':
    app.run(debug=True)