# Process Flowcharts

Visual representations of the application's flows and processes.

---

## 🔄 User Search Flow

### ASCII Flowchart

```
┌─────────────────────────────────────┐
│  Start: User Opens Browser          │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Navigates to localhost:5000        │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Flask Receives GET Request         │
│  Route: /                           │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Calls home() Function              │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Renders index.html Template        │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Returns HTML Form                  │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Browser Displays Form              │
│  - Text input field                 │
│  - Search button                    │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  User Types Name                    │
│  Example: "Alice"                   │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  User Clicks Search Button          │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Form Submits POST Request          │
│  To: /check                         │
│  Data: name=Alice                   │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Flask Receives POST Request        │
└────────────┬────────────────────────┘
             │
             ↓
         CONTINUE BELOW...
```

### Database Query Flow

```
┌─────────────────────────────────────┐
│  check_name() Function Called       │
│  Parameter: name="Alice"            │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Extract Form Data                  │
│  name = request.form.get('name')    │
│  name = name.strip()                │
└────────────┬────────────────────────┘
             │
             ↓
         ┌───────────────────────┐
         │ Is name empty?        │
         └───────────────────────┘
              │          │
          YES │          │ NO
              ↓          ↓
    ┌─────────────┐  ┌──────────────────────┐
    │ Set error   │  │ Call                 │
    │ message     │  │ name_exists(name)    │
    │ "Please     │  └──────────┬───────────┘
    │ enter a     │             │
    │ name"       │             ↓
    └──────┬──────┘  ┌──────────────────────┐
           │         │ Get DB Connection    │
           │         │ get_db_connection()  │
           │         └──────────┬───────────┘
           │                    │
           │                    ↓
           │         ┌──────────────────────┐
           │         │ Connection Success?  │
           │         └──────────┬───────────┘
           │                    │
           │              ┌─────┴─────┐
           │              │           │
           │          YES │           │ NO
           │              ↓           ↓
           │    ┌──────────────────┐ ┌─────────────┐
           │    │ Create Cursor    │ │ Return Error│
           │    └────────┬─────────┘ │ Connection  │
           │             │           │ Failed      │
           │             ↓           └──────┬──────┘
           │    ┌──────────────────────────┐│
           │    │ Execute SQL Query        ││
           │    │ SELECT * FROM names      ││
           │    │ WHERE name = %s          ││
           │    └────────┬─────────────────┘│
           │             │                  │
           │             ↓                  │
           │    ┌──────────────────────────┐│
           │    │ Fetch Result             ││
           │    │ fetchone()               ││
           │    └────────┬─────────────────┘│
           │             │                  │
           │             ↓                  │
           │         ┌─────────────────┐   │
           │         │ Result Found?   │   │
           │         └─────┬───────────┘   │
           │               │               │
           │         ┌─────┴──────┐        │
           │         │            │       │
           │     YES │            │ NO    │
           │         ↓            ↓       │
           │   ┌──────────┐  ┌──────────┐ │
           │   │ found =  │  │ found =  │ │
           │   │ True     │  │ False    │ │
           │   └────┬─────┘  └────┬─────┘ │
           │        │             │       │
           │    GREEN MESSAGE  RED MESSAGE│
           │        │             │       │
           │        └──────┬──────┘       │
           │               │              │
           └───────┬───────┴──────────────┘
                   │
                   ↓
    ┌──────────────────────────────────────┐
    │ Render Template with Result          │
    │ render_template('index.html',        │
    │    result=message,                   │
    │    found=True/False)                 │
    └────────────┬─────────────────────────┘
                 │
                 ↓
    ┌──────────────────────────────────────┐
    │ Return HTML to Browser               │
    │ Green or Red Styled Message          │
    └────────────┬─────────────────────────┘
                 │
                 ↓
    ┌──────────────────────────────────────┐
    │ Browser Displays Result              │
    │ ✓ Found in database! (Green)         │
    │ OR                                   │
    │ ✗ Not found in database. (Red)       │
    └──────────────────────────────────────┘
```

---

## 🗄️ Database Schema Diagram

```
┌─────────────────────────────────────────────┐
│ Database: name_db                           │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │ Table: names                        │   │
│  ├─────────────────────────────────────┤   │
│  │ Column         │ Type        │ Attr │   │
│  ├────────────────┼─────────────┼──────┤   │
│  │ id             │ INT         │ PK ⭐ │   │
│  │ name           │ VARCHAR(100)│ UNQ  │   │
│  │ created_at     │ TIMESTAMP   │      │   │
│  ├─────────────────────────────────────┤   │
│  │                                     │   │
│  │ Rows (Sample Data):                 │   │
│  ├─────────────────────────────────────┤   │
│  │ 1 │ Alice    │ 2026-05-30 12:30:00  │   │
│  │ 2 │ Bob      │ 2026-05-30 12:30:01  │   │
│  │ 3 │ Charlie  │ 2026-05-30 12:30:02  │   │
│  │ 4 │ Diana    │ 2026-05-30 12:30:03  │   │
│  │ 5 │ Eve      │ 2026-05-30 12:30:04  │   │
│  │ 6 │ Frank    │ 2026-05-30 12:30:05  │   │
│  │ 7 │ Grace    │ 2026-05-30 12:30:06  │   │
│  │ 8 │ Henry    │ 2026-05-30 12:30:07  │   │
│  │ 9 │ Ivy      │ 2026-05-30 12:30:08  │   │
│  │10 │ Jack     │ 2026-05-30 12:30:09  │   │
│  │ …│ ...      │ ...                  │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘

PK = Primary Key (unique identifier)
UNQ = Unique constraint (no duplicates)
⭐ = Auto-increment (automatic numbering)
```

---

## 🔐 Error Handling Flow

```
┌─────────────────────────────────┐
│ User Submits Form               │
│ name = (user input)             │
└────────────┬────────────────────┘
             │
             ↓
    ┌─────────────────────────────┐
    │ Check: name empty?          │
    └────┬──────────────┬─────────┘
         │              │
     YES │              │ NO
         ↓              ↓
    ┌────────────┐  ┌──────────────────┐
    │ ERROR 1    │  │ Try DB Connect   │
    │ Empty Name │  │ get_db_connection│
    └────┬───────┘  └─────┬────────────┘
         │                │
         │                ↓
         │           ┌──────────────────┐
         │           │ Connection OK?   │
         │           └────┬──────┬──────┘
         │                │      │
         │            YES │      │ NO
         │                ↓      ↓
         │           ┌──────┐ ┌──────────┐
         │           │Query │ │ERROR 2   │
         │           │DB    │ │DB Connect│
         │           └─┬────┘ │Failed    │
         │             │      └────┬─────┘
         │             │           │
         │             ↓           │
         │        ┌──────────────┐ │
         │        │Query Success?│ │
         │        └──┬─────┬──────┘ │
         │           │     │        │
         │       YES │     │ NO     │
         │           ↓     ↓        │
         │      ┌──────┐┌──────┐    │
         │      │Found?││ERROR3│    │
         │      └┬──┬──┘└──┬───┘    │
         │        │ │      │        │
         │    YES │ │ NO   │        │
         │        ↓ ↓      │        │
         │     ┌──────────┐│        │
         │     │SUCCESS   ││        │
         │     │Green msg ││        │
         │     └────┬─────┘│        │
         │          │      │        │
         └──────┬───┴──────┴────────┘
                │
                ↓
        ┌──────────────────┐
        │ Display Result   │
        │ Green or Red     │
        │ Message          │
        └──────────────────┘

ERROR 1: "Please enter a name" (Red)
ERROR 2: "Database connection failed" (Red)
ERROR 3: "Database error: [message]" (Red)
SUCCESS: "✓ 'name' found in database!" (Green)
         OR
         "✗ 'name' not found in database." (Red)
```

---

## 📊 Application Startup Flow

```
┌─────────────────────────────────┐
│ User Runs: python main.py       │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│ Python Interprets main.py       │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│ Import Libraries                │
│ - Flask                         │
│ - mysql.connector               │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│ Initialize Flask App            │
│ app = Flask(__name__)           │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│ Define Routes                   │
│ @app.route("/")                 │
│ @app.route("/check", POST)      │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│ Check: if __name__ == '__main__'│
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│ Call app.run(debug=True)        │
│ - Start development server      │
│ - Bind to localhost:5000        │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│ Flask Running                   │
│ Listening on localhost:5000     │
│ Waiting for requests...         │
└─────────────────────────────────┘
```

---

## 🔗 Component Integration Diagram

```
┌──────────────────────────────────────────────┐
│         FLASK APPLICATION LAYER              │
├──────────────────────────────────────────────┤
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │ main.py                                │  │
│  ├────────────────────────────────────────┤  │
│  │ Routes:                                │  │
│  │ ├─ GET /          → home()             │  │
│  │ └─ POST /check    → check_name()       │  │
│  │                                        │  │
│  │ Functions:                             │  │
│  │ ├─ get_db_connection()                 │  │
│  │ └─ name_exists()                       │  │
│  │                                        │  │
│  │ Config:                                │  │
│  │ └─ DB_CONFIG (MySQL credentials)       │  │
│  └────────────────────────────────────────┘  │
│                 ↓         ↓                   │
├─────────────┬──────────────────┬─────────────┤
│             │                  │             │
│             ↓                  ↓             │
│     ┌──────────────┐   ┌──────────────┐     │
│     │ HTML/Template│   │ Error Handler│     │
│     │              │   │              │     │
│     │ index.html   │   │ Try/Except   │     │
│     │ - Form UI    │   │ blocks       │     │
│     │ - Result msg │   │              │     │
│     │ - Styling    │   │ Connection   │     │
│     │              │   │ Query errors │     │
│     └──────────────┘   └──────────────┘     │
└──────────────────────────────────────────────┘
             ↓
┌──────────────────────────────────────────────┐
│    MYSQL CONNECTOR LAYER (Driver)            │
├──────────────────────────────────────────────┤
│                                              │
│  mysql-connector-python                      │
│  - Connection management                     │
│  - Query execution                           │
│  - Result fetching                           │
│  - Error handling                            │
│                                              │
└──────────────────────────────────────────────┘
             ↓
┌──────────────────────────────────────────────┐
│       MYSQL DATABASE LAYER                   │
├──────────────────────────────────────────────┤
│                                              │
│  MySQL Server (localhost:3306)               │
│                                              │
│  Database: name_db                           │
│  ├─ Table: names                             │
│  │  ├─ Column: id (PK)                       │
│  │  ├─ Column: name (UNIQUE)                 │
│  │  └─ Column: created_at                    │
│  │                                           │
│  └─ Data: 10 sample names                    │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 📈 Deployment Flow (Future)

```
Local Development (Current)
    ↓
┌─────────────────────────────┐
│ Code Testing & Validation   │
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│ Commit to Git               │
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│ Push to GitHub              │
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│ CI/CD Pipeline (Future)     │
│ - Run tests                 │
│ - Build artifacts           │
│ - Deploy to staging         │
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│ Production Server           │
│ - Cloud hosting (AWS/Azure) │
│ - Production MySQL          │
│ - Load balancer             │
└─────────────────────────────┘
```

---

## 🔄 Testing Workflow

```
┌─────────────────────────────────┐
│ Unit Testing                    │
├─────────────────────────────────┤
│ - Test get_db_connection()      │
│ - Test name_exists()            │
│ - Test input validation         │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ Integration Testing             │
├─────────────────────────────────┤
│ - Flask + MySQL together        │
│ - Full request-response cycle   │
│ - Database queries              │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ Manual Testing                  │
├─────────────────────────────────┤
│ - UI testing in browser         │
│ - Search existing name          │
│ - Search non-existing name      │
│ - Test empty input              │
│ - Test error scenarios          │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ All Tests Passed ✓              │
│ Ready for Deployment            │
└─────────────────────────────────┘
```

---

**Last Updated:** May 30, 2026
**Version:** 1.0
