# Name Lookup Flask + MySQL Application

A simple web application that checks if a name exists in a MySQL database.

## Features

- Clean, modern web interface
- Real-time name lookup in MySQL database
- Responsive design
- Easy-to-use form submission

## Prerequisites

- Python 3.9+
- MySQL Server running locally
- Virtual environment (already set up: `.venv`)

## Setup Instructions

### 1. Install Dependencies

```bash
.venv/bin/python -m pip install -r requirements.txt
```

### 2. Configure MySQL Credentials

Edit `main.py` and update the `DB_CONFIG` dictionary with your MySQL credentials:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # Change this!
    'database': 'name_db'
}
```

Do the same in `setup_db.py`.

### 3. Set Up the Database

Run the setup script to create the database and populate it with sample names:

```bash
.venv/bin/python setup_db.py
```

This will:
- Create a `name_db` database
- Create a `names` table
- Insert sample names (Alice, Bob, Charlie, Diana, Eve, Frank, Grace, Henry, Ivy, Jack)

### 4. Run the Application

```bash
.venv/bin/python main.py
```

The application will start on `http://localhost:5000`

### 5. Test the Application

Open your browser and navigate to `http://localhost:5000`. Try entering names like:
- ✓ Alice (exists in database)
- ✓ Bob (exists in database)
- ✗ Zoe (does not exist)

## Project Structure

```
helloworld/
├── main.py              # Flask application
├── setup_db.py          # Database setup script
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # HTML form template
├── .venv/               # Virtual environment
└── README.md            # This file
```

## Database Schema

The `names` table has the following structure:

```sql
CREATE TABLE names (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Adding More Names

### Via Python

Edit `setup_db.py` and add names to the `SAMPLE_NAMES` list, then run the script again.

### Via MySQL CLI

```bash
mysql -u root -p
USE name_db;
INSERT INTO names (name) VALUES ('Your Name');
```

## Troubleshooting

### Database Connection Error

**Error**: `Database connection failed`

**Solution**: 
- Ensure MySQL is running
- Check your credentials in `main.py`
- Verify the database exists: `mysql -u root -p -e "SHOW DATABASES;"`

### Permission Denied

**Error**: `Access denied for user 'root'@'localhost'`

**Solution**:
- Update the `password` in `DB_CONFIG` to match your MySQL password
- Or create a new MySQL user with appropriate permissions

### Table Not Found

**Error**: `Table 'name_db.names' doesn't exist`

**Solution**:
- Run the setup script again: `.venv/bin/python setup_db.py`

## Next Steps

- Add a database entry form to insert new names
- Add name editing/deletion features
- Implement user authentication
- Add pagination for large datasets
- Deploy to a cloud platform (AWS, Azure, etc.)
