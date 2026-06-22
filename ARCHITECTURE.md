# System Architecture Documentation

This document describes the architecture, components, and data flow of the Name Lookup application.

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                    (HTML + CSS + JavaScript)                     │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP Request/Response
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                    FLASK WEB SERVER                              │
│  (Python web framework - runs on localhost:5000)                │
│                                                                   │
│  ┌──────────────────┐    ┌──────────────────┐                  │
│  │  Flask Routing   │    │  Request Handler │                  │
│  │                  │    │                  │                  │
│  │ / → home()       │    │ check_name()     │                  │
│  │ /check → POST    │    │ name_exists()    │                  │
│  └──────────────────┘    └──────────────────┘                  │
└────────────────────────┬────────────────────────────────────────┘
                         │ SQL Queries
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                   MYSQL DATABASE                                 │
│              (localhost:3306 - port 3306)                        │
│                                                                   │
│  Database: name_db                                               │
│  ┌──────────────────────────┐                                    │
│  │ Table: names             │                                    │
│  ├──────────────────────────┤                                    │
│  │ id (PK, Auto-Increment)  │                                    │
│  │ name (VARCHAR, UNIQUE)   │                                    │
│  │ created_at (TIMESTAMP)
   │                                    │
│  └──────────────────────────┘                                    │
│                                                                   │
│  Data: 10 sample names                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Component Breakdown

### 1. Frontend Layer

**File:** `templates/index.html`

**Components:**
- HTML form with text input
- Search button
- Result display area
- CSS styling for UI

**Responsibilities:**
- Display user interface
- Collect user input
- Show search results
- Apply conditional styling (green/red)

**Technologies:**
- HTML5 (structure)
- CSS3 (styling and gradients)
- Jinja2 templating (dynamic content)

---

### 2. Application Layer (Backend)

**File:** `main.py`

**Core Functions:**

#### `get_db_connection()`
```
Purpose: Establish MySQL database connection
Input: None (uses global DB_CONFIG)
Output: Connection object or None
Errors: MySQL connection errors
Flow:
  1. Use mysql.connector.connect()
  2. Pass DB_CONFIG credentials
  3. Return connection if successful
  4. Return None if failed
```

#### `name_exists(name)`
```
Purpose: Check if name exists in database
Input: name (string)
Output: (exists_boolean, error_message) tuple

Flow:
  1. Get database connection
  2. If connection fails → return (None, error_msg)
  3. Create cursor
  4. Execute: SELECT * FROM names WHERE name = %s
  5. Fetch result
  6. Close cursor and connection
  7. Return (True, None) if found
  8. Return (False, None) if not found
  9. Catch errors → return (None, error_msg)

Security:
  - Uses parameterized queries (% placeholder)
  - Prevents SQL injection attacks
  - Example: ✓ Good
    cursor.execute("... WHERE name = %s", (name,))
  - Example: ✗ Bad
    cursor.execute(f"... WHERE name = '{name}'")
```

#### `home()` - Route `/`
```
Purpose: Display home page
HTTP Method: GET
Flow:
  1. Render templates/index.html
  2. Pass empty result
  3. Return HTML to browser
```

#### `check_name()` - Route `/check` POST
```
Purpose: Process name search request
HTTP Method: POST
Input: Form data with 'name' field
Flow:
  1. Get 'name' from form
  2. Strip whitespace
  3. Validate name is not empty
  4. Call name_exists(name)
  5. Determine response message
  6. Render template with result
  7. Return HTML with green or red styling
  
Outcomes:
  - Empty name → "Please enter a name" (red)
  - DB connection error → "Database connection failed" (red)
  - Name found → "✓ 'name' found in database!" (green)
  - Name not found → "✗ 'name' not found in database." (red)
```

**Configuration:**
```python
DB_CONFIG = {
    'host': 'localhost',           # MySQL server address
    'user': 'root',                # MySQL username
    'password': 'MySecurePass123',  # MySQL password
    'database': 'name_db'          # Database to connect to
}
```

---

### 3. Data Layer (Database)

**Database Server:** MySQL 9.6.0 (localhost:3306)

**Database:** `name_db`

**Table:** `names`

**Schema:**
```sql
CREATE TABLE names (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Columns:**
| Column | Type | Purpose | Constraints |
|--------|------|---------|-------------|
| id | INT | Row identifier | PK, Auto-Increment |
| name | VARCHAR(100) | Name to search | UNIQUE, NOT NULL |
| created_at | TIMESTAMP | Insert time | Default: CURRENT_TIMESTAMP |

**Sample Data:**
```
1 | Alice    | 2026-05-30 ...
2 | Bob      | 2026-05-30 ...
3 | Charlie  | 2026-05-30 ...
4 | Diana    | 2026-05-30 ...
5 | Eve      | 2026-05-30 ...
6 | Frank    | 2026-05-30 ...
7 | Grace    | 2026-05-30 ...
8 | Henry    | 2026-05-30 ...
9 | Ivy      | 2026-05-30 ...
10| Jack     | 2026-05-30 ...
```

---

## 🔄 Data Flow Diagram

### User Search Flow

```
User Browser
    │
    │ 1. GET http://localhost:5000
    ↓
Flask Server
    │
    ├─→ home() function
    │   └─→ render_template('index.html')
    ↓
Browser displays form
    │
    │ 2. User enters name "Alice"
    │ 3. User clicks "Search" button
    │
    ↓
Browser
    │
    │ 4. POST http://localhost:5000/check
    │    Form data: name=Alice
    ↓
Flask Server
    │
    ├─→ check_name() function
    │   │
    │   ├─→ Get name from form: "Alice"
    │   │
    │   ├─→ Validate name is not empty ✓
    │   │
    │   ├─→ Call name_exists("Alice")
    │   │
    │   ├─→ Get DB connection
    │   │   │
    │   │   ├─→ MySQL: CONNECT root@localhost:3306
    │   │   │
    │   │   ├─→ USE name_db
    │   ↓   │
    │   MySQL Database
    │   │
    │   ├─→ Execute: SELECT * FROM names WHERE name = 'Alice'
    │   │
    │   ├─→ Result found: (1, 'Alice', timestamp)
    │   │
    │   ├─→ Return to Flask: (True, None)
    │   │
    │   ├─→ Create message: "✓ 'Alice' found in database!"
    │   │
    │   ├─→ Set found = True (for green styling)
    │   │
    │   ├─→ render_template with result
    ↓
Browser
    │
    ├─→ Display form again
    │
    ├─→ Show green box with: "✓ 'Alice' found in database!"
```

---

## 🔐 Security Architecture

### SQL Injection Prevention
```
✓ SAFE: Parameterized Query
cursor.execute("SELECT * FROM names WHERE name = %s", (user_input,))

✗ UNSAFE: String Concatenation
cursor.execute(f"SELECT * FROM names WHERE name = '{user_input}'")
// If user_input = "'; DROP TABLE names; --"
// Query becomes: SELECT * FROM names WHERE name = ''; DROP TABLE names; --'
```

### Connection Management
```
✓ SAFE: Connection Cleanup
connection = get_db_connection()
cursor = connection.cursor()
cursor.execute(...)
result = cursor.fetchone()
cursor.close()              # Close cursor
connection.close()          # Close connection
```

### Input Validation
```
✓ Validate before database query
name = request.form.get('name', '').strip()
if not name:
    return "Please enter a name"

✓ Validate input length
# MySQL VARCHAR(100) allows max 100 chars
# Application checks before query
```

---

## 📊 Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | HTML5 | - | User interface markup |
| Frontend | CSS3 | - | Styling and gradients |
| Frontend | Jinja2 | 3.1.6 | Template rendering |
| Backend | Python | 3.9.6 | Programming language |
| Backend | Flask | 3.0.0 | Web framework |
| Database | MySQL | 9.6.0 | Relational database |
| Driver | mysql-connector-python | 8.2.0 | Python MySQL driver |
| Env Mgmt | Homebrew | Latest | Package manager (macOS) |
| Env Mgmt | Virtual Environment | Python venv | Dependency isolation |

---

## 🚀 Deployment Architecture (Current)

```
┌──────────────────────────────────────────┐
│         DEVELOPER MACHINE                │
│            (macOS)                       │
├──────────────────────────────────────────┤
│                                          │
│  Python venv (.venv)                     │
│  └─ Flask 3.0.0                          │
│  └─ mysql-connector-python 8.2.0         │
│                                          │
├──────────────────────────────────────────┤
│                                          │
│  http://localhost:5000                   │
│  (Flask development server)               │
│                                          │
├──────────────────────────────────────────┤
│                                          │
│  MySQL Server (Homebrew)                 │
│  localhost:3306                          │
│  Database: name_db                       │
│                                          │
└──────────────────────────────────────────┘
```

---

## 🔄 Request-Response Cycle

### Step 1: Initial Page Load (GET /)
```
Browser → GET http://localhost:5000/
  ↓
Flask Router → Matches @app.route("/")
  ↓
home() function
  ↓
render_template('index.html')
  ↓
Jinja2 Template Engine
  ↓
Returns HTML with form
  ↓
← Browser displays form
```

### Step 2: Form Submission (POST /check)
```
Browser → POST http://localhost:5000/check
         (Form data: name="Alice")
  ↓
Flask Router → Matches @app.route("/check", methods=['POST'])
  ↓
check_name() function
  ├─ Extract: name = "Alice"
  ├─ Validate: not empty ✓
  ├─ Query: name_exists("Alice")
  │
  ├─ get_db_connection()
  │  └─ Connect to MySQL
  │
  ├─ Execute: SELECT * FROM names WHERE name = %s
  │  └─ Pass: ("Alice",)
  │
  ├─ Result: Found / Not Found
  │
  ├─ Create message & styling
  │
  └─ render_template('index.html', result=..., found=...)
  ↓
Jinja2 Template Engine
  ├─ If found == True → Green styling
  ├─ If found == False → Red styling
  ↓
Returns HTML with result message
  ↓
← Browser displays result
```

---

## 💾 Database Query Patterns

### Pattern 1: Read Operation (Search)
```sql
SELECT * FROM names WHERE name = %s

Python:
cursor.execute("SELECT * FROM names WHERE name = %s", (search_name,))
result = cursor.fetchone()
# Returns: (id, name, created_at) or None
```

### Pattern 2: Write Operation (Insert)
```sql
INSERT INTO names (name) VALUES (%s)

Python:
cursor.execute("INSERT INTO names (name) VALUES (%s)", (new_name,))
connection.commit()
```

### Pattern 3: Read All (Admin)
```sql
SELECT * FROM names

Python:
cursor.execute("SELECT * FROM names")
results = cursor.fetchall()
# Returns: [(id, name, created_at), ...]
```

---

## 🔧 Configuration Points

### Flask Configuration
**File:** `main.py`
- `DB_CONFIG` dictionary
- Database credentials
- Connection parameters

### MySQL Configuration
**Location:** `/opt/homebrew/etc/my.cnf`
- Server settings
- Port configuration
- Performance tuning

### Application Settings
**File:** `main.py`
- `app.run(debug=True)` - Debug mode enabled
- Port: 5000
- Host: localhost

---

## ⚠️ Error Handling Flow

```
User Action
    ↓
Validation Check
    ├─ Empty input? → Display "Please enter a name"
    └─ ✓ Valid
    ↓
Database Connection
    ├─ Connection fails? → Display "Database connection failed"
    └─ ✓ Connected
    ↓
Query Execution
    ├─ Query error? → Display "Database error: [error message]"
    └─ ✓ Successful
    ↓
Result Processing
    ├─ Found? → Green message
    └─ Not found? → Red message
```

---

## 📈 Scalability Notes

### Current Limitations
- Single Flask development server
- No caching implemented
- No connection pooling
- Synchronous request handling

### Future Improvements
- Use production WSGI server (Gunicorn, uWSGI)
- Implement Redis caching for frequent searches
- Connection pooling for better performance
- Async request handling (Celery)
- Load balancing for multiple servers
- Database replication for high availability

---

**Last Updated:** May 30, 2026
**Version:** 1.0
