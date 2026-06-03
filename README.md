# Name Lookup Flask + MySQL Application

A simple web application that checks if a name exists in a MySQL database.

## 🎯 Quick Start

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Start Flask server
.venv/bin/python main.py

# 3. Open browser to http://localhost:5000
```

---

## 📚 Documentation

This project includes comprehensive documentation covering every aspect:

### For Setup & Installation
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete step-by-step setup instructions
- **[README_FLASK_MYSQL.md](README_FLASK_MYSQL.md)** - Technical setup and troubleshooting

### For Understanding the Code
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development process broken down into phases
  - Phase 1: Initial Setup
  - Phase 2: Dependencies
  - Phase 3: Database Infrastructure
  - Phase 4: Backend Logic
  - Phase 5: Application Flow
  - Phase 6: Testing Checklist

### For System Design
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and components
  - High-level architecture diagram
  - Component breakdown
  - Data flow diagram
  - Security considerations

- **[FLOWCHART.md](FLOWCHART.md)** - Visual flowcharts and diagrams
  - User search flow (ASCII)
  - Database query flow
  - Database schema diagram
  - Error handling flow

---

## ⚡ Features

- ✅ Clean, modern web interface
- ✅ Real-time name lookup in MySQL database
- ✅ Responsive design with color-coded results
- ✅ Error handling and validation
- ✅ SQL injection prevention
- ✅ Comprehensive documentation

---

## 🚀 Running the Application

### Prerequisites
- Python 3.9+
- MySQL Server running (port 3306)
- Virtual environment activated

### Start the Server
```bash
source .venv/bin/activate
.venv/bin/python main.py
```

### Open in Browser
```
http://localhost:5000
```

### Try These Searches
- ✓ `Alice` → Green: "✓ 'Alice' found in database!"
- ✓ `Bob` → Green: "✓ 'Bob' found in database!"
- ✗ `Zoe` → Red: "✗ 'Zoe' not found in database."

---

## 📁 Project Structure

```
helloworld/
├── main.py                       # Flask application
├── setup_db.py                   # Database setup script
├── requirements.txt              # Python dependencies
├── templates/
│   └── index.html               # HTML form template
├── .venv/                       # Virtual environment
├── README.md                    # Overview (this file)
├── SETUP_GUIDE.md               # Step-by-step setup
├── DEVELOPMENT.md               # Development phases
├── ARCHITECTURE.md              # System design
└── FLOWCHART.md                 # Visual diagrams
```

---

## 🔧 Configuration

**MySQL Credentials** (in `main.py`):
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MySecurePass123',
    'database': 'name_db'
}
```

---

## 🗄️ Database

**Database:** `name_db`  
**Table:** `names`  
**Sample Data:** 10 pre-loaded names

```sql
CREATE TABLE names (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

---

## 🧪 Quick Test

```bash
# Activate environment
source .venv/bin/activate

# Run application
.venv/bin/python main.py

# In another terminal, connect to database
mysql -u root -p'MySecurePass123' name_db
SELECT * FROM names;
EXIT;
```

---

## 📞 Support

- **Setup Help:** See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Process Documentation:** See [DEVELOPMENT.md](DEVELOPMENT.md)
- **System Architecture:** See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Visual Flowcharts:** See [FLOWCHART.md](FLOWCHART.md)

---

**Status:** ✅ Fully Documented & Ready  
**Version:** 1.0  
**Last Updated:** May 30, 2026