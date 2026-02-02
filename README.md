# WSGComponentTool

BFC Software Fundamentals Assignment 1

A Python-based GUI application for managing component inventory, users, and audit logs using SQLite databases. Built with Tkinter for the user interface and bcrypt for secure password hashing.

## Features

- **User Management**: Register and authenticate users with role-based access (admin/regular users).
- **Inventory Management**: Add, view, update, and manage items in stock with quantity tracking and low-stock alerts.
- **Audit Logging**: Tracks all actions performed in the system
- **GUI Interface**: User-friendly Tkinter-based interface with multiple pages (Login, Dashboard, Inventory, Stock Management, Admin Panel, User Management, Audit Logs).
- **Secure Authentication**: Passwords are hashed using bcrypt for security.

## Project Structure
```
WSGComponentTool/
├── README.md
├── Databases/
│   ├── users.db       # User database
│   ├── items.db       # Inventory database
│   └── audit.db       # Audit log database
├── Main/
│   ├── main.py        # Entry point to launch the GUI
│   ├── gui.py         # Tkinter GUI application
│   ├── user.py        # User class
│   ├── userdb.py      # User database operations
│   ├── item.py        # Item class
│   ├── itemdb.py      # Item database operations
│   ├── audit.py       # Audit class
│   └── auditdb.py     # Audit database operations
├── Unit Tests/
│   ├── test_users.py  # Unit tests for user functionality
│   └── test_itemdb.py # Unit tests for item database
└── Documentation/
    ├── designUMLpuml  # UML design diagrams
    └── documentation  # Full documentation for development
```

## How to install

1. **Download the repository** - Download and extract to a location of your choice.

2. **Install dependencies** - 'pip install -r requirements.txt'

## How to run

1. **Run the application** - run main.py - 'python Main/main.py'

2. **Login**
   
   The program comes with three example users. Use these or create your own account using the admin.



   (Username:Password)



   testuser:Password       - default account

   testuseradmin:Password  - admin account

   testuserlocked:Password - locked account



3. **Explore the GUI!**

## Testing

Run unit tests using Python's unittest module

Or run specific test files:
Tests/test_users.py
Tests/test_itemdb.py

## Dependencies

- Python
- `bcrypt` (for password hashing)
- Standard library: `sqlite3`, `tkinter`, `os`, `datetime`