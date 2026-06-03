# Development Process Documentation

This document outlines the complete software development workflow for the Name Lookup Flask + MySQL application.

---

## 🎯 Project Overview

**Purpose:** A web application that allows users to search for names in a MySQL database and get immediate feedback on whether the name exists.

**Stack:**
- Backend: Python + Flask
- Database: MySQL
- Frontend: HTML + CSS
- Environment: Python 3.9 + Virtual Environment

---

## 📋 Development Phase 1: Initial Setup

### Step 1.1: Create Virtual Environment
```bash
python3 -m venv .venv
```
**Purpose:** Isolate project dependencies from system Python
**Status:** ✓ Completed

### Step 1.2: Activate Virtual Environment
```bash
source .venv/bin/activate
```
**Purpose:** Use isolated Python environment
**Status:** ✓ Completed

### Step 1.3: Upgrade pip
```bash
.venv/bin/python -m pip install --upgrade pip
```
**Purpose:** Ensure latest pip version (21.2.4 → 26.0.1)
**Status:** ✓ Completed

### Step 1.4: Remove Duplicate Environment
```bash
rm -rf .venv-1
```
**Purpose:** Clean up duplicate `.venv-1` that caused confusion
**Status:** ✓ Completed

---

## 📋 Development Phase 2: Install Dependencies

### Step 2.1: Create requirements.txt
```
Flask==3.0.0
mysql-connector-python==8.2.0
```
**Purpose:** Define all Python package dependencies
**Status:** ✓ Completed

### Step 2.2: Install Dependencies
```bash
.venv/bin/python -m pip install -r requirements.txt
```
**Purpose:** Install Flask web framework and MySQL connector
**Status:** ✓ Completed

**Packages Installed:**
- Flask 3.0.0 (web framework)
- mysql-connector-python 8.2.0 (database driver)
- Dependencies: Werkzeug, Jinja2, click, etc.

---

## 📋 Development Phase 3: Set Up Database Infrastructure

### Step 3.1: Install Homebrew (macOS)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
**Purpose:** Package manager to install MySQL
**Status:** ✓ Completed

### Step 3.2: Install MySQL via Homebrew
```bash
brew install mysql
```
**Purpose:** Install MySQL 9.6.0 database server
**Status:** ✓ Completed

### Step 3.3: Start MySQL Service
```bash
brew services start mysql
```
**Purpose:** Run MySQL as background daemon
**Status:** ✓ Completed

### Step 3.4: Secure MySQL Installation
```bash
mysql -u root << EOF
ALTER USER 'root'@'localhost' IDENTIFIED BY 'MySecurePass123';
FLUSH PRIVILEGES;
EOF
```
**Purpose:** Set root password and secure the installation
**Status:** ✓ Completed
**Credentials:**
- User: `root`
- Password: `MySecurePass123`
- Host: `localhost`
- Port: `3306`

---

## 📋 Development Phase 4: Create Backend Logic

### Step 4.1: Create Main Flask Application (main.py)

**Components:**
1. **Database Configuration**
   - Stores MySQL connection parameters
   - Credentials: localhost, root, password, name_db

2. **Connection Function: `get_db_connection()`**
   - Establishes MySQL connection
   - Handles connection errors gracefully
   - Returns connection object or None

3. **Query Function: `name_exists(name)`**
   - Accepts a name as parameter
   - Executes SQL SELECT query
   - Returns tuple: (exists_boolean, error_message)

4. **Home Route: `@app.route("/")`**
   - Handles GET requests to `/`
   - Renders HTML form template

5. **Check Route: `@app.route("/check", methods=['POST'])`**
   - Handles POST requests from form submission
   - Validates user input
   - Queries database
   - Determines response message
   - Returns HTML with result

**Status:** ✓ Completed

### Step 4.2: Create HTML Template (templates/index.html)

**Components:**
1. **HTML Structure**
   - Form with text input
   - Submit button

2. **CSS Styling**
   - Gradient background
   - Responsive card design
   - Color-coded messages (green for found, red for not found)

3. **Template Logic**
   - Displays form
   - Shows result message if provided
   - Applies styling based on result status

**Status:** ✓ Completed

### Step 4.3: Create Database Setup Script (setup_db.py)

**Components:**
1. **Database Creation**
   - SQL: `CREATE DATABASE IF NOT EXISTS name_db`

2. **Table Creation**
   - SQL: Create `names` table with columns:
     - `id` (auto-increment primary key)
     - `name` (VARCHAR 100, unique)
     - `created_at` (timestamp)

3. **Sample Data Insertion**
   - 10 sample names: Alice, Bob, Charlie, Diana, Eve, Frank, Grace, Henry, Ivy, Jack
   - Uses `INSERT IGNORE` to avoid duplicates

4. **Verification**
   - Displays all inserted names
   - Shows success/error messages

**Status:** ✓ Completed

### Step 4.4: Run Database Setup
```bash
.venv/bin/python setup_db.py
```
**Output:**
```
✓ Database created or already exists
✓ Table created or already exists
✓ Inserted 10 names into database
```
**Status:** ✓ Completed

---

## 📋 Development Phase 5: Application Flow

### User Request Flow (High Level)

```
1. User opens browser
   ↓
2. Types http://localhost:5000
   ↓
3. Flask receives GET request to /
   ↓
4. Calls home() function
   ↓
5. Renders templates/index.html
   ↓
6. User sees form with text input
   ↓
7. User types name and clicks "Search"
   ↓
8. Flask receives POST request to /check
   ↓
9. Calls check_name() function
   ↓
10. Extracts name from form data
   ↓
11. Validates name is not empty
   ↓
12. Calls name_exists(name)
   ↓
13. Connects to MySQL database
   ↓
14. Executes: SELECT * FROM names WHERE name = 'entered_name'
   ↓
15. Checks if result found
   ↓
16. Returns to check_name()
   ↓
17. Creates appropriate message (green or red)
   ↓
18. Renders template with result
   ↓
19. User sees green ✓ or red ✗ message
```

### Database Query Flow

```
name_exists("Alice")
    ↓
get_db_connection()
    ↓
mysql.connector.connect(
    host='localhost',
    user='root',
    password='MySecurePass123',
    database='name_db'
)
    ↓
connection.cursor()
    ↓
cursor.execute(
    "SELECT * FROM names WHERE name = %s",
    ("Alice",)
)
    ↓
cursor.fetchone()
    ↓
Returns: (1, 'Alice', '2026-05-30 12:34:56')  or  None
    ↓
Return: (True, None)  or  (False, None)
```

---

## 📋 Testing Checklist

### Manual Testing

- [ ] Application starts without errors
  ```bash
  .venv/bin/python main.py
  ```

- [ ] Web form loads at http://localhost:5000
  - Visual check: Form displays properly

- [ ] Search for existing name: "Alice"
  - Expected: Green message "✓ 'Alice' found in database!"

- [ ] Search for non-existing name: "Zoe"
  - Expected: Red message "✗ 'Zoe' not found in database."

- [ ] Search for empty input: ""
  - Expected: Red message "Please enter a name"

- [ ] Database connection test
  ```bash
  mysql -u root -p'MySecurePass123' name_db
  SELECT * FROM names;
  ```

### Error Handling Tests

- [ ] Stop MySQL service and try to search
  - Expected: "Database connection failed" message
  ```bash
  brew services stop mysql
  ```

- [ ] Restart MySQL after stopping
  ```bash
  brew services start mysql
  ```

---

## 🔍 Code Quality Checks

### Step 1: Syntax Validation
```bash
.venv/bin/python -m py_compile main.py
```
**Status:** ✓ Passed (all files valid)

### Step 2: Code Structure Review
- ✓ Functions are small and focused
- ✓ Error handling implemented
- ✓ SQL injection prevention (using parameterized queries)
- ✓ Connection cleanup (close cursor and connection)

### Step 3: Documentation
- ✓ Docstrings added to functions
- ✓ Code comments explain logic
- ✓ README files created

---

## 📁 Project File Structure

```
helloworld/
├── main.py                      # Flask application
├── setup_db.py                  # Database initialization
├── requirements.txt             # Python dependencies
├── templates/
│   └── index.html              # HTML form template
├── .venv/                       # Virtual environment
├── .vscode/
│   └── settings.json           # VS Code interpreter config
├── README.md                    # User guide
├── README_FLASK_MYSQL.md        # Technical setup guide
├── DEVELOPMENT.md               # This file - Development process
├── ARCHITECTURE.md              # System architecture
├── FLOWCHART.md                 # Visual flowcharts
├── SETUP_GUIDE.md               # Step-by-step setup
└── .git/                        # Git version control
```

---

## 🚀 Running the Application

### Quick Start
```bash
# Activate environment
source .venv/bin/activate

# Start Flask server
.venv/bin/python main.py

# Open browser
open http://localhost:5000
```

### Verify MySQL is Running
```bash
brew services list | grep mysql
# Should show: mysql started
```

### Check Database
```bash
mysql -u root -p'MySecurePass123' name_db -e "SELECT * FROM names;"
```

---

## 📝 Configuration Details

### Flask Configuration
```python
DB_CONFIG = {
    'host': 'localhost',        # MySQL server location
    'user': 'root',             # MySQL username
    'password': 'MySecurePass123',  # MySQL password
    'database': 'name_db'       # Database name
}
```

### Database Schema
```sql
CREATE TABLE names (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sample Data
```sql
INSERT INTO names (name) VALUES ('Alice');
INSERT INTO names (name) VALUES ('Bob');
INSERT INTO names (name) VALUES ('Charlie');
-- ... 7 more names (Diana, Eve, Frank, Grace, Henry, Ivy, Jack)
```

---

## 🔧 Common Commands Reference

| Task | Command |
|------|---------|
| Start MySQL | `brew services start mysql` |
| Stop MySQL | `brew services stop mysql` |
| Check MySQL status | `brew services list \| grep mysql` |
| Connect to MySQL | `mysql -u root -p'MySecurePass123' name_db` |
| Run Flask app | `.venv/bin/python main.py` |
| Install dependencies | `.venv/bin/python -m pip install -r requirements.txt` |
| View all names | `mysql -u root -p'MySecurePass123' name_db -e "SELECT * FROM names;"` |
| Add a name | `mysql -u root -p'MySecurePass123' name_db -e "INSERT INTO names (name) VALUES ('John');"` |

---

## ✅ Development Status

| Phase | Task | Status |
|-------|------|--------|
| 1 | Virtual Environment Setup | ✓ Complete |
| 2 | Dependencies Installation | ✓ Complete |
| 3 | Database Infrastructure | ✓ Complete |
| 4 | Backend Logic | ✓ Complete |
| 5 | Frontend Template | ✓ Complete |
| 6 | Testing | ⏳ Ready |
| 7 | Deployment | ⏳ Next |

---

## 📚 Additional Documentation Files

- **README.md** - User-facing overview
- **README_FLASK_MYSQL.md** - Technical setup and troubleshooting
- **ARCHITECTURE.md** - System design and components
- **FLOWCHART.md** - Visual request/response flows
- **SETUP_GUIDE.md** - Step-by-step installation

---

**Last Updated:** May 30, 2026
**Version:** 1.0
**Status:** Development Complete, Ready for Testing
