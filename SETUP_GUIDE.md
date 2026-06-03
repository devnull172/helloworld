# Complete Setup Guide

Step-by-step instructions to set up and run the Name Lookup Flask + MySQL application.

---

## ✅ Prerequisites

Before starting, ensure you have:
- macOS system
- Terminal/bash knowledge
- Internet connection (for downloads)
- About 1-2 hours for complete setup

---

## 📋 Setup Steps

### Phase 1: Initial Project Setup

#### Step 1: Create Project Directory
```bash
mkdir -p ~/Projects/Hello_World/helloworld
cd ~/Projects/Hello_World/helloworld
```

**Explanation:** Creates a workspace for your project

---

#### Step 2: Initialize Git Repository
```bash
git init
```

**Explanation:** Enables version control for tracking changes

---

#### Step 3: Create Virtual Environment
```bash
python3 -m venv .venv
```

**Explanation:** Creates isolated Python environment to avoid package conflicts

**Files Created:**
```
.venv/
├── bin/
│   ├── python
│   ├── pip
│   └── activate
├── lib/
├── include/
└── pyvenv.cfg
```

---

#### Step 4: Activate Virtual Environment
```bash
source .venv/bin/activate
```

**Expected Output:** Prompt changes to `(.venv) $`

**Explanation:** Activates the isolated Python environment

---

#### Step 5: Upgrade pip
```bash
.venv/bin/python -m pip install --upgrade pip
```

**What It Does:**
- Upgrades pip package manager
- Version: 21.2.4 → 26.0.1

---

### Phase 2: Install Python Dependencies

#### Step 6: Create requirements.txt
```bash
cat > requirements.txt << EOF
Flask==3.0.0
mysql-connector-python==8.2.0
EOF
```

**File Contents:**
```
Flask==3.0.0
mysql-connector-python==8.2.0
```

**Explanation:** Lists all Python packages needed for the project

---

#### Step 7: Install Dependencies
```bash
.venv/bin/python -m pip install -r requirements.txt
```

**What It Installs:**
1. **Flask 3.0.0** - Web framework
2. **mysql-connector-python 8.2.0** - MySQL driver
3. **Dependencies:**
   - Werkzeug 3.1.8
   - Jinja2 3.1.6
   - click 8.1.8
   - itsdangerous 2.2.0
   - And others...

**Expected Output:**
```
Successfully installed Flask-3.0.0 mysql-connector-python-8.2.0 ...
```

---

### Phase 3: Set Up Database Infrastructure

#### Step 8: Install Homebrew (if not installed)
```bash
# Check if Homebrew is installed
which brew

# If not found, install it:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**What It Does:**
- Installs Homebrew package manager for macOS
- Used to install MySQL

---

#### Step 9: Install MySQL
```bash
brew install mysql
```

**What It Installs:**
- MySQL Server 9.6.0
- Command-line tools
- Libraries and dependencies

**Installation Location:** `/opt/homebrew/Cellar/mysql/9.6.0_3`

**Expected Duration:** 5-10 minutes

---

#### Step 10: Start MySQL Service
```bash
brew services start mysql
```

**What It Does:**
- Starts MySQL as background service
- Runs automatically on login

**Verify It's Running:**
```bash
brew services list | grep mysql
# Should show: mysql started
```

---

#### Step 11: Set MySQL Root Password
```bash
mysql -u root << EOF
ALTER USER 'root'@'localhost' IDENTIFIED BY 'MySecurePass123';
FLUSH PRIVILEGES;
EOF
```

**What It Does:**
- Sets root password to: `MySecurePass123`
- Reloads privilege tables

**Security Note:** Change password to something unique in production

---

### Phase 4: Create Application Files

#### Step 12: Create Flask Application (main.py)
```bash
cat > main.py << 'EOF'
from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MySecurePass123',
    'database': 'name_db'
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
EOF
```

**Explanation:** Creates main Flask application with database logic

---

#### Step 13: Create Templates Directory
```bash
mkdir -p templates
```

---

#### Step 14: Create HTML Template (templates/index.html)
```bash
cat > templates/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Name Lookup</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            text-align: center;
            width: 100%;
            max-width: 400px;
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        input[type="text"] {
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            padding: 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #764ba2;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
            font-size: 18px;
        }
        .result.found {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .result.not-found {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Name Lookup</h1>
        <form method="POST" action="/check">
            <input type="text" name="name" placeholder="Enter a name" required autofocus>
            <button type="submit">Search</button>
        </form>
        {% if result %}
            <div class="result {% if found %}found{% else %}not-found{% endif %}">
                {{ result }}
            </div>
        {% endif %}
    </div>
</body>
</html>
EOF
```

**Explanation:** Creates HTML form with styling

---

#### Step 15: Create Database Setup Script (setup_db.py)
```bash
cat > setup_db.py << 'EOF'
#!/usr/bin/env python3
"""Database setup script for the name lookup application."""

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MySecurePass123',
}

SAMPLE_NAMES = [
    'Alice', 'Bob', 'Charlie', 'Diana', 'Eve',
    'Frank', 'Grace', 'Henry', 'Ivy', 'Jack',
]

def create_database_and_table():
    """Create the database and names table."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("Creating database 'name_db'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS name_db")
        cursor.execute("USE name_db")
        
        print("Creating 'names' table...")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS names (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"✗ Error: {e}")
        return False

def insert_sample_data():
    """Insert sample names into the database."""
    try:
        config = DB_CONFIG.copy()
        config['database'] = 'name_db'
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print("Inserting sample names...")
        insert_query = "INSERT IGNORE INTO names (name) VALUES (%s)"
        
        cursor.executemany(insert_query, [(name,) for name in SAMPLE_NAMES])
        connection.commit()
        
        print(f"✓ Inserted {cursor.rowcount} names into database")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"✗ Error: {e}")
        return False

def show_database_contents():
    """Display all names in the database."""
    try:
        config = DB_CONFIG.copy()
        config['database'] = 'name_db'
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM names")
        rows = cursor.fetchall()
        
        print("\nNames in database:")
        for row in rows:
            print(f"  - {row[1]}")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"✗ Error: {e}")

if __name__ == '__main__':
    print("=== Name Lookup Database Setup ===\n")
    
    if create_database_and_table():
        if insert_sample_data():
            show_database_contents()
            print("\n✓ Database setup complete!")
        else:
            print("\n✗ Failed to insert sample data")
    else:
        print("\n✗ Failed to create database and table")
EOF
chmod +x setup_db.py
```

**Explanation:** Script to initialize MySQL database with sample data

---

### Phase 5: Initialize Database

#### Step 16: Run Database Setup
```bash
.venv/bin/python setup_db.py
```

**Expected Output:**
```
=== Name Lookup Database Setup ===

Creating database 'name_db'...
Creating 'names' table...
Inserting sample names...
✓ Inserted 10 names into database

Names in database:
  - Alice
  - Bob
  - Charlie
  - Diana
  - Eve
  - Frank
  - Grace
  - Henry
  - Ivy
  - Jack

✓ Database setup complete!
```

---

### Phase 6: Test the Application

#### Step 17: Start Flask Server
```bash
.venv/bin/python main.py
```

**Expected Output:**
```
 * Serving Flask app 'main'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
 * Restarting with reloader
 * Debugger is active!
```

**Note:** Server keeps running until you press `Ctrl+C`

---

#### Step 18: Open Application in Browser
1. Open web browser (Chrome, Safari, Firefox, etc.)
2. Navigate to: `http://localhost:5000`
3. You should see the search form

---

#### Step 19: Test Searches

**Test Case 1: Search for existing name**
- Enter: `Alice`
- Expected: Green message "✓ 'Alice' found in database!"

**Test Case 2: Search for non-existing name**
- Enter: `Zoe`
- Expected: Red message "✗ 'Zoe' not found in database."

**Test Case 3: Search with empty input**
- Leave blank and click Search
- Expected: Red message "Please enter a name"

**Test Case 4: Search with whitespace**
- Enter: `  Bob  ` (spaces around name)
- Expected: Green message (spaces are trimmed)

---

### Phase 7: Verify Database Connection

#### Step 20: Direct Database Access
```bash
# Connect to MySQL
mysql -u root -p'MySecurePass123' name_db

# Inside MySQL shell, run:
SELECT * FROM names;
SHOW TABLE STATUS\G;
EXIT;
```

**Expected Output:**
```
+----+---------+---------------------+
| id | name    | created_at          |
+----+---------+---------------------+
|  1 | Alice   | 2026-05-30 12:30:00 |
|  2 | Bob     | 2026-05-30 12:30:01 |
... (more names)
+----+---------+---------------------+
```

---

## 🔧 Troubleshooting

### Issue: "MySQL connection failed"

**Diagnosis:**
```bash
# Check if MySQL is running
brew services list | grep mysql

# Try connecting
mysql -u root -p'MySecurePass123'
```

**Solutions:**
```bash
# Restart MySQL
brew services restart mysql

# Wait 5 seconds and try again
sleep 5
.venv/bin/python main.py
```

---

### Issue: "Port 3306 already in use"

**Diagnosis:**
```bash
lsof -i :3306
```

**Solution:**
```bash
# Kill the process
brew services stop mysql
sleep 2
brew services start mysql
```

---

### Issue: "Access denied for user 'root'"

**Check Password:**
```bash
# Test connection
mysql -u root -p'MySecurePass123'

# If fails, reset password
mysql -u root << EOF
ALTER USER 'root'@'localhost' IDENTIFIED BY 'MySecurePass123';
FLUSH PRIVILEGES;
EOF
```

---

### Issue: "Can't find 'templates/index.html'"

**Check File Structure:**
```bash
# Should output:
# main.py
# setup_db.py
# requirements.txt
# templates/index.html
ls -la
ls -la templates/
```

**Solution:**
```bash
# Ensure templates directory exists
mkdir -p templates

# Ensure index.html is in templates
# Re-run Step 14
```

---

## 📁 Final Project Structure

After all steps, your directory should look like:

```
helloworld/
├── main.py                    # Flask application
├── setup_db.py                # Database setup script
├── requirements.txt           # Python dependencies
├── templates/
│   └── index.html            # HTML form template
├── .venv/                    # Virtual environment
│   ├── bin/
│   ├── lib/
│   └── pyvenv.cfg
├── .vscode/
│   └── settings.json         # VS Code settings
├── .git/                     # Git repository
├── README.md                 # Project overview
├── DEVELOPMENT.md            # Development process
├── ARCHITECTURE.md           # System architecture
├── FLOWCHART.md              # Process flowcharts
└── SETUP_GUIDE.md            # This file
```

---

## 🚀 Quick Reference Commands

### Daily Usage
```bash
# Activate environment
source .venv/bin/activate

# Start Flask server
.venv/bin/python main.py

# Access web app
# Open: http://localhost:5000

# Stop server
# Press: Ctrl+C
```

### Database Management
```bash
# Connect to database
mysql -u root -p'MySecurePass123' name_db

# View all names
SELECT * FROM names;

# Add a name
INSERT INTO names (name) VALUES ('John');

# Delete a name
DELETE FROM names WHERE name = 'John';

# Exit MySQL
EXIT;
```

### Service Management
```bash
# Start MySQL
brew services start mysql

# Stop MySQL
brew services stop mysql

# Restart MySQL
brew services restart mysql

# Check status
brew services list
```

### Dependency Management
```bash
# Install dependencies
.venv/bin/python -m pip install -r requirements.txt

# List installed packages
.venv/bin/python -m pip list

# Update a package
.venv/bin/python -m pip install --upgrade Flask

# Export dependencies
.venv/bin/python -m pip freeze > requirements.txt
```

---

## ✅ Completion Checklist

- [ ] Python virtual environment created
- [ ] Python virtual environment activated
- [ ] pip upgraded to latest version
- [ ] requirements.txt created
- [ ] Python dependencies installed
- [ ] Homebrew installed (macOS)
- [ ] MySQL installed via Homebrew
- [ ] MySQL service started
- [ ] MySQL root password set
- [ ] main.py created
- [ ] templates/index.html created
- [ ] setup_db.py created
- [ ] Database setup script executed
- [ ] Flask server starts without errors
- [ ] Web browser can access http://localhost:5000
- [ ] Search for existing name works (green result)
- [ ] Search for non-existing name works (red result)
- [ ] Direct MySQL access works
- [ ] All documentation files created

---

## 🎓 Next Steps After Setup

1. **Test the Application**
   - Perform all test cases from Phase 6

2. **Explore the Code**
   - Read through main.py
   - Understand the database schema
   - Study the HTML template

3. **Try Modifications**
   - Add more names to the database
   - Change the CSS styling
   - Add new search features

4. **Version Control**
   - Commit your code to Git
   - Push to GitHub

5. **Learn More**
   - Study Flask documentation
   - Learn MySQL query optimization
   - Explore web development concepts

---

**Last Updated:** May 30, 2026
**Status:** Ready for Implementation
**Estimated Setup Time:** 1-2 hours

---

## 📞 Support

If you encounter issues:

1. **Check the logs** - Flask will show detailed error messages
2. **Review troubleshooting section** - Solutions for common problems
3. **Check file permissions** - Ensure files are readable/writable
4. **Verify database connection** - Test directly with MySQL CLI
5. **Review error messages carefully** - They usually indicate the problem

